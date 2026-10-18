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

# ---- the hand's size ----
# Tefa, 2026-10-18: "we need to make hands bigger". Every length below is the approved hand's, times HAND_SCALE, so the
# shapes and colours Tefa approved stay as they were, only bigger.
HAND_SCALE = 1.25


def sc(v):
    """A length of the approved hand, at HAND_SCALE."""
    return int(round(v * HAND_SCALE))


# ---- the hand's shape: the Ashes gloves' approved hand (2026-09-23), in cubes ----
PALM_W, PALM_L, PALM_T = sc(26), sc(27), sc(8)
PALM_CORNER = sc(4)                 # rounding at the wrist corners and knuckle corners
DOME = sc(2)                        # the back of the hand rises this much in the middle
EDGE_ROUND = sc(2)                  # cubes shaved off the palm's long edges, top and bottom
TAPER = 1                           # the palm gets this much thinner towards the knuckles and the wrist
THUMB_PAD = dict(y0=1, y1=sc(15), yc=sc(8), ry=sc(7), reach=sc(5))   # the pad of the thumb, low and wide
PALM_LINES = dict(x=sc(4), y0=sc(3), y1=PALM_L - sc(4))             # the palm's lines
# (name, centre x for the RIGHT hand, knuckle y, length in cubes); the centres picked by hand, not scaled, so the
# wider fingers keep one cube between them
FINGERS = [("index", -10, sc(26), sc(22)), ("middle", -3, sc(27), sc(24)), ("ring", 4, sc(26), sc(23)),
           ("pinky", 11, sc(23), sc(18))]
FINGER_W, FINGER_T = 6, 6
CURL = (14, 26, 16)                 # relaxed curl, degrees down at each of the three joints
SPLAY = {"index": -1, "middle": 0, "ring": 0, "pinky": 1}
THUMB_BASE = (sc(-11), sc(8), -1)   # where it leaves the palm (right hand)
THUMB_W, THUMB_T = sc(7), sc(6)
THUMB_SEGS = [(sc(14), 56, 6), (sc(12), 30, 24)]   # (length, degrees outward from +y, degrees down)


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
KNUCKLE_PLATE = dict(y0=PALM_L - sc(4), y1=PALM_L + 1, half_w=2, raise_=PLATE_RAISE)   # over each finger's knuckle
BACK_PLATE = dict(x0=sc(-11), x1=sc(12), y0=sc(3), y1=sc(21), corner=sc(3), raise_=PLATE_RAISE)   # the big plate
BACK_PLATE_TOP = dict(x0=sc(-5), x1=sc(6), y0=sc(8), y1=sc(16), corner=2, raise_=1)   # a smaller one stacked on it
RIVETS = [(sc(-9), sc(5)), (sc(10), sc(5)), (sc(-9), sc(19)), (sc(10), sc(19))]   # bolt heads at the big plate's corners
# Tefa, 2026-10-18, on the bulkier plates: "thats good, now needs other parts to be dark green too". Which plates are
# dark green (the rest stay steel): 'knuckle', 'back', 'back_top', 'finger'.
# Then: "please have fingers have steel only on the knucle and joint parts, but the rest green" -> finger and thumb
# plates green, a narrower steel band over every finger joint, knuckle plates steel.
GREEN_PLATES = ('back', 'back_top', 'finger')
JOINT_RAISE = 1                     # a joint's steel band stands this far above the glove, lower than the plates

# ---- the armoured cuff (step 3; the plates approved by Tefa 2026-10-18: "thats good!") ----
# A chunky green bracer over the wrist, wider and taller than the hand, two steel bands round it, a raised panel on top.
ARMOUR_CUFF = dict(y0=sc(-14), y1=-1, half_w=sc(12), thick=sc(12), corner=sc(3))
CUFF_BANDS = (sc(-14) + 1, sc(-14) + 2, -3, -2)   # rows that are steel bands
CUFF_PANEL = dict(x0=sc(-6), x1=sc(6), y0=sc(-10), y1=sc(-5), corner=1, raise_=1)
CUFF_RIVETS = [(sc(-9), sc(-7)), (sc(9), sc(-7))]

# ---- leather (Tefa, 2026-10-18: "maybe add some leather") ----
# Brown leather on the palm side (where the hand holds the gun), and a strap round the cuff, next to its band at the
# open end, fastened with a steel buckle beside the cuff's raised panel.
LEATHER_PALM = True
STRAP = dict(y0=ARMOUR_CUFF['y0'] + 3, y1=ARMOUR_CUFF['y0'] + 4)      # the rows the strap covers; it stands one proud
BUCKLE = dict(x0=CUFF_PANEL['x1'] + 1, x1=CUFF_PANEL['x1'] + 5, y0=STRAP['y0'] - 1, y1=STRAP['y1'] + 1)   # steel frame

