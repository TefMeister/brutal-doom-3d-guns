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

ROUND_SLACK = 0.3                 # a cube is inside a circle when its distance squared is under r * r plus this,
                                  # the same rounding as the kit's tubes (parts.py)
PIVOT = (10, 0.5, 28)             # the top of the grip, the same point as the Ashes pistol's

# ---- HAND CANNON (Tefa, 2026-10-18: "yes go over the top to make it into a hand cannon") ----
# Everything below was made bigger after the first look: a taller, wider slide, a heavy compensator with ports on the
# nose, windows down the slide showing the copper barrel, a bigger frame and ring module, a fatter grip.

# ---- the grip: raked back like the Ashes pistol's, a palm swell at the back, a flared base ----
GRIP = dict(z0=2, z1=28, front=20, back=1, rake=0.2, y=7, swell=2, belly=1)  # front/back x at the top; y half-width;
                                                                              # swell/belly = bulge at back/front
GRIP_TEXTURE = dict(inset=2, z0=7, z1=24)          # stippled rubber on both sides, `inset` cubes in from the edges
# Tefa, 2026-10-18: "that handle could use a silver plate with a millitary logo in the middle". A silver plate one cube
# proud on each side, and on it a dark military star in a ring (bd_pistol_fine.py, LOGO).
GRIP_PLATE = dict(inset=2, z0=6, z1=24, corner=2)
MAG_BASE = dict(z0=-1, z1=1, over=1, y=8)          # the magazine's flared base plate
TANG = dict(x0=-11, z0=29, z1=32, y=5, droop=0.25)  # the tang reaching back over the web of the hand, its end drooping

# ---- the frame under the slide, the trigger guard and the ring module under the front ----
FRAME = dict(x0=0, x1=62, y=6, z0=28, z1=32)
GUARD = dict(x1=38, z_bottom=15, y=2, lean=3)      # bottom bar from the grip's front to x1; its front post leans back
TRIGGER = [(30, 27), (29, 26), (29, 25), (29, 24), (29, 23), (30, 22), (30, 21), (31, 20)]
MODULE = dict(x0=39, x1=62, y=6, z0=17, z1=27, lean=3, bevel=1)   # the box under the front, its nose leaning back
RING = dict(x=50, z=22, r_out=5.5, r_in=3.0, y=7)                 # the round coil on each side: plain metal, no glow
RAIL = dict(x0=42, x1=61, z=17, slots=(45, 49, 53, 57))           # slots along the module's underside

# ---- the slide: a wide lower band and a narrower upper deck, windows showing the copper barrel ----
SLIDE = dict(x0=-6, x1=64, y=6, z0=33, z1=49, bevel=1)
DECK = dict(z0=44, y=5, x1=64)                     # above z0 the slide is narrower, all the way to the compensator
REAR_SLOPE = dict(x1=0, drop=4)                    # the slide's back end slopes down `drop` cubes towards x0
WINDOW = dict(x0=18, x1=46, y=4, z0=44)            # the ejection window on top, deep enough to show the barrel
SIDE_WINDOWS = dict(x=(20, 30, 40), length=6, z0=44, z1=47)   # windows down the deck's sides, onto the barrel
SERRATIONS = dict(x0=-3, x1=10, step=2, z0=35, z1=42)  # grip grooves at the back of the lower band, both sides
REAR_SIGHT = dict(x0=-5, x1=0, y=5, z1=52, notch=1)
BARREL = dict(x0=8, x1=64, zc=41, r=4.0)           # copper, under the windows; it stops at the compensator, so
                                                   # the bore through that is dark metal, not copper
# The compensator: a heavy block on the nose, ports cut into its top and sides, the bore through its front.
COMP = dict(x0=65, x1=75, y=6, z0=34, z1=50, bevel=2, top_ports=(67, 70, 73), port_w=2, port_depth=3,
            side_ports=dict(x0=67, x1=73, z0=43, z1=45, depth=2))
FRONT_SIGHT = dict(x0=72, x1=73, z1=53)
MUZZLE = dict(x0=76, x1=77, r=4.4, bore=2.6)       # a ring round the bore, proud of the compensator's front

# ---- fine detail with the kit's smallest cubes (0.85 mm): bd_pistol_fine.py, the shotgun's way (shotgun/bd_fine.py) ----
# In cubes, quarters allowed: (part, side, y, ...): y = how far out the face is; side 'both' mirrors it.
FINE_LINES = [   # cut one small cube deep: (part, side, y, [(x, z) corners, joined])
    ('slide', 'both', 6, [(12, 37.5), (48, 37.5), (54, 42.5), (63, 42.5)]),   # an angled panel line on the lower band
    ('slide', 'both', 6, [(52, 35), (54.5, 41)]),                          # the picture's "//" near the nose
    ('slide', 'both', 6, [(55.5, 35), (58, 41)]),
    ('slide', 'both', 6, [(66, 40), (74, 40)]),                            # round the compensator
    ('frame', 'both', 6, [(1, 30.5), (38, 30.5)]),                          # along the frame
    ('frame', 'both', 6, [(40, 18.25), (60, 18.25)]),                       # along the module's bottom
]
FINE_SCREWS = [  # raised screw heads with a slot: (part, side, y, [(x, z) centres])
    ('frame', 'both', 6, [(4, 30.5), (35, 30.5), (59, 24)]),
    ('slide', 'both', 6, [(66.5, 36.5), (73.5, 36.5), (66.5, 47.5), (73.5, 47.5)]),
]
FINE_STAMPS = [  # raised marks: (part, side, y, x, z_top, pattern, dot, colour); '#' = a dot of dot x dot small cubes
    ('slide', 'both', 5, 2, 48, ("#..#..", ".#..#.", "..#..#", ".#..#.", "#..#.."), 2, 'red'),   # the red ">>"
    ('slide', 'both', 6, 14, 42.5, ("...#...", "..#.#..", "..#.#..", ".#.#.#.", ".#...#.", "#..#..#",
                                    "#.....#", "#######"), 1, 'white'),                          # a warning triangle
]
# The military star in a ring on each grip plate: centred on the plate, in cubes.
LOGO = dict(z=15, ring_r=4.75, ring_w=0.75, star_r=3.75, star_in=1.5, height=2)
FINE_COL = dict(line=(8, 8, 9), screw=(70, 72, 78), red=(176, 24, 20), white=(200, 200, 194),
                ring=(30, 30, 33), star=(30, 30, 33))   # dark on the silver: a pale star did not show

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
    silver=(160, 163, 170),       # the grip plates
    silver_hi=(205, 208, 214),
    silver_dark=(104, 106, 112),
    sight_dot=(235, 235, 228),
)
EDGE_WEAR = 0.6                  # how far a worn metal edge goes toward metal_hi

SHADE = {(0, 0, 1): 1.12, (0, 0, -1): 0.55, (0, 1, 0): 0.88, (0, -1, 0): 0.88,
         (1, 0, 0): 0.74, (-1, 0, 0): 0.74}
NOISE = 0.05
