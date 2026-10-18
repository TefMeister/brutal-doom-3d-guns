# Brutal Doom cube pistol: every number and colour in one place.
# A beefed-up Beretta 92F (Tefa, 2026-10-18): the 92's open-topped slide showing the barrel, its squared trigger
# guard, a raked grip, an exposed hammer, all chunkier than the real gun. Black like Brutal Doom's own pistol.
# Built one step at a time with Tefa: this block-out first.
# Voxel axes, as in every cubekit gun: x = rear -> muzzle, y = width (+ = the gun's LEFT side), z = up.
# The grip is laid out like the Ashes 2063 pistol's (top at z 28, same rake), so that gun's glove pose fits it later.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CUBEKIT = os.path.abspath(os.path.join(HERE, "..", "..", "blender-cubekit"))   # the framework, cloned beside this repo
sys.path.insert(0, CUBEKIT)
from cube_size import VOXEL_M     # ONE cube size for every cube model (3.4 mm), set in blender-cubekit/cube_size.py

PIVOT = (10, 0.5, 28)             # the top of the grip, the same point as the Ashes pistol's

# ---- the grip: front and back edges lean back going down (the Ashes pistol's rake), a little fatter ----
GRIP = dict(z0=3, z1=28, front=19, back=2, rake=0.2, y=6, round=1)   # front/back x at the top; y = half-width
GRIP_PANEL = dict(inset=2, z0=6, z1=25, check=2)    # checkered panels on both sides, `inset` cubes in from the edges
MAG_BASE = dict(z0=1, z1=2, over=1)                 # the magazine's base plate, `over` cubes past the grip all round

# ---- the frame under the slide, and the trigger guard (the 92F's squared front with a small hook) ----
FRAME = dict(x0=0, x1=56, y=5, z0=28, z1=31)
GUARD = dict(x1=41, z_bottom=17, y=2, hook=1)      # from the grip's front to x1, bar 2 thick; hook = lip at its front
TRIGGER = [(28, 27), (27, 26), (27, 25), (27, 24), (27, 23), (28, 22), (28, 21), (29, 20)]
SLIDE_CATCH = dict(x0=22, x1=30, z=32)             # lever on the left side, just above the frame
TAKEDOWN = dict(x0=34, x1=37, z=30)                # takedown lever on the left side

# ---- the slide: beefy, open on top over the barrel, closed round the muzzle ----
SLIDE = dict(x0=-2, x1=58, y=6, z0=32, z1=44, bevel=1)        # ~20 cm long, ~4.4 cm wide
# the 92's cut: open on top, its sides dipping low enough that the barrel shows from the side too (its trademark look)
OPEN_TOP = dict(x0=22, x1=52, y=4, z0=40, dip_x0=25, dip_x1=49, dip_z0=39)
SERRATIONS = dict(x0=1, x1=11, step=2, z0=34, z1=41)          # grip grooves at the back of the slide, both sides
REAR_SIGHT = dict(x0=0, x1=3, y=4, z1=46, notch=1)
FRONT_SIGHT = dict(x0=54, x1=55, z1=47)
SAFETY = dict(x0=3, x1=8, z0=41, z1=42)                       # ambidextrous safety/decocker levers, both sides
BARREL = dict(x0=18, x1=59, zc=38, r=3.6, bore=1.6)

# ---- the hammer, behind the slide ----
HAMMER = dict(x0=-6, x1=-3, y=2, z0=34, z1=42)

# ---- colours, sRGB 0-255: black like the shotgun's metal ----
COL = dict(
    metal=(26, 26, 28),
    metal_hi=(52, 53, 57),        # worn edges, levers
    metal_dark=(14, 14, 15),
    barrel=(78, 80, 86),          # lighter, so it reads through the open top
    bore=(4, 4, 4),
    grip=(20, 20, 22),
    grip_check=(36, 36, 38),
    sight_dot=(235, 235, 228),
)
EDGE_WEAR = 0.6                  # how far a worn metal edge goes toward metal_hi

SHADE = {(0, 0, 1): 1.12, (0, 0, -1): 0.55, (0, 1, 0): 0.88, (0, -1, 0): 0.88,
         (1, 0, 0): 0.74, (-1, 0, 0): 0.74}
NOISE = 0.05
