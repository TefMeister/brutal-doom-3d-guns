# Which sprites a weapon shows in the player's hand, read from its DECORATE source, by state label. No Blender.
#   from weapon_sprites import sprites_by_label
# Spawn is the weapon lying in the world: a MODELDEF entry for its sprite would draw the hand-held model, hand
# offsets and all, on the floor, so those sprites are kept apart (2026-10-24, the forge guns going into the games).
import re

STATE = re.compile(r"\s*\"?([A-Z0-9_#]{4})\"?\s+\"?([A-Z\[\]\#^]+)\"?\s+-?\d")
LABEL = re.compile(r"\s*([A-Za-z0-9_.]+)\s*:(?!:)")


def actor_text(source, cls):
    """The text of one actor (DECORATE `actor cls ...` or ZScript `class cls ...`), comments taken out."""
    t = re.sub(r"//[^\n]*", "", source)
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
    parts = re.split(r"(?im)^\s*(?:actor|class)\s+", t)[1:]
    for p in parts:
        if re.match(re.escape(cls) + r"(\s|:|$|\{)", p, re.I):
            return p
    return None


def frames_by_label(source, cls):
    """{label: set of (sprite, letter)} for one weapon; TNT1 (nothing drawn) left out."""
    p = actor_text(source, cls)
    if p is None:
        return {}
    i = p.lower().find("states")
    label, out = None, {}
    for line in p[i:].splitlines():
        if not STATE.match(line):
            m = LABEL.match(line)
            if m and m.group(1).lower() not in ("goto", "loop", "stop", "wait", "fail"):
                label = m.group(1)
        for m in STATE.finditer(line):
            if m.group(1) != "TNT1":
                out.setdefault(label, set()).update((m.group(1), L) for L in m.group(2))
    return out


def sprites_by_label(source, cls):
    """{label: set of sprite names}."""
    return {k: {s for s, _ in v} for k, v in frames_by_label(source, cls).items()}


def hand_frames(source, cls, foreign=()):
    """The (sprite, letter) frames shown in the hand: every label but Spawn, less the frames Spawn also uses, less
    sprites in `foreign` (another weapon's, borrowed for a kick, a throw or a switch) and '####' / PLAY."""
    by = frames_by_label(source, cls)
    world = set().union(*([v for k, v in by.items() if k and k.lower() == "spawn"] or [set()]))
    held = set().union(*([v for k, v in by.items() if not k or k.lower() != "spawn"] or [set()]))
    drop = set(foreign) | {"####", "PLAY"}
    return sorted(f for f in held - world if f[0] not in drop)
