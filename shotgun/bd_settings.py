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
# The Ashes right hand is moved by this many cubes (x forward, z up) from where it held the Ashes gun's grip, onto this
# gun's grip. Until our own Doomguy hands exist, the Ashes hand copied into this file is moved.
RIGHT_HAND_MOVE = (-4, 0, -9)

# ---- the grip, in cubes: dark oak, in place of the wooden stock ----
# Tefa, 2026-10-18: "please lose the stock and make the handle dark oak instead". The DOOM (2016) gun's pistol grip,
# raked like the Ashes shotgun's so the same right hand fits it. The stock is in git history.
GRIP = dict(front=13, back=-3, z0=-37, z1=-7, rake=0.38, y=5, cap=2)   # front/back x at the top, leaning back `rake`
                                                                       # per cube going down; `cap` = metal base plate
GRAIN_STEP = 4                                          # a grain line every this many cubes down the grip
GRAIN_WAVE = (1.0, 4.0)                                 # how far a grain line wanders, and over how many cubes
# The short metal end behind the grip, where the stock was: the picture's stubby rear with its end plate.
REAR_STUB = dict(x0=-20, x1=-1, y=6, top=[(-20, 9), (-1, 15)], bottom=[(-20, -13), (-8, -9), (-1, -6)], plate=2)

# ---- the metal and the pump, in cubes: the DOOM (2016) combat shotgun's shape round our dark oak stock and pump ----
# Tefa, 2026-10-18 (with a picture of it): "we make a mash of the old and new weapons. keep the dark oak parts and
# remodel the gun to look like the new one ... mirror the side you don't see as much as possible and add the shell exit
# hole". The picture shows the gun's LEFT side; the right side mirrors it, plus the ejection port.
# The square-bodied first metal (2026-10-18) is in git history.
RECEIVER = dict(x0=0, x1=100, y=7, z0=-8, z1=17, bevel=1)     # ~34 cm long, ~8.5 cm tall, ~5 cm wide
REAR_STEP = dict(x1=9, z0=-6, z1=15)                          # its rear end matches the stock's wrist
NOSE_CHAMFER = dict(x0=84, rise=2)                            # the underside rises 1 cube every `rise` towards the front
SIDE_PLATE = dict(x0=14, x1=88, y=8, z0=-5, z1=13, slant=10)  # an armour plate one cube proud on each side; its
                                                              # front and rear edges lean back by `slant` going up
SPINE = dict(x0=24, x1=100, y=4, z0=18, z1=19, notch_step=4)  # notched rail along the top
REAR_SIGHT = dict(x0=64, x1=70, y=4, z0=20, z1=28, hole_z=(23, 25), hole_y=1)   # tall peep sight, square frame
TOP_BLOCK = dict(x0=88, x1=100, y=6, z0=18, z1=22)          # the block the barrel leaves the receiver through
PORT = dict(x0=42, x1=64, z0=3, z1=12, y_in=-2)               # ejection port, RIGHT side, cut in to y_in
SHELL = dict(x0=47, x1=60, y=-4, zc=7, r=2.4, head=2)         # a red shell lying in the open port, brass head
LOADING_PORT = dict(x0=22, x1=58, y=3, depth=2)               # slot on the underside
TRIGGER_PLATE = dict(x0=10, x1=48, y=5, z0=-10, z1=-9)        # the frame stepping down round the trigger
GUARD = dict(x0=14, x1=44, z_bottom=-19, y=1, lean=4)         # angular guard, its front leaning back `lean` going down
TRIGGER = [(28, -11), (28, -12), (27, -13), (27, -14), (27, -15), (28, -16)]

LOWER_BLOCK = dict(x0=46, x1=74, y=6, z0=-12, z1=-9, lean=3)  # angular block ahead of the guard, front leaning back

