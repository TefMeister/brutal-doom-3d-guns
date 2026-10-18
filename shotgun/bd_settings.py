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

# ---- the stock, in cubes: (x, z) points along its top and bottom edges, joined by straight lines ----
STOCK_X = (-93, -1)                                     # butt to wrist (~31 cm)
STOCK_TOP = [(-93, -2), (-86, 3), (-37, 3), (-29, -2), (-23, -6), (-1, -6)]          # comb, then down into the wrist
STOCK_BOTTOM = [(-93, -30), (-89, -36), (-83, -44), (-70, -40), (-50, -35), (-31, -30), (-18, -25), (-1, -25)]
STOCK_HALF_WIDTH = (6, 4)                               # half-width at the butt, at the wrist (~4 cm down to ~3 cm)
BUTT_PAD = 3                                            # black rubber pad on the butt end, cubes thick
GRAIN_STEP = 5                                          # a grain line every this many cubes up the stock
GRAIN_WAVE = (2.0, 9.0)                                 # how far a grain line wanders, and over how many cubes

# ---- colours, sRGB 0-255 (sampled from the Brutal Doom picture, in brackets) ----
COL = dict(
    wood=(101, 67, 45),          # [65432d]
    wood_hi=(109, 72, 49),       # worn top edges [6d4831]
    wood_grain=(82, 58, 36),     # [523a24]
    wood_dark=(70, 53, 32),      # lower stock [463520]
    butt_pad=(24, 24, 24),       # [181818]
)

# per-face shade painted into the colour (not lighting), the same as the Ashes guns
SHADE = {(0, 0, 1): 1.12, (0, 0, -1): 0.55, (0, 1, 0): 0.88, (0, -1, 0): 0.88,
         (1, 0, 0): 0.74, (-1, 0, 0): 0.74}
NOISE = 0.05                      # per-cube brightness wobble