# ---- colours, sRGB 0-255, picked from the reference picture ----
COL = dict(
    steel=(58, 66, 74),             # dark blue-grey steel
    steel_dark=(34, 38, 44),        # plate sides and undersides
    steel_hi=(104, 112, 122),       # the leading edge of each plate, catching the light
    rivet=(140, 146, 152),
    gunmetal=(26, 26, 28),          # the cuff's bands: the shotgun's own metal (Tefa, 2026-10-18: "the steel on the
    gunmetal_hi=(52, 53, 57),       # cuffs needs to be like gun metal colour"), its worn-edge colour on top
    green=(50, 66, 38),             # dark green armour
    green_dark=(30, 40, 23),
    green_hi=(76, 96, 56),
    # The cuff, bluer than the plates (Tefa, 2026-10-18: "a bit bluer green please", "sorry i meant only the cuff
    # bit", then "just a bit bluer and colour the rest of the brown like that too"): the under-glove, brown until
    # then, takes the cuff's colour as well. Then: "that looks wrong, can you make it even darker green, than the top
    # plate?" -> both a dark green, darker than the plates; then "even darker by 60%", then "doo dark now" -> about
    # two thirds of the dark green, between the two.
    cuff=(20, 28, 17),
    cuff_dark=(12, 17, 10),
    cuff_hi=(29, 40, 25),
    under=(20, 28, 17),             # the under-glove, the cuff's colour
    under_dark=(12, 17, 10),        # creases at the joints, the palm's lines, the cuff's lining
    under_hi=(28, 38, 24),          # worn ridges (knuckles)
    leather=(66, 40, 22),           # brown leather: the palm, the strap
    leather_dark=(44, 26, 14),
    leather_hi=(92, 60, 34),        # worn edges
)
# ---- fine detail with the kit's smallest cubes (0.85 mm): bd_glove_fine.py ----
# Tefa, 2026-10-18: "decorate them more with smaller cubes ... and the raised slayer sign to the left glove plate".
# In hand space (the right hand; the left gets the mirror), in cubes, quarters allowed. Built ones stand proud of the
# surface below them, cut ones go one small cube in.
SLAYER_MARK = dict(x=0.5, y=BACK_PLATE['y0'] + 2.25, height=2, colour='mark')   # the LEFT back plate only: the mark's
                                                                              # middle-bottom (x, y); `height` small cubes
PLATE_GROOVE = 1.5            # an engraved line this far inside the back plate's edge
KNUCKLE_STUD = dict(size=2, height=2)   # a raised square stud, in small cubes, on every knuckle plate
STITCH = dict(step=2, colour='stitch')  # stitch dots along both edges of the strap, every `step` small cubes
CUFF_VENTS = dict(n=3, gap=1.0, colour='under_dark')   # short grooves across the cuff's raised panel
FINE_COL = dict(mark=(176, 22, 18), stitch=(150, 118, 76), groove=(10, 14, 9), stud=(120, 128, 138))

SHADE = {(0, 0, 1): 1.12, (0, 0, -1): 0.62, (0, 1, 0): 0.88, (0, -1, 0): 0.88,
         (1, 0, 0): 0.78, (-1, 0, 0): 0.78}
NOISE = 0.04

# Carved scratches, as on the shotgun (Tefa, 2026-10-18: "gloves need to have carved scratches too"): the kit's
# smallest cubes dug out, steel showing in the cut. Shorter than the gun's, the plates being small.
WEAR = dict(seed=667, scratch_per_cm2=0.08, scratch_mm=(5.0, 18.0), along_share=0.6, gouge_share=0.1,
            zigzag_share=0.35)
# Inside a cut: a fraction lighter than what it is cut into (Tefa, 2026-10-18: "carved scrathces need to be a fraction
# lighter colour than what they are on"; steel in every cut was the first try).
SCRATCH_LIGHTEN = 1.4

# ---- on the shotgun (Tefa, 2026-10-18: "please now swap the hands over") ----
# The Ashes shotgun hands' poses (ashes-2063-weapons vs_hands.py, 2026-09-24), in this gun's cube space.
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "shotgun")))
from bd_settings import RIGHT_HAND_MOVE, PUMP as GUN_PUMP     # where the Ashes right hand was moved to; the pump
RIGHT_POSE = dict(
    x0=-11, y0=-10, z0=-13,         # where hand space lands (the Ashes grip's front top, its right side)
    grip_top=-1, rake=0.38,         # the hand leans back with the Ashes grip below this height
    curls={"middle": (45, 55, 60), "ring": (45, 55, 60), "pinky": (40, 50, 50), "index": (10, 35, 30)},
    thumb=[(sc(12), 5, 80), (sc(10), -30, 20)],
    shift=RIGHT_HAND_MOVE,          # onto this gun's grip
)
LEFT_POSE = dict(
    x0=116, y0=19,                  # the Ashes pump's middle; the knuckle line just off the pump's right side
    z0=GUN_PUMP['z0'] - 1 - PALM_T // 2,   # the palm's face (half the palm below hand-space 0) just under this pump
    left_edge=GUN_PUMP['y'] + 1, wrist_drop=0.7,   # past the pump's left side the wrist drops 1 cube in 1.4
    curls={"index": (65, 50, 20), "middle": (65, 50, 20), "ring": (65, 50, 20), "pinky": (60, 45, 15)},
    thumb=[(sc(11), 88, 22), (sc(11), 80, 60)], thumb_base=(sc(-11), sc(12), -1), thumb_size=(sc(9), sc(7)),
    shift=(26, 0, 0),               # forward to the pump's place on this gun (the Ashes LEFT_SHIFT)
)       # Blender metres: where the glove sits, beside the shotgun, while it is shaped
