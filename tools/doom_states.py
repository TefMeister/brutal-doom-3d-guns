"""doom_states.py - play a DECORATE weapon's state list forward, the way GZDoom would, for one made-up situation
(how much ammo is in the gun and in the pocket), and time it. Used by weapon_sheet.py.

Every check the weapon makes is answered from a small pretend inventory: ammo is whatever the situation says,
every other item (purist mode, zoomed, running, tactical class...) is absent unless the weapon gives it to itself.
Random jumps are never taken. So the times are the PLAIN path: normal mode, nobody pressing anything.
"""
import re

TICS_PER_SECOND = 35          # Doom's fixed game clock
MAX_STEPS = 20000             # a run that has not reached a resting state by then is reported as cut short
READY_LABELS = {"ready", "ready3", "oktofire", "readytofireagain", "ready2"}

FLOW = re.compile(r"^\s*(goto|stop|loop|wait|fail)\b\s*([\w.:]*)\s*(?:\+\s*(\d+))?", re.I)
LABEL = re.compile(r"^\s*([A-Za-z_][\w.]*)\s*:(?!:)")
FRAME = re.compile(r'^\s*("[^"]+"|[A-Za-z0-9_#\-]{4})\s+("[^"]+"|[A-Za-z\[\]\\^#]+)\s+(-?\d+|random\s*\([^)]*\))\s*(.*)$',
                   re.I)
CALL = re.compile(r"(A_\w+)\s*\(", re.I)
ARGS = re.compile(r'"[^"]*"|[^,]+')


def strip_comment(line):
    out, q, i = [], False, 0
    while i < len(line):
        ch = line[i]
        if ch == '"':
            q = not q
        if not q and line[i:i + 2] == "//":
            break
        if not q and line[i:i + 2] == "/*":
            j = line.find("*/", i + 2)
            i = len(line) if j < 0 else j + 2
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def tics_of(text):
    m = re.match(r"random\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)", text, re.I)
    return (int(m.group(1)) + int(m.group(2))) / 2 if m else int(text)


def calls(action):
    """[(name, [args])] for every A_ call on a state line (nested brackets kept in the args)."""
    out = []
    for m in CALL.finditer(action):
        depth, j = 0, m.end() - 1
        for j in range(m.end() - 1, len(action)):
            depth += {"(": 1, ")": -1}.get(action[j], 0)
            if depth == 0:
                break
        inner = action[m.end():j]
        parts, buf, d = [], "", 0
        for ch in inner:
            if ch == "," and d == 0:
                parts.append(buf.strip())
                buf = ""
                continue
            d += {"(": 1, ")": -1}.get(ch, 0)
            buf += ch
        if buf.strip():
            parts.append(buf.strip())
        out.append((m.group(1), parts))
    return out


def flatten(lines):
    """One entry per state (a frame letter), plus label positions. A goto/stop/loop/wait is not a state of its own:
    it says where the state BEFORE it goes next, so jump offsets count frames only, as GZDoom does."""
    states, labels, sprite = [], {}, "TNT1"
    for raw in lines:
        line = strip_comment(raw).replace("{", " ").replace("}", " ").rstrip()
        while True:
            m = LABEL.match(line)
            if not m or FRAME.match(line):
                break
            labels[m.group(1).lower()] = len(states)
            line = line[m.end():]
        if not line.strip():
            continue
        f = FLOW.match(line)
        if f:
            if states:
                states[-1]["after"] = {"flow": f.group(1).lower(), "target": f.group(2).lower(),
                                       "plus": int(f.group(3) or 0)}
            continue
        m = FRAME.match(line)
        if not m:
            continue
        spr, frames = m.group(1).strip('"'), m.group(2).strip('"')
        if spr != "####":
            sprite = spr
        act = calls(m.group(4))
        bright = "BRIGHT" in m.group(4).upper().split("A_")[0]
        for ch in frames:
            states.append({"sprite": sprite, "frame": ch, "tics": tics_of(m.group(3)), "calls": act,
                           "bright": bright})
    return states, labels


def unq(s):
    return s.strip().strip('"')