# The front half, top to bottom as in the picture: the round barrel with a rod either side, a long flat housing, then
# the boxy pump round the magazine tube; all of it ending in a big muzzle block. Made heavier after the first look,
# where the front half came out much thinner than the picture's.
BARREL = dict(x0=100, x1=218, zc=15, r=4.2)                   # round and polished, ~40 cm
BARREL_SHINE = 1                                              # a lighter line along the barrel's top, this many cubes
                                                              # either side of its middle, so it reads round
BARREL_RING = dict(x0=101, x1=103, r=4.8)                     # the brass ring where it leaves the receiver
RODS = dict(x0=103, x1=187, y=6, z=17)                        # thin rods beside the barrel, both sides
HOUSING = dict(x0=100, x1=187, y=8, z0=2, z1=10, holes=12, hole_z=6,   # long flat box under the barrel, bolt holes
               slot=dict(x0=112, x1=170, z0=4, z1=8))                 # and a long recessed slot along each side
MAGTUBE = dict(x0=100, x1=212, zc=-2, r=4.0)
# The second look (2026-10-18): next to the picture the pump was a slim bar; the picture's is a tall box, as deep as the
# housing above it, with a raised rim round a sunken panel. Still dark oak.
PUMP = dict(x0=108, x1=172, y=9, z0=-17, z1=1, round_r=6, inset=dict(x0=116, x1=164, z0=-13, z1=-2), end_bevel=2)
ACTION_BARS = dict(x0=90, y=8, z=-4)                          # from the pump back into the receiver
FRONT_MODULE = dict(x0=174, x1=187, y=6, z0=-12, z1=1, slots=(177, 179, 181, 183), slot_z=(-9, -1))
SHROUD = dict(x0=188, x1=218, y=9, z0=0, z1=24, bevel=2)      # the big muzzle block, upper part
SHROUD_LOW = dict(x0=188, x1=213, y=8, z0=-11, z1=-1, bevel=1)  # its lower part, round the magazine tube's end
SHROUD_PANEL = dict(x0=193, x1=213, z0=4, z1=20)              # recessed panel on both sides
MUZZLE = dict(x0=219, x1=221, r=5.2, bore=3.2)                # the barrel's ring proud of the block's front
MAG_MUZZLE = dict(x0=214, x1=215, r=4.6, bore=3.0)            # the lower hole: the magazine tube's open end
FRONT_SIGHT = dict(x0=212, x1=214, ears=2, z0=25, z1=27)

# ---- fine detail, cut with the kit's smallest cubes (0.85 mm, a quarter cube) into the metal: bd_fine.py ----
# Tefa, 2026-10-18: "this is where you can really utilize the different cube size combinations for finer details and
# still keep the pixelated look". All in cubes (halves and quarters allowed): x along the gun, z up, on a side face whose
# distance from the middle is `y`; a cut that lands more than one cube deeper than `y` (in a port, a slot) is skipped.
# side: 'both' (mirrored, as Tefa asked: "mirror the side you don't see as much as possible"), 'left' or 'right'.
FINE_LINES = [   # panel lines: (side, y, [(x, z) corners, joined]), one small cube deep
    ('both', 7, [(10, 14.5), (99, 14.5)]),                                   # receiver, under the spine
    ('both', 7, [(10, -6.5), (83, -6.5)]),                                   # receiver, along the bottom
    ('both', 8, [(19, -3), (83, -3), (75, 11), (27, 11), (19, -3)]),         # an inner panel on each armour plate
    ('right', 8, [(40.25, 1.5), (65.75, 1.5), (65.75, 13.5), (40.25, 13.5), (40.25, 1.5)]),  # round the shell port
    ('both', 6, [(-17, 7), (-9, 0), (-17, -7)]),                             # a chevron on the rear end
    ('both', 8, [(189, -5), (212, -5)]),                                     # the muzzle block's lower part
    ('both', 9, [(189, 2), (217, 2)]),                                       # the muzzle block, under its panel
]
# Tefa, 2026-10-18: "you can also use small cubes to build not just carve". So the screws stand proud, and there are
# raised trims and the picture's little white arrow marks.
FINE_SCREWS = [  # raised screw heads: (side, y, [(x, z) centres]); a ring of small cubes round an empty middle
    ('both', 8, [(22, -1), (80, -1), (72, 9), (30, 9)]),                     # the armour plates' corners
    ('both', 9, [(190.5, 22), (216, 22), (190.5, 0.5), (216, 0.5)]),         # the muzzle block's corners
    ('both', 6, [(94, 20)]),                                                 # the top block
    ('both', 6, [(-13, 9), (-13, -6)]),                                      # the rear end
]
FINE_VENTS = dict(side='both', y=8, x0=196, x1=210, z=(6, 9, 12, 15, 18), depth=2)   # slots in the muzzle panel
FINE_TRIMS = [   # raised strips one small cube proud: (side, y, [(x, z) corners, joined])
    ('both', 6, [(89, 21.5), (99, 21.5)]),                                   # the top block's upper edge
    ('both', 8, [(103, 10.5), (186, 10.5)]),                                 # the housing's top edge
    ('both', 6, [(176, 1.5), (186, 1.5)]),                                   # over the front module's slots
]
FINE_MARKS = [   # little raised arrow marks, white like the picture's: (side, y, x, z, points down?)
    ('both', 7, 92, 13, True),
    ('both', 8, 32, 5, False),
]
FINE_COL = dict(line=(8, 8, 9), screw=(70, 72, 78), vent=(5, 5, 5), trim=(56, 58, 63), mark=(190, 190, 184))

