# The guns' animations, as poses per Brutal Doom sprite frame (2026-10-19).
#
# Tefa 2026-10-19: "doom games, please animate the shooting animations, pump after each shotgun shot, but not the
# reloads, we'll not include reloading guns, only the initial weapon pick up animation we must animate too", then
# "please do all the animations without me and we'll look at them all together later and tweak what we have to then".
# So: Fire (and the shotgun's pump after each shot), the raise, and the FIRST pick-up (Brutal Doom's
# FirstSelectAnimation / Tacticalselect); no reloads. Everything here is a first pass to be tweaked together.
#
# How it reaches the game: GZDoom picks a model frame per sprite frame (MODELDEF FrameIndex), so the animation is
# stepped exactly like Brutal Doom's sprites, with the same timing. Each gun is split into SLOTS (separate MD3s drawn
# together): the body (frame, right glove, ...) and the one moving part (pump + left glove, slide, charging handle).
# A slot gets one MD3 frame per distinct pose it takes, so a 300,000-vertex body is only stored a few times.
#
# A pose moves the whole gun about the grip (the right glove's middle): BACK (metres, along the barrel), UP (metres),
# PITCH (degrees, + = muzzle up), ROLL (degrees, + = the top tilts right), YAW (degrees, + = muzzle to the left).
# A moving part also slides TRAVEL (0..1) of its stroke along its axis, inside the posed gun.
# Which frame shows what was read from Brutal Doom v22 test 6's DECORATE and sprites (refs sheets, 2026-10-19).
import math

POSES = {   # name: (back, up, pitch, roll, yaw)
    "rest": (0.0, 0.0, 0.0, 0.0, 0.0),
    # the kick of a shot, strongest first
    "k3": (0.022, 0.004, 7.0, 0.0, 0.0),
    "k2": (0.013, 0.002, 4.5, 0.0, 0.0),
    "k1": (0.005, 0.001, 2.0, 0.0, 0.0),
    # the raise: from muzzle-down and low, up to aim
    "r1": (0.0, -0.06, -40.0, 0.0, 0.0),
    "r2": (0.0, -0.035, -25.0, 0.0, 0.0),
    "r3": (0.0, -0.012, -10.0, 0.0, 0.0),
    # pistol first pick-up: tipped up and turned in to look it over (PISR), the side (PISI E-H), the front (PISI I-N)
    "t1": (0.0, 0.005, 10.0, -8.0, 0.0),
    "t2": (0.0, 0.010, 20.0, -15.0, 0.0),
    "t3": (0.0, 0.015, 30.0, -22.0, 0.0),
    "t4": (0.0, 0.020, 35.0, -25.0, 0.0),
    "side": (0.0, 0.020, 35.0, -50.0, 0.0),
    "front": (0.0, 0.015, 20.0, -10.0, 30.0),
    # machine gun first pick-up: raised canted on its side (3IFR), held canted (RIFR), turned back level (2IFR)
    "c1": (0.0, -0.05, -40.0, -40.0, 0.0),
    "c2": (0.0, -0.03, -25.0, -40.0, 0.0),
    "c3": (0.0, -0.01, -10.0, -40.0, 0.0),
    "c4": (0.0, 0.0, 0.0, -40.0, 0.0),
    "c5": (0.0, 0.0, 0.0, -30.0, 0.0),
    "c6": (0.0, 0.0, 0.0, -20.0, 0.0),
    "c7": (0.0, 0.0, 0.0, -12.0, 0.0),
    "c8": (0.0, 0.0, 0.0, -6.0, 0.0),
}


def table(*rows):
    """rows: (sprite, letters, pose, travel). Later rows win."""
    out = {}
    for spr, lets, pose, travel in rows:
        for L in lets:
            out[(spr, L)] = (pose, travel)
    return out


