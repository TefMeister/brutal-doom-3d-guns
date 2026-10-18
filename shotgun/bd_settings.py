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

# ---- the metal and the pump, in cubes (2026-10-18, Tefa: "more square tones ... make the tip of the muzzle round but
# the barrel leading up to it bulky and square") ----
RECEIVER = dict(x0=0, x1=96, y=6, z0=-8, z1=18, bevel=1)      # ~33 cm long, ~9 cm tall, ~4 cm wide
PORT = dict(x0=30, x1=54, z0=8, z1=14)                        # ejection port, on the right side (as in the Ashes gun)
BOLTS = dict(start=4, end_gap=3, step=23, z=3)                # big square bolt heads along the receiver's lower sides
BARREL = dict(x0=96, x1=204, y=4, z0=10, z1=18)               # square and bulky, ~37 cm
MUZZLE = dict(x0=205, x1=214, zc=14, r=4.6, bore=2.0)         # the round tip
RIB = dict(z=19, y=1, notch_step=6)                           # the vent rib along the barrel's top
SIGHT = dict(x0=209, x1=211, z1=21)                           # front sight blade
MAGTUBE = dict(x0=96, x1=184, y=4, z0=0, z1=8)                # square magazine tube under the barrel
MAGCAP = dict(x0=185, x1=191, y=5, z0=-1, z1=9)
CLAMP = dict(x0=176, x1=182, y=5, z0=-1, z1=19)               # band holding barrel and magazine together
PUMP = dict(x0=118, x1=168, y=7, z0=-5, z1=10, groove_step=3, end_bevel=2)   # beefy square dark-oak fore-end
ACTION_BARS = dict(y=5, z=3)                                  # from the pump back into the receiver
GUARD = dict(x0=12, x1=40, z_bottom=-17, y=1)                 # square trigger guard
TRIGGER = [(26, -9), (26, -10), (25, -11), (25, -12), (26, -13)]

# ---- colours, sRGB 0-255 ----
# Tefa, 2026-10-18: nearly black metal, DARK OAK wood, "almost unrealistically beefy, dangerous and cool".
COL = dict(
    wood=(58, 37, 23),           # dark oak
    wood_hi=(76, 50, 31),        # worn top edges
    wood_grain=(40, 25, 15),
    wood_dark=(36, 23, 14),      # lower stock
    butt_pad=(18, 18, 19),
    metal=(26, 26, 28),          # nearly black
    metal_hi=(52, 53, 57),       # worn edges
    metal_dark=(14, 14, 15),
    bore=(4, 4, 4),
    port=(9, 9, 10),
    sight=(150, 140, 110),
)
EDGE_WEAR = 0.6                  # how far a worn metal edge goes toward metal_hi

# ---- the look pass (2026-10-18, Tefa: combat scratches, dried blood, a chipped bit showing iron) ----
# Scratches: short bright streaks scraped into the metal's outer sides and top, a few cubes long, some slanted.
SCRATCHES = dict(count=26, length=(3, 9), seed=666)
COL['scratch'] = (92, 94, 99)    # bare steel showing through the black finish

# per-face shade painted into the colour (not lighting), the same as the Ashes guns
SHADE = {(0, 0, 1): 1.12, (0, 0, -1): 0.55, (0, 1, 0): 0.88, (0, -1, 0): 0.88,
         (1, 0, 0): 0.74, (-1, 0, 0): 0.74}
NOISE = 0.05                      # per-cube brightness wobble
