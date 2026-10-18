# Brutal Doom cube machine gun: every number and colour in one place.
# Tefa, 2026-10-18, with two pictures (a red and grey DOOM-style heavy rifle with a top box sight, a belt drum and a
# slotted muzzle brake; and a black sci-fi heavy MG with a long shroud and side tube, a box magazine and a skeleton
# stock): "make a mash of these two, keep the red tones, but make it look like dried blood stains on the machine gun
# all over". So: the black MG's long layout and box magazine, the red gun's chunky receiver, box sight, ammo window
# and muzzle brake, grey panels from the red gun. The blood was tried and dropped (Tefa: "the blood stains dont fit,
# please just use the dark red colours from the picture"): the red is the picture's worn dark red paint instead, on
# the grip, box sight, stock sides, handguard and front block, its edges worn lighter. The blood code is in git history.
# Voxel axes, as in every cubekit gun: x = rear -> muzzle, y = width (+ = the gun's LEFT side), z = up.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CUBEKIT = os.path.abspath(os.path.join(HERE, "..", "..", "blender-cubekit"))   # the framework, cloned beside this repo
sys.path.insert(0, CUBEKIT)
from cube_size import VOXEL_M     # ONE cube size for every cube model (3.4 mm), set in blender-cubekit/cube_size.py

ROUND_SLACK = 0.3                 # a cube is inside a circle when its distance squared is under r * r plus this
PIVOT = (71, 0.5, 0)              # the top of the pistol grip, where the right hand holds it

# ---- the receiver: a chunky box, its upper part a cube narrower ----
RECEIVER = dict(x0=56, x1=165, y=7, z0=0, z1=28, bevel=2, upper_z=22, upper_y=6)
RAIL = dict(x0=60, x1=162, y=3, z0=29, z1=30, slot_step=4)           # a rail along the top, slotted
# ---- the stock: in line with the receiver, its underside dropping to the butt, a skeleton window with two rods ----
STOCK = dict(x0=0, x1=55, y=6, top=26, bottom=[(0, -8), (40, 3), (55, 3)], bevel=1)
STOCK_WINDOW = dict(x0=14, x1=42, z0=6, z1=18, rods=(9, 15), rod_r=1.2)
BUTT = dict(x1=1, y=7)                                                # the rubber butt plate
# ---- pistol grip, raked back, ridged sides ----
GRIP = dict(z0=-30, z1=-1, front=78, back=64, rake=0.3, y=5, ridge_step=3, ridge_inset=2)
GUARD = dict(x1=100, z_bottom=-12, y=2, lean=3)
TRIGGER = [(85, -1), (84, -2), (84, -3), (84, -4), (85, -5), (85, -6), (86, -7)]
# ---- the box magazine under the receiver, with a carry strap on each side ----
MAG = dict(x0=102, x1=132, y=8, z0=-34, z1=-1, lean=3, bevel=1)
MAG_STRAP = dict(x0=108, x1=126, z0=-26, z1=-6, y=9)
# ---- the box sight on top: look through its tunnel at the front post (for VR aiming) ----
BOX_SIGHT = dict(x0=96, x1=124, y=5, z0=29, z1=38, tunnel_y=2, tunnel_z=(33, 36))
# ---- the ammo window on the right side, brass rounds showing through, framed in caution yellow ----
AMMO_WINDOW = dict(x0=130, x1=152, z0=10, z1=22, y_in=-4, rounds=range(132, 151, 3), round_w=2, round_z=(12, 20))
CHARGE = dict(x0=139, x1=142, z0=22, z1=25, y0=8, y1=10)             # the charging handle on the left side
# ---- the front: a slotted handguard under a long shroud with a side tube, then a bulky block ----
HANDGUARD = dict(x0=166, x1=239, y=6, z0=0, z1=12, bevel=1, slots=range(172, 234, 9), slot_len=4, slot_z=(4, 7))
SHROUD = dict(x0=166, x1=239, y=6, z0=13, z1=28, bevel=2, top_slots=range(170, 236, 6), top_slot_len=3, top_slot_y=3)
SIDE_TUBE = dict(x0=168, x1=238, y=7, zc=17, r=1.7)                   # a tube along each side of the shroud
FRONT_BLOCK = dict(x0=240, x1=262, y=7, z0=4, z1=28, bevel=2, slashes=(246, 250, 254), slash_z=(18, 23), lean=2)
BARREL = dict(x0=160, x1=288, zc=18, r=3.0)
BRAKE = dict(x0=289, x1=306, y=5, z0=13, z1=23, bevel=2, slots=((292, 294), (298, 300)), slot_z=(15, 21), bore=2.0)
FRONT_SIGHT = dict(x0=252, x1=253, y=1, z1=34, ears_y=4, ears_z1=33, ears_x=(251, 254))   # its top in the middle of
                                                                                     # BOX_SIGHT's tunnel