# ---- colours, sRGB 0-255 ----
# Tefa, 2026-10-18: nearly black metal, DARK OAK wood, "almost unrealistically beefy, dangerous and cool".
COL = dict(
    wood=(58, 37, 23),           # dark oak
    wood_hi=(76, 50, 31),        # worn edges
    wood_grain=(40, 25, 15),
    wood_dark=(36, 23, 14),      # the bottom of a wooden part
    metal=(26, 26, 28),          # nearly black
    metal_hi=(52, 53, 57),       # worn edges
    metal_dark=(14, 14, 15),
    bore=(4, 4, 4),
    port=(9, 9, 10),
    sight=(150, 140, 110),
    metal_mid=(36, 37, 41),      # the raised armour plates, a touch lighter than the body
    polish=(46, 48, 53),         # the polished barrel and rods, dark like the picture's
    polish_hi=(84, 88, 96),      # the shine along the barrel's top
    brass=(160, 120, 50),
    shell=(140, 26, 22),         # Brutal Doom's red shells
    shell_brass=(176, 136, 58),
)
EDGE_WEAR = 0.6                  # how far a worn metal edge goes toward metal_hi

# ---- the look pass (2026-10-18, Tefa: combat scratches, dried blood, a chipped bit showing iron) ----
# Scratches: painted streaks could not be seen, and grooves one whole cube deep "look like a broken weapon" (Tefa,
# 2026-10-18), so they are carved with the kit's smallest cubes (0.85 mm) instead: bd_wear.py.
# Metal only for now: no chips or pits yet (the chip showing iron is its own step), the wood left alone.
# Tefa, 2026-10-18, on the first fine pass: "fewer, longer -- some lihtning strike shaped and darker, just a little
# brighter than the gun".
WEAR = dict(seed=666, scratch_per_cm2=0.05, scratch_mm=(12.0, 40.0), along_share=0.75, gouge_share=0.1,
            zigzag_share=0.35)
# Inside a cut: a fraction lighter than what it is cut into, as on the gloves (Tefa, 2026-10-18: "make the scratches on
# the gun follow the same brightness what you applied to the glove scratches"; a fixed (46, 47, 51) before).
SCRATCH_LIGHTEN = 1.4

# per-face shade painted into the colour (not lighting), the same as the Ashes guns
SHADE = {(0, 0, 1): 1.12, (0, 0, -1): 0.55, (0, 1, 0): 0.88, (0, -1, 0): 0.88,
         (1, 0, 0): 0.74, (-1, 0, 0): 0.74}
NOISE = 0.05                      # per-cube brightness wobble