def simulate(states, labels, start, inv, maxima):
    """Run from label `start`. Returns the timeline: total tics, shots, sounds and sprite frames, each with its tic."""
    if start.lower() not in labels:
        return None
    inv = dict(inv)
    i, t, steps = labels[start.lower()], 0.0, 0
    shots, sounds, frames, end = [], [], [], "cut short"

    def jump(target, plus=0):
        target = unq(target).lower()
        if target.isdigit():
            return None
        return labels.get(target, None) if not plus else (labels[target] + plus if target in labels else None)

    while steps < MAX_STEPS:
        steps += 1
        here = [k for k, v in labels.items() if v == i]
        if steps > 1 and here and set(here) & READY_LABELS:
            end = "ready (" + here[0] + ")"
            break
        if i >= len(states):
            end = "fell off the end"
            break
        s = states[i]
        nxt, jumped = i + 1, False
        for name, args in s["calls"]:
            low = name.lower()
            if low in ("a_giveinventory", "a_takeinventory") and args:
                item = unq(args[0]).lower()
                n = int(args[1]) if len(args) > 1 and args[1].strip().lstrip("-").isdigit() else 1
                cap = maxima.get(item, 1)
                if low == "a_giveinventory":
                    inv[item] = min(cap, inv.get(item, 0) + n)
                else:
                    inv[item] = max(0, inv.get(item, 0) - n)
            elif low == "a_jumpifinventory" and len(args) >= 3:
                item, need = unq(args[0]).lower(), args[1].strip()
                need = int(need) if need.lstrip("-").isdigit() else 1
                have = inv.get(item, 0)
                taken = have >= (maxima.get(item, 1) if need == 0 else need) and have > 0
                if taken:
                    tgt = args[2].strip()
                    if tgt.lstrip("-").isdigit():
                        nxt, jumped = i + int(tgt), True
                    else:
                        lab = unq(tgt).lower()
                        if lab in READY_LABELS:
                            end = "ready (" + lab + ")"
                            return finish(t, shots, sounds, frames, end)
                        p = jump(lab)
                        if p is None:
                            return finish(t, shots, sounds, frames, "jump to " + lab + " (not followed)")
                        nxt = p
                    jumped = True
                    break
            elif low == "a_jump" and len(args) >= 2 and args[0].strip() == "256":
                tgt = args[1].strip()
                nxt = i + int(tgt) if tgt.isdigit() else (jump(tgt) or nxt)
                jumped = True
                break
            elif low == "a_firebullets":
                shots.append({"tic": t, "bullets": args[2] if len(args) > 2 else "?",
                              "damage": args[3] if len(args) > 3 else "?",
                              "puff": unq(args[4]) if len(args) > 4 else ""})
            elif low in ("a_firecustommissile", "a_fireprojectile") and args:
                shots.append({"tic": t, "projectile": unq(args[0])})
            elif low in ("a_railattack", "a_custompunch", "a_saw"):
                shots.append({"tic": t, low[2:]: ", ".join(args)})
            elif low in ("a_playsound", "a_startsound", "a_playweaponsound") and args:
                sounds.append({"tic": t, "sound": unq(args[0])})
        if s["tics"] < 0:
            end = "rests here for good"
            break
        if s["tics"] > 0 and s["sprite"] != "TNT1":
            frames.append({"tic": t, "sprite": s["sprite"] + s["frame"], "tics": s["tics"], "bright": s["bright"]})
        t += s["tics"]
        flow = s.get("after")
        if flow and not jumped:
            if flow["flow"] == "goto":
                if flow["target"] in READY_LABELS:
                    end = "ready (" + flow["target"] + ")"
                    break
                n = jump(flow["target"], flow["plus"])
                if n is None:
                    end = "goto " + flow["target"] + " (not followed)"
                    break
                nxt = n
            elif flow["flow"] == "loop":
                nxt = max((v for v in labels.values() if v <= i), default=0)
            else:
                end = flow["flow"]
                break
        i = nxt
    return finish(t, shots, sounds, frames, end)


def finish(t, shots, sounds, frames, end):
    return {"tics": t, "seconds": round(t / TICS_PER_SECOND, 2), "ends": end,
            "shots": shots, "sounds": sounds, "frames": frames}