# ---- fine detail with the kit's smallest cubes (0.85 mm), the shotgun's and pistol's way ----
FINE_LINES = [   # cut one small cube deep: (part, side, y, [(x, z) corners, joined])
    ('body', 'both', 7, [(60, 6.5), (125, 6.5), (130, 2.5), (164, 2.5)]),
    ('body', 'both', 7, [(118, 6), (121, 12)]), ('body', 'both', 7, [(122, 6), (125, 12)]),   # the red gun's ////
    ('body', 'both', 7, [(126, 6), (129, 12)]), ('body', 'both', 7, [(156, 6), (159, 12)]),
    ('body', 'both', 6, [(168, 24.5), (238, 24.5)]),
]
FINE_SCREWS = [  # raised screw heads with a slot: (part, side, y, [(x, z) centres])
    ('body', 'both', 7, [(60, 3), (60, 19), (162, 3), (162, 19)]),
    ('body', 'both', 7, [(243, 7), (243, 25), (259, 7), (259, 25)]),
    ('mag', 'both', 8, [(105, -4), (129, -4)]),
]
FINE_STAMPS = [  # raised marks: (part, side, y, x, z_top, pattern, dot, colour)
    ('body', 'both', 6, 228, 27, ("#....", "###..", "#####", "###..", "#...."), 2, 'red'),    # the black MG's
    ('body', 'both', 7, 82, 20, ("#.#.#.#.#.#", ".#.#.#.#.#."), 2, 'caution'),               # red markers; hazard
]
FINE_COL = dict(line=(6, 6, 7), screw=(52, 54, 58), red=(150, 20, 16), caution=(196, 150, 36))

WEAR = dict(seed=1066, scratch_per_cm2=0.04, scratch_mm=(8.0, 32.0), along_share=0.75, gouge_share=0.1,
            zigzag_share=0.35)
SCRATCH_LIGHTEN = 1.4

# ---- colours, sRGB 0-255 ----
COL = dict(
    metal=(22, 23, 26),
    metal_hi=(48, 50, 55),
    metal_mid=(34, 35, 39),
    metal_dark=(12, 12, 13),
    panel=(62, 64, 68),           # the red gun's grey parts (lighter read near white)
    panel_dark=(44, 46, 50),
    rubber=(12, 12, 13),
    port=(9, 9, 10),
    bore=(4, 4, 4),
    brass=(170, 130, 60),
    brass_hi=(206, 166, 86),
    caution=(196, 150, 36),
    sight_dot=(235, 235, 228),
    red=(104, 30, 28),            # the picture's dark red paint
    red_hi=(138, 52, 46),         # its worn edges
    red_dark=(72, 20, 18),
)
EDGE_WEAR = 0.6                  # how far a worn edge goes toward its colour's _hi
EDGE_HI = dict(metal='metal_hi', red='red_hi')   # the colours whose long edges wear

SHADE = {(0, 0, 1): 1.12, (0, 0, -1): 0.55, (0, 1, 0): 0.88, (0, -1, 0): 0.88,
         (1, 0, 0): 0.74, (-1, 0, 0): 0.74}
NOISE = 0.05