GUNS = {
    "shotgun": {
        "slots": [("body", ["BD_body", "BD_trigger", "BD_glove_right"]),
                  ("pump", ["BD_pump", "BD_glove_left"])],
        "axis": (0.0, -1.0, 0.0), "stroke": 0.085,   # the pump comes back about 8.5 cm
        "frames": table(
            # Fire: SHTA A B (flash) C D E W, then the 6-tic hold on SHTN A; after the pump SHTA F G H I
            ("SHTA", "AB", "k3", 0), ("SHTA", "C", "k2", 0), ("SHTA", "DE", "k1", 0),
            # the raise (SHTA M L K J), also the first three frames of the first pick-up
            ("SHTA", "M", "r1", 0), ("SHTA", "L", "r2", 0), ("SHTA", "K", "r3", 0),
            # the pump (Pump1 / Pump2 and the first pick-up): H = Pump1 sound (back), N then Pump2 sound (home)
            ("SHTN", "H", "rest", 0.55), ("SHTN", "I", "rest", 0.9), ("SHTN", "J", "rest", 1.0),
            ("SHTN", "K", "rest", 0.8), ("SHTN", "L", "rest", 0.55), ("SHTN", "M", "rest", 0.3),
            ("SHTN", "N", "rest", 0.1),
        ),
        # for the preview blend: Brutal Doom's own order and tics
        "sequences": {
            "fire": [("SHTA", "ABCDEW"), ("SHTN", "AAAAAAA" "ABCDEFG" "HIJKLMN" "PQFEDCB"), ("SHTA", "FGHI")],
            "first_pickup": [("SHTA", "MLK"), ("SHTN", "BCDEFG" "H" "IJJKKLLLLLMMN" "PQRGGGFFEDCBA")],
            "raise": [("SHTA", "MLKJ")],
        },
    },
    "pistol": {
        "slots": [("body", ["BDP_frame", "BDP_barrel", "BDP_cover", "BDP_heat", "BDP_mag", "BDP_trigger", "BDP_glove_right"]),
                  ("slide", ["BDP_slide"])],
        "axis": (0.0, -1.0, 0.0), "stroke": 0.05,
        "frames": table(
            # Fire: PIST A (shot) B C D E; E is also the gun at rest
            ("PIST", "A", "k3", 1.0), ("PIST", "B", "k2", 0.6), ("PIST", "C", "k1", 0.25),
            # the raise: PISS A B C (loaded) and G H I (empty)
            ("PISS", "AG", "r1", 0), ("PISS", "BH", "r2", 0), ("PISS", "CI", "r3", 0),
            # first pick-up: PISR A-D tip it up, E-T hold (the magazine check of the sprites is left out), P-S rack
            ("PISR", "A", "t1", 0), ("PISR", "B", "t2", 0), ("PISR", "C", "t3", 0),
            ("PISR", "DEFGHIJKLMNOTUVW", "t4", 0),
            ("PISR", "P", "t4", 0.5), ("PISR", "QR", "t4", 1.0), ("PISR", "S", "t4", 0.4),
            # ... then PISI: the side (E-H), the front (I-N), lowered (O P), racked by the left hand (Q-S), back (T U)
            ("PISI", "EFGH", "side", 0), ("PISI", "IJKLMN", "front", 0), ("PISI", "OP", "t2", 0),
            ("PISI", "Q", "t2", 0.5), ("PISI", "RS", "t2", 1.0), ("PISI", "T", "t1", 0.3), ("PISI", "U", "t1", 0),
        ),
        "sequences": {
            "fire": [("PIST", "ABCDEEEEEEE")],
            "first_pickup": [("PISS", "ABC"), ("PISR", "ABCDEFGG" "HIJKKLLL" "MNO" "PQRSTTT"),
                             ("PISI", "QRSTUU" "EE" "FG" "HHHH" "IJKLLL" "MMNOP"), ("PISR", "BA")],
            "raise": [("PISS", "ABC")],
        },
    },
    "machinegun": {
        "slots": [("body", ["BDM_body", "BDM_mag", "BDM_trigger", "BDM_glove_right", "BDM_glove_left"]),
                  ("charge", ["BDM_charge"])],
        "axis": (0.0, -1.0, 0.0), "stroke": 0.06,
        "frames": table(
            # Fire: RIFF A (shot) B C, D = the other shot frame
            ("RIFF", "AD", "k2", 0), ("RIFF", "B", "k1", 0),
            # the raise: RIFG I H G F
            ("RIFG", "I", "r1", 0), ("RIFG", "H", "r2", 0), ("RIFG", "G", "r3", 0),
            # first pick-up: 3IFR A-F raised on its side, RIFR held there while the charging handle is pulled (R-V),
            # 2IFR turned back level
            ("3IFR", "A", "c1", 0), ("3IFR", "BC", "c2", 0), ("3IFR", "DE", "c3", 0), ("3IFR", "F", "c4", 0),
            ("RIFR", "GHIJKLMNOPQWXYZ[B", "c4", 0),
            ("RIFR", "R", "c4", 0.5), ("RIFR", "ST", "c4", 1.0), ("RIFR", "U", "c4", 0.6), ("RIFR", "V", "c4", 0.2),
            ("2IFR", "ABCDEFGH", "c4", 0), ("2IFR", "I", "c5", 0), ("2IFR", "J", "c6", 0), ("2IFR", "K", "c7", 0),
            ("2IFR", "L", "c8", 0),
        ),
        "sequences": {
            "fire": [("RIFF", "ABC" "ABC" "ABC"), ("RIFG", "A")],
            "first_pickup": [("3IFR", "ABCDEF"), ("RIFR", "GGH" "H" "IJKLMNNO" "OONPQRSTUU" "VVVWXYZ" "[" "B"),
                             ("2IFR", "ABCDEFG" "HHH" "IJJJ" "KKLMNOP")],
            "raise": [("RIFG", "IHGF")],
        },
    },
}


def pose_of(gun, sprite, letter):
    """(pose name, travel) for one sprite frame; anything not listed is the gun at rest."""
    return GUNS[gun]["frames"].get((sprite, letter), ("rest", 0.0))


def _rot(axis, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    if axis == "x":
        return [[1, 0, 0], [0, c, -s], [0, s, c]]
    if axis == "y":
        return [[c, 0, s], [0, 1, 0], [-s, 0, c]]
    return [[c, -s, 0], [s, c, 0], [0, 0, 1]]


def _mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def pose_transform(gun, pose, travel, pivot, slot_index):
    """(R, t): a point p of slot `slot_index` (in the gun root's space, metres) goes to R @ p + t.
    Blender space: +Y along the barrel, +Z up, +X right. Pitch turns +Y towards +Z (muzzle up)."""
    back, up, pitch, roll, yaw = POSES[pose]
    R = _mul(_rot("z", yaw), _mul(_rot("x", pitch), _rot("y", roll)))
    g = GUNS[gun]
    slide = [c * g["stroke"] * travel for c in g["axis"]] if slot_index > 0 else [0.0, 0.0, 0.0]
    # p -> R @ (p + slide - pivot) + pivot + (0, -back, up)
    q = [slide[i] - pivot[i] for i in range(3)]
    Rq = [sum(R[i][k] * q[k] for k in range(3)) for i in range(3)]
    t = [Rq[i] + pivot[i] + (0.0, -back, up)[i] for i in range(3)]
    return R, t
