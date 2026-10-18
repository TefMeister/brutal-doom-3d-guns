# Brutal Doom cube pistol: every number and colour in one place.
# Tefa, 2026-10-18 (with a picture of the DOOM (2016) pistol): "then the pistol to look like this ... the pistol, lose
# the blue glowing parts and the round hammer at the back, lets see what comes out of that, these normal looking
# weapons are too boring in a doom game fighting demons on another planet". So: the picture's boxy slide with its
# squared nose and round bore, the angular frame with the ring module under the front, a shaped black grip and the tang
# reaching back over the hand; the glowing parts become plain copper and dark metal, and there is no hammer.
# The beefed-up Beretta 92F block-out before it is in git history.
# Voxel axes, as in every cubekit gun: x = rear -> muzzle, y = width (+ = the gun's LEFT side), z = up.
# The grip is laid out like the Ashes 2063 pistol's (top at z 28, same rake), so that gun's glove pose fits it later.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CUBEKIT = os.path.abspath(os.path.join(HERE, "..", "..", "blender-cubekit"))   # the framework, cloned beside this repo
sys.path.insert(0, CUBEKIT)
from cube_size import VOXEL_M     # ONE cube size for every cube model (3.4 mm), set in blender-cubekit/cube_size.py

PIVOT = (10, 0.5, 28)             # the top of the grip, the same point as the Ashes pistol's

# ---- the grip: raked back like the Ashes pistol's, a palm swell at the back, a flared base ----
GRIP = dict(z0=3, z1=28, front=19, back=2, rake=0.2, y=6, swell=2, belly=1)  # front/back x at the top; y half-width;
                                                                              # swell/belly = bulge at back/front
GRIP_TEXTURE = dict(inset=2, z0=7, z1=24)          # stippled rubber on both sides, `inset` cubes in from the edges
MAG_BASE = dict(z0=0, z1=2, over=1, y=7)           # the magazine's flared base plate
TANG = dict(x0=-9, z0=29, z1=31, y=4, droop=0.25)  # the tang reaching back over the web of the hand, its end drooping

# ---- the frame under the slide, the trigger guard and the ring module under the front ----
FRAME = dict(x0=0, x1=56, y=5, z0=28, z1=31)
GUARD = dict(x1=36, z_bottom=17, y=2, lean=3)      # bottom bar from the grip's front to x1; its front post leans back
TRIGGER = [(28, 27), (27, 26), (27, 25), (27, 24), (28, 23), (28, 22), (29, 21)]
MODULE = dict(x0=37, x1=56, y=5, z0=19, z1=27, lean=3, bevel=1)   # the box under the front, its nose leaning back
RING = dict(x=46, z=23, r_out=4.4, r_in=2.4, y=6)                 # the round coil on each side: plain metal, no glow
RAIL = dict(x0=40, x1=55, z=19, slots=(43, 47, 51))               # slots along the module's underside

# ---- the slide: a wide lower band and a narrower upper deck, a squared nose, a window showing the copper barrel ----
SLIDE = dict(x0=-4, x1=60, y=5, z0=32, z1=44, bevel=1)
DECK = dict(z0=40, y=4, x1=53)                     # above z0 the slide is narrower, back to the nose at x1
REAR_SLOPE = dict(x1=1, drop=3)                    # the slide's back end slopes down `drop` cubes towards x0
WINDOW = dict(x0=20, x1=40, y=3, z0=40)            # the ejection window on top, deep enough to show the barrel
SERRATIONS = dict(x0=0, x1=10, step=2, z0=33, z1=38)   # grip grooves at the back of the lower band, both sides
REAR_SIGHT = dict(x0=-1, x1=3, y=4, z1=47, notch=1)
FRONT_SIGHT = dict(x0=55, x1=56, z1=46)
BARREL = dict(x0=10, x1=60, zc=39, r=3.0)          # copper, under the window
MUZZLE = dict(x0=61, x1=63, r=3.2, bore=1.6)       # the round barrel end standing out of the squared nose

# ---- fine detail with the kit's smallest cubes (0.85 mm): bd_pistol_fine.py, the shotgun's way (shotgun/bd_fine.py) ----
# In cubes, quarters allowed: (part, side, y, ...): y = how far out the face is; side 'both' mirrors it.
FINE_LINES = [   # cut one small cube deep: (part, side, y, [(x, z) corners, joined])
    ('slide', 'both', 5, [(12, 34.5), (43, 34.5), (48, 38.5), (53, 38.5)]),   # an angled panel line on the lower band
    ('slide', 'both', 5, [(45, 33.5), (47, 38)]),                          # the picture's "//" near the nose
    ('slide', 'both', 5, [(47.5, 33.5), (49.5, 38)]),
    ('frame', 'both', 5, [(1, 29.5), (36, 29.5)]),                          # along the frame
    ('frame', 'both', 5, [(38, 20.25), (54, 20.25)]),                       # along the module's bottom
]
FINE_SCREWS = [  # raised screw heads with a slot: (part, side, y, [(x, z) centres])
    ('frame', 'both', 5, [(4, 29.5), (33, 29.5), (53, 25)]),
    ('slide', 'both', 5, [(57.5, 35)]),
]
FINE_STAMPS = [  # raised marks: (part, side, y, x, z_top, pattern, dot, colour); '#' = a dot of dot x dot small cubes
    ('slide', 'both', 4, 4, 43, ("#..#..", ".#..#.", "..#..#", ".#..#.", "#..#.."), 1, 'red'),   # the red ">>"
    ('slide', 'both', 5, 14, 38.75, ("...#...", "..#.#..", "..#.#..", ".#.#.#.", ".#...#.", "#..#..#",
                                     "#.....#", "#######"), 1, 'white'),                         # a warning triangle
]
FINE_COL = dict(line=(8, 8, 9), screw=(70, 72, 78), red=(176, 24, 20), white=(200, 200, 194))

# Carved scratches, as on the shotgun and the gloves: shorter, the pistol being small; a fraction lighter inside.
WEAR = dict(seed=668, scratch_per_cm2=0.06, scratch_mm=(6.0, 22.0), along_share=0.75, gouge_share=0.1,
            zigzag_share=0.35)
SCRATCH_LIGHTEN = 1.4

# ---- colours, sRGB 0-255: black like the shotgun's metal, copper where the picture glows ----
COL = dict(
    metal=(26, 26, 28),
    metal_hi=(52, 53, 57),        # worn edges, the ring
    metal_mid=(38, 39, 43),       # the upper deck, a touch lighter, like the picture's slide
    metal_dark=(14, 14, 15),
    copper=(132, 74, 44),
    copper_hi=(170, 102, 62),
    bore=(4, 4, 4),
    port=(9, 9, 10),
    grip=(20, 20, 22),
    grip_check=(32, 32, 35),
    sight_dot=(235, 235, 228),
)
EDGE_WEAR = 0.6                  # how far a worn metal edge goes toward metal_hi

SHADE = {(0, 0, 1): 1.12, (0, 0, -1): 0.55, (0, 1, 0): 0.88, (0, -1, 0): 0.88,
         (1, 0, 0): 0.74, (-1, 0, 0): 0.74}
NOISE = 0.05
