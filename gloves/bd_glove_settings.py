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
CUFF_L, CUFF_W = 9, 20              # cubes of cuff below the wrist, and its width

# ---- the under-glove: brown leather over the whole hand, fingers and thumb included ----
CREASE = 1                          # a darker line this many cubes long at each finger joint
TIP_ROUND = 2                       # the last cubes of a finger lose their side edges: a rounded glove tip

# ---- colours, sRGB 0-255, picked from the reference picture ----
COL = dict(
    under=(92, 54, 34),             # brown leather
    under_dark=(62, 36, 23),        # creases at the joints, the palm's lines
    under_hi=(120, 74, 47),         # worn ridges (knuckles)
    seam=(40, 24, 16),              # stitching where the cuff joins
)
SHADE = {(0, 0, 1): 1.12, (0, 0, -1): 0.62, (0, 1, 0): 0.88, (0, -1, 0): 0.88,
         (1, 0, 0): 0.78, (-1, 0, 0): 0.78}
NOISE = 0.04

SHOW_AT = (0.30, 0.10, 0.0)         # Blender metres: where the glove sits, beside the shotgun, while it is shaped
