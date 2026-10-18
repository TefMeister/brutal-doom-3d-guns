# Doomguy's armoured gloves: every number and colour in one place.
# Tefa's reference picture (2026-10-18, kept in the local refs folder, never on GitHub): a full-finger glove, brown
# leather underneath, dark blue-grey steel plates over every finger joint, the knuckles and the back of the hand, and a
# bulky armoured cuff. Built one step at a time with Tefa: the brown under-glove first, then the plates, then the cuff.
#
# HAND SPACE, as in the Ashes gloves: lay the RIGHT hand flat on a table, palm down, fingers pointing away from you.
#   x = across the hand (+x to your right; the thumb sits at -x), y = wrist -> fingertips, z = up (back of the hand).
#   The left hand is the mirror (x -> -x).
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CUBEKIT = os.path.abspath(os.path.join(HERE, "..", "..", "blender-cubekit"))   # the framework, cloned beside this repo
sys.path.insert(0, CUBEKIT)
from cube_size import VOXEL_M     # ONE cube size for every cube model (3.4 mm), set in blender-cubekit/cube_size.py

# ---- the hand's shape: the Ashes gloves' approved hand (2026-09-23), in cubes ----
PALM_W, PALM_L, PALM_T = 26, 27, 8
PALM_CORNER = 4                     # rounding at the wrist corners and knuckle corners
DOME = 2                            # the back of the hand rises this much in the middle
EDGE_ROUND = 2                      # cubes shaved off the palm's long edges, top and bottom
TAPER = 1                           # the palm gets this much thinner towards the knuckles and the wrist
# (name, centre x for the RIGHT hand, knuckle y, length in cubes)
FINGERS = [("index", -9, 26, 22), ("middle", -3, 27, 24), ("ring", 3, 26, 23), ("pinky", 9, 23, 18)]
FINGER_W, FINGER_T = 5, 5
CURL = (14, 26, 16)                 # relaxed curl, degrees down at each of the three joints
SPLAY = {"index": -1, "middle": 0, "ring": 0, "pinky": 1}
THUMB_BASE = (-11, 8, -1)           # where it leaves the palm (right hand)
THUMB_W, THUMB_T = 7, 6
THUMB_SEGS = [(14, 56, 6), (12, 30, 24)]   # (length, degrees outward from +y, degrees down)


# ---- the under-glove: leather over the whole hand (blue-green since 2026-10-18, see COL), fingers and thumb included ----
CREASE = 1                          # a darker line this many cubes long at each finger joint
TIP_ROUND = 2                       # the last cubes of a finger lose their side edges: a rounded glove tip

# ---- the steel plates (step 2; the under-glove approved by Tefa 2026-10-18: "looks about right to me") ----
# Each finger and thumb segment gets its own plate: its top row and upper sides turned to steel, plus one raised row,
# with the under-glove left bare at every joint so the plates read as separate pieces, as in the picture.
# Tefa, 2026-10-18, on the first plates: "little bit bulkier please" -> one cube thicker, overhanging the fingers'
# sides, and a bigger back plate.
PLATE_GAP = 1                       # bare under-glove steps at each joint, between two plates
PLATE_RAISE = 2                     # cubes a plate stands above the glove
PLATE_OVERHANG = 1                  # cubes a finger plate reaches past each side of the finger
KNUCKLE_PLATE = dict(y0=PALM_L - 4, y1=PALM_L + 1, half_w=2, raise_=PLATE_RAISE)   # over each finger's knuckle
BACK_PLATE = dict(x0=-11, x1=12, y0=3, y1=21, corner=3, raise_=PLATE_RAISE)        # the big plate on the back
BACK_PLATE_TOP = dict(x0=-5, x1=6, y0=8, y1=16, corner=2, raise_=1)                # a smaller one stacked on it
RIVETS = [(-9, 5), (10, 5), (-9, 19), (10, 19)]                    # bright bolt heads at the big plate's corners
# Tefa, 2026-10-18, on the bulkier plates: "thats good, now needs other parts to be dark green too". Which plates are
# dark green (the rest stay steel): 'knuckle', 'back', 'back_top', 'finger'.
# Then: "please have fingers have steel only on the knucle and joint parts, but the rest green" -> finger and thumb
# plates green, a narrower steel band over every finger joint, knuckle plates steel.
GREEN_PLATES = ('back', 'back_top', 'finger')
JOINT_RAISE = 1                     # a joint's steel band stands this far above the glove, lower than the plates

# ---- the armoured cuff (step 3; the plates approved by Tefa 2026-10-18: "thats good!") ----
# A chunky green bracer over the wrist, wider and taller than the hand, two steel bands round it, a raised panel on top.
ARMOUR_CUFF = dict(y0=-14, y1=-1, half_w=12, thick=12, corner=3)
CUFF_BANDS = (-13, -12, -3, -2)     # rows that are steel bands
CUFF_PANEL = dict(x0=-6, x1=6, y0=-10, y1=-5, corner=1, raise_=1)
CUFF_RIVETS = [(-9, -7), (9, -7)]

# ---- colours, sRGB 0-255, picked from the reference picture ----
COL = dict(
    steel=(58, 66, 74),             # dark blue-grey steel
    steel_dark=(34, 38, 44),        # plate sides and undersides
    steel_hi=(104, 112, 122),       # the leading edge of each plate, catching the light
    rivet=(140, 146, 152),
    green=(50, 66, 38),             # dark green armour
    green_dark=(30, 40, 23),
    green_hi=(76, 96, 56),
    # The cuff, bluer than the plates (Tefa, 2026-10-18: "a bit bluer green please", "sorry i meant only the cuff
    # bit", then "just a bit bluer and colour the rest of the brown like that too"): the under-glove, brown until
    # then, takes the cuff's colour as well.
    cuff=(38, 62, 64),
    cuff_dark=(22, 38, 40),
    cuff_hi=(60, 92, 94),
    under=(38, 62, 64),             # the under-glove, the cuff's colour
    under_dark=(24, 40, 42),        # creases at the joints, the palm's lines, the cuff's lining
    under_hi=(54, 84, 86),          # worn ridges (knuckles)
)
SHADE = {(0, 0, 1): 1.12, (0, 0, -1): 0.62, (0, 1, 0): 0.88, (0, -1, 0): 0.88,
         (1, 0, 0): 0.78, (-1, 0, 0): 0.78}
NOISE = 0.04

SHOW_AT = (0.30, 0.10, 0.0)         # Blender metres: where the glove sits, beside the shotgun, while it is shaped
