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
GRIP = dict(z0=-12, z1=28, front=20, back=1, rake=0.2, y=5, swell=2, belly=1)  # front/back x at the top; y half-width;
                                                                              # swell/belly = bulge at back/front
GRIP_TEXTURE = dict(inset=2, z0=-7, z1=24)          # stippled rubber on both sides, `inset` cubes in from the edges
# Tefa, 2026-10-18: "that handle could use a silver plate with a millitary logo in the middle". A silver plate one cube
# proud on each side, and on it a dark military star in a ring (bd_pistol_fine.py, LOGO).
GRIP_PLATE = dict(inset=2, z0=-8, z1=24, corner=2)  # Tefa: "make the handle longer downwards", then "extend
                                                   # the handle even further": 14 cubes lower, the plate with it
MAG_BASE = dict(z0=-15, z1=-13, over=1, y=6)          # the magazine's flared base plate
TANG = dict(x0=-11, z0=29, z1=32, y=4, droop=0.25)  # the tang reaching back over the web of the hand, its end drooping

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
# Tefa, 2026-10-18, second look: "the open area at the top of the slider needs to be closed - leave the open holes on
# the left hand side but make them rhombus shape and 5 smaller ones, on the right hand side make a bullet casing eject
# hole with a guard that will animate open afterwards". So the top is closed, the left side has five diamond holes onto
# the copper barrel, and the right side an ejection port with a brass case in it and a hinged cover, its own part.
DIAMONDS = dict(x=(20, 27, 34, 41, 48), z=44, half=2, y_in=1)   # LEFT side only; cut in to y_in, the barrel shows
PORT = dict(x0=24, x1=40, z0=41, z1=47, y_in=-1)   # RIGHT side: the ejection port, cut in to y_in
CASE = dict(x0=29, x1=36, y=-3, zc=45, r=1.8, head=1)   # a brass case lying in the port
COVER = dict(x0=24, x1=40, z0=41, z1=47, y=-7, ridges=(28, 32, 36), hinge_z=40)   # the port's cover, closed: one
                                                   # cube proud, hinged along its bottom edge (hinge_z) to swing down
SERRATIONS = dict(x0=-3, x1=10, step=2, z0=35, z1=42)  # grip grooves at the back of the lower band, both sides
# Tefa: "the sights need to sit right for VR actual aiming". So the front post's top is level with the rear sight's
# top and sits in the middle of the notch, with a cube of light either side; the three white dots (two on the rear
# sight's back face, one on the post's back face) are all at one height; and the sight line runs 3 cubes above the
# compensator, so nothing between the sights blocks it.
REAR_SIGHT = dict(x0=-5, x1=0, y=5, z1=54, notch=1, notch_depth=2, dot_z=53)
BARREL = dict(x0=8, x1=64, zc=41, r=4.0)           # copper, under the windows; it stops at the compensator, so
                                                   # the bore through that is dark metal, not copper
# The compensator: a heavy block on the nose, ports cut into its top and sides, the bore through its front.
# Tefa: "the front of the weapon needs to be thicker than the rest of the body and the barrel has to extend further
# out". So the compensator is wider and taller than the slide, and the barrel runs on past it with a lip at its end.
# Third look (Tefa): "extend the pistol thick part backwards 1x and forwards 3x the thickness of it, so it covers the
# thin muzzle completely". Its length was 11 cubes (65-75): now 11 more behind and 33 more in front, the bore cut into
# its front face with a bright crown, no barrel sticking out. Where it reaches back over the frame it wraps around it.
COMP = dict(x0=54, x1=108, y=8, z0=31, z1=51, bevel=2, top_ports=(90, 94, 98, 102), port_w=2, port_depth=3)
# Tefa: "it needs some sort of a thing at the bottom of the [compensator] ... that actually blows out steam from both
# left and right sides when a mag is ejected". A vent box under the compensator's front with five slots on each side,
# dark inside. The steam itself is a game effect for later; STEAM_POINTS are where it comes out, (x, z), both sides.
VENT = dict(x0=68, x1=102, y=7, z0=23, z1=30, bevel=1, lean=3, slots=(73, 79, 85, 91, 97), slot_w=2, slot_z=(25, 28),
            slot_depth=2)
STEAM_POINTS = [(x + 0.5, 26.5) for x in VENT['slots']]
FRONT_SIGHT = dict(x0=105, x1=106, y=1, z1=54, dot_z=53)   # top level with REAR_SIGHT's; 3 cubes wide, as one
                                                   # cube looked too thin from behind the rear sight
