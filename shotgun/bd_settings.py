# Brutal Doom cube shotgun: every number and colour in one place.
# Shape: Brutal Doom's own pickup picture of its shotgun (side view, 64 x 15 pixels), traced at 1 picture pixel =
# 4.73 cubes, scaled so its stock wrist sits in the Ashes 2063 shotgun's right hand and its wooden pump in the left
# (Tefa, 2026-10-18: the Ashes shotgun is the size to compare against; the real size is judged in VR).
# Cubes like the Ashes guns, and a STRAIGHT pump, not turned on its side (Tefa, 2026-10-18).
# Voxel axes, as in every cubekit gun: x = rear -> muzzle, y = width (+ = the gun's LEFT side), z = up.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CUBEKIT = os.path.abspath(os.path.join(HERE, "..", "..", "blender-cubekit"))   # the framework, cloned beside this repo
sys.path.insert(0, CUBEKIT)
from cube_size import VOXEL_M     # ONE cube size for every cube model (3.4 mm), set in blender-cubekit/cube_size.py

PIVOT = (6, 0.5, -12)             # the same grip point as the Ashes shotgun, so its hands fit this gun unchanged
# The Ashes right hand held a pistol grip; this gun has a stock wrist instead, higher and further back, so the hand
# moves by this many cubes (x back, z up) from where the Ashes gun had it (2026-10-18, Tefa: "the right hand moved
# accordingly"). Until our own Doomguy hands exist, the Ashes hand copied into this file is moved.
RIGHT_HAND_MOVE = (-12, 0, 14)

# ---- the stock, in cubes: (x, z) points along its top and bottom edges, joined by straight lines ----
# Rebuilt 2026-10-18 after Tefa's first look: "way too low down". Now its top runs level with the top of the gun, as
# in Tefa's reference picture (a blocky shotgun found online), with a deep wrist dip and a tall, beefy butt.
STOCK_X = (-93, -1)                                     # butt to wrist (~31 cm)
STOCK_TOP = [(-93, 9), (-40, 13), (-14, 15), (-1, 15)]  # nearly level with the gun's top, dropping a little to the butt
STOCK_BOTTOM = [(-93, -33), (-88, -36), (-75, -33), (-50, -28), (-34, -22), (-22, -14), (-10, -9), (-1, -6)]
STOCK_HALF_WIDTH = (7, 5)                               # half-width at the butt, at the wrist (~5 cm down to ~3.5 cm)
BUTT_PAD = 3                                            # black rubber pad on the butt end, cubes thick
GRAIN_STEP = 5                                          # a grain line every this many cubes up the stock
GRAIN_WAVE = (2.0, 9.0)                                 # how far a grain line wanders, and over how many cubes

# ---- colours, sRGB 0-255 ----
# Tefa, 2026-10-18: nearly black metal, DARK OAK wood, "almost unrealistically beefy, dangerous and cool".
COL = dict(
    wood=(58, 37, 23),           # dark oak
    wood_hi=(76, 50, 31),        # worn top edges
    wood_grain=(40, 25, 15),
    wood_dark=(36, 23, 14),      # lower stock
    butt_pad=(18, 18, 19),
)

# per-face shade painted into the colour (not lighting), the same as the Ashes guns
SHADE = {(0, 0, 1): 1.12, (0, 0, -1): 0.55, (0, 1, 0): 0.88, (0, -1, 0): 0.88,
         (1, 0, 0): 0.74, (-1, 0, 0): 0.74}
NOISE = 0.05                      # per-cube brightness wobble
