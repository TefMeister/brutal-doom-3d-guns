"""weapon_sheet.py - read every weapon out of a Brutal Doom pk3 (unpacked) and write one sheet of numbers: how
long firing, reloading, raising and lowering take, what each shot fires and for how much damage, magazine and
ammo, and when each sound plays. Nothing of Brutal Doom is copied into the sheet, only the numbers and names.

    python weapon_sheet.py <unpacked pk3 folder> <out folder>

Writes <out>/weapons.json (every frame and sound with its tic, for timing animations) and <out>/WEAPONS.md.
Times come from playing the weapon's states forward (doom_states.py) on the plain path: normal mode, nobody
pressing anything, ammo as the situation says. So they are [inferred-static] until timed in the game.
"""
import json
import os
import re
import sys

from doom_states import TICS_PER_SECOND, flatten, simulate, strip_comment

ACTOR = re.compile(r"^\s*actor\s+(\w+)\s*(?::\s*(\w+))?", re.I)
PROP = re.compile(r"^\s*(Weapon\.\w+|Inventory\.\w+|Ammo\.\w+|Tag)\s+(.+?)\s*$", re.I)
# projectiles fired only for show (far-away sound, smoke, tracers, casings): kept out of the damage column
COSMETIC = re.compile(r"sound|particle|tracer|smoke|case|casing|spark|flash|light|puff|empty|muzzle", re.I)
DEFAULT_POCKET_MAX = 50        # carry limit assumed for an ammo type whose MaxAmount the files do not give
WEAPON_BASES = {"weapon", "brutalweapon", "doomweapon"}
# items every normal player class starts with (Rifle, Pistol, Melee and Purist all give it; only Tactical lacks it)
NORMAL_PLAYER_ITEMS = {"isnottacticalclass": 1}
# the situations each weapon is played through: (row name, start label, magazine, pocket)
SITUATIONS = (("Fire (one shot, back to ready)", "Fire", "full", "full"),
              ("Reload from empty", "Reload", 0, "full"),
              ("Reload with one round used", "Reload", "full-1", "full"),
              ("Raise (select)", "Select", "full", "full"),
              ("Lower (deselect)", "Deselect", "full", "full"),
              ("Alt fire / aim", "AltFire", "full", "full"))


def read_actors(root):
    actors = []
    for dp, _, fns in os.walk(os.path.join(root, "actors")):
        for fn in fns:
            if not fn.lower().endswith((".dec", ".txt")):
                continue
            cur, depth, body = None, 0, []
            for raw in open(os.path.join(dp, fn), encoding="utf-8", errors="replace"):
                line = strip_comment(raw)
                if cur is None:
                    m = ACTOR.match(line)
                    if not m:
                        continue
                    cur = {"name": m.group(1), "parent": (m.group(2) or ""), "file": fn, "props": {}}
                    depth, body = 0, []
                depth += line.count("{") - line.count("}")
                body.append(raw)
                if depth <= 0 and "}" in line:
                    split_body(cur, body)
                    actors.append(cur)
                    cur = None
    return actors


def split_body(actor, body):
    in_states, states = False, []
    for raw in body[1:]:
        line = strip_comment(raw)
        if re.match(r"^\s*states\b", line, re.I):
            in_states = True
            continue
        if in_states:
            states.append(raw)
        else:
            p = PROP.match(line)
            if p:
                actor["props"][p.group(1).lower()] = p.group(2).strip('"')
    actor["states"] = states


def is_weapon(actor, by_name):
    seen, a = set(), actor
    while a and a["name"].lower() not in seen:
        seen.add(a["name"].lower())
        if a["parent"].lower() in WEAPON_BASES:
            return True
        a = by_name.get(a["parent"].lower())
    return False


def sound_files(root):
    """Logical sound name -> file inside the pk3, from every SNDINFO."""
    lumps = {}
    for dp, _, fns in os.walk(os.path.join(root, "sounds")):
        for fn in fns:
            lumps.setdefault(os.path.splitext(fn)[0].lower(), os.path.relpath(os.path.join(dp, fn), root))
    out = {}
    for fn in os.listdir(root):
        if not fn.upper().startswith("SNDINFO"):
            continue
        for raw in open(os.path.join(root, fn), encoding="utf-8", errors="replace"):
            parts = strip_comment(raw).split()
            if len(parts) >= 2 and not parts[0].startswith("$"):
                out[parts[0].lower()] = lumps.get(parts[1].lower(), parts[1])
    return out