MUZZLE = dict(bore=2.4, depth=6)                   # the bore into the compensator's front, its walls dark

# ---- fine detail with the kit's smallest cubes (0.85 mm): bd_pistol_fine.py, the shotgun's way (shotgun/bd_fine.py) ----
# In cubes, quarters allowed: (part, side, y, ...): y = how far out the face is; side 'both' mirrors it.
FINE_LINES = [   # cut one small cube deep: (part, side, y, [(x, z) corners, joined])
    ('slide', 'both', 6, [(12, 37.5), (44, 37.5), (49, 42.5), (53, 42.5)]),   # an angled panel line on the lower band
    ('slide', 'both', 6, [(46, 35), (48.5, 41)]),                          # the picture's "//" near the nose
    ('slide', 'both', 6, [(49.5, 35), (52, 41)]),
    ('frame', 'both', 6, [(1, 30.5), (38, 30.5)]),                          # along the frame
    ('frame', 'both', 6, [(40, 18.25), (60, 18.25)]),                       # along the module's bottom
]
FINE_SCREWS = [  # raised screw heads with a slot: (part, side, y, [(x, z) centres])
    ('frame', 'both', 6, [(4, 30.5), (35, 30.5), (59, 24)]),
    ('slide', 'both', 8, [(55.5, 33.5), (55.5, 48.5)]),                   # the compensator's back corners
]
FINE_STAMPS = [  # raised marks: (part, side, y, x, z_top, pattern, dot, colour); '#' = a dot of dot x dot small cubes
    ('slide', 'both', 5, 2, 48, ("#..#..", ".#..#.", "..#..#", ".#..#.", "#..#.."), 2, 'red'),   # the red ">>"
    ('slide', 'both', 6, 14, 42.5, ("...#...", "..#.#..", "..#.#..", ".#.#.#.", ".#...#.", "#..#..#",
                                    "#.....#", "#######"), 1, 'white'),                          # a warning triangle
]
# Tefa: "the bulkier bit needs raised diagonal lines near the muzzle, 4 of them like //// in a row on both sides".
# Then: "make the //// go alongside it so that they are wider and a bit have bigger gaps between them".
# Raised strips on the compensator's sides: (side, y, count, first (x, z) bottom, (x, z) top, step along x, width and
# height in small cubes).
FINE_RIDGES = [('both', 8, 4, (64, 36), (68, 46), 9, 4, 2)]
# The military star in a ring on each grip plate: centred on the plate, in cubes.
LOGO = dict(z=8, ring_r=4.75, ring_w=0.75, star_r=3.75, star_in=1.5, height=2)
FINE_COL = dict(line=(4, 4, 4), screw=(40, 41, 45), ridge=(30, 31, 34), red=(176, 24, 20), white=(200, 200, 194),
                ring=(10, 10, 11), star=(10, 10, 11))   # near black on the gunmetal plate

# Carved scratches, as on the shotgun and the gloves: shorter, the pistol being small; a fraction lighter inside.
WEAR = dict(seed=668, scratch_per_cm2=0.06, scratch_mm=(6.0, 22.0), along_share=0.75, gouge_share=0.1,
            zigzag_share=0.35)
SCRATCH_LIGHTEN = 1.4

# ---- colours, sRGB 0-255: black like the shotgun's metal, copper where the picture glows ----
# Tefa: "we need to make this a black gun": every metal tone taken down, the grip too; the silver plates stay.
COL = dict(
    metal=(14, 14, 15),
    metal_hi=(32, 33, 36),        # worn edges, the ring
    metal_mid=(20, 20, 22),       # the upper deck, a touch lighter, like the picture's slide
    metal_dark=(8, 8, 9),
    copper=(132, 74, 44),
    copper_hi=(170, 102, 62),
    brass=(170, 130, 60),
    brass_hi=(206, 166, 86),
    bore=(4, 4, 4),
    port=(9, 9, 10),
    grip=(11, 11, 12),
    grip_check=(20, 20, 22),
    silver=(46, 49, 55),          # the grip plates. Tefa: "silver plates need to be the gun metal colour"
    silver_hi=(66, 70, 77),
    silver_dark=(32, 34, 38),
    sight_dot=(235, 235, 228),
)
EDGE_WEAR = 0.6                  # how far a worn metal edge goes toward metal_hi

SHADE = {(0, 0, 1): 1.12, (0, 0, -1): 0.55, (0, 1, 0): 0.88, (0, -1, 0): 0.88,
         (1, 0, 0): 0.74, (-1, 0, 0): 0.74}
NOISE = 0.05