def amount(word, cap):
    if word == "full":
        return cap
    if word == "full-1":
        return max(0, cap - 1)
    return word


def sheet(root):
    actors = read_actors(root)
    by_name = {a["name"].lower(): a for a in actors}
    maxima = {a["name"].lower(): int(a["props"]["inventory.maxamount"])
              for a in actors if a["props"].get("inventory.maxamount", "").isdigit()}
    sounds = sound_files(root)
    weapons = []
    for a in actors:
        if not is_weapon(a, by_name) or not a["states"]:
            continue
        states, labels = flatten(a["states"])
        pocket = a["props"].get("weapon.ammotype1", "").lower()
        mag = a["props"].get("weapon.ammotype2", "").lower()
        runs = {}
        for row, start, in_mag, in_pocket in SITUATIONS:
            inv = dict(NORMAL_PLAYER_ITEMS)
            if pocket:
                inv[pocket] = amount(in_pocket, maxima.get(pocket, DEFAULT_POCKET_MAX))
            if mag:
                inv[mag] = amount(in_mag, maxima.get(mag, 1))
            r = simulate(states, labels, start, inv, maxima)
            if r:
                runs[row] = r
        heard = sorted({s["sound"] for r in runs.values() for s in r["sounds"]})
        weapons.append({"name": a["name"], "file": a["file"], "tag": a["props"].get("tag", ""),
                        "pocket_ammo": pocket, "pocket_max": maxima.get(pocket), "magazine": mag,
                        "magazine_size": maxima.get(mag), "runs": runs,
                        "sprites": sorted({f["sprite"][:4] for r in runs.values() for f in r["frames"]}),
                        "sounds": {s: sounds.get(s.lower(), "") for s in heard}})
    return weapons


def shot_text(r):
    out = []
    for s in r["shots"]:
        if "bullets" in s:
            out.append(f"{s['bullets']} x {s['damage']}")
        elif "projectile" in s and not COSMETIC.search(s["projectile"]):
            out.append(s["projectile"])
        elif "projectile" not in s:
            out.append(", ".join(f"{k} {v}" for k, v in s.items() if k != "tic"))
    return "; ".join(out) or "-"


def write_md(weapons, path):
    lines = ["# Brutal Doom weapons: the numbers", "",
             f"Read from the mod's own weapon files by `tools/weapon_sheet.py`, playing each one forward at "
             f"{TICS_PER_SECOND} tics a second on the plain path (a normal, not Tactical, player class; nobody "
             "pressing anything). All of it "
             "is `[inferred-static]` until timed in the game. Damage is bullets x damage per bullet as written; "
             "Brutal Doom's bullet puffs can add more on hit. Every frame and sound with its exact tic is in "
             "`weapons.json`.", ""]
    for w in sorted(weapons, key=lambda x: x["name"].lower()):
        mag = f"{w['magazine']} holds {w['magazine_size']}" if w["magazine"] else "no magazine"
        lines += [f"## {w['name']}  ({w['tag'] or w['file']})", "",
                  f"- Ammo: {w['pocket_ammo'] or '-'} (carry up to {w['pocket_max']}); {mag}",
                  f"- Sprites: {', '.join(w['sprites']) or '-'}", "",
                  "| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |",
                  "| --- | --- | --- | --- | --- | --- |"]
        for row, r in w["runs"].items():
            snd = ", ".join(f"{s['sound']} @{s['tic']:g}" for s in r["sounds"][:8]) or "-"
            if len(r["sounds"]) > 8:
                snd += f" (+{len(r['sounds']) - 8})"
            lines.append(f"| {row} | {r['tics']:g} | {r['seconds']} | {shot_text(r)} | {snd} | {r['ends']} |")
        lines += ["", "Sound files: " + (", ".join(f"`{k}` {v or '?'}" for k, v in w["sounds"].items()) or "-"), ""]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    root, out = argv
    weapons = sheet(root)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "weapons.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(weapons, f, indent=1)
    write_md(weapons, os.path.join(out, "WEAPONS.md"))
    print(f"{len(weapons)} weapons -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
