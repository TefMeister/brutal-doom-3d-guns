# Brutal Doom: the incendiary launcher (an M202 kind of gun), forge cube version. Free design, bold: four square
# launch tubes in a block, olive drab with orange warning bands, the front cover flipped open showing four
# glowing-orange rocket noses, a folding sight frame on the left, a pistol grip and a firing box, a shoulder pad.
from _common import (Model, fp, METAL, METAL_HI, METAL_MID, CAUTION, WHITE, ORANGE, GREEN, DARK, SCREW, HAZARD_TRI,
                     corner_screws, hazard, finish, mul)

OLIVE = (82, 90, 54)
OLIVE_DK = (52, 58, 32)
Z_AXIS = 20.0
TUBE = 9.0                             # each square tube's outside width


def build():
    m = Model("bd_incendiary_launcher")
    m.pivot = (70, 0, 0)
    # the four tubes as one block with grooves between them
    m.cbox(0, 180, 2 * TUBE, Z_AXIS - TUBE, Z_AXIS + TUBE, fp.metal(OLIVE, 0.08), bevel=1.5, edge=0.5)
    for side in ('+y', '-y'):
        m.groove([(2, Z_AXIS), (178, Z_AXIS)], side, depth=2, dark=0.35)
    for side in ('+z', '-z'):
        m.groove([(2, 0), (178, 0)], side, depth=2, dark=0.35)
    for y in (-TUBE / 2, TUBE / 2):
        for z in (Z_AXIS - TUBE / 2, Z_AXIS + TUBE / 2):
            m.cyl(176, 181, y, z, 3.2, None, edge=0.25, carve=True)
            m.cyl(173, 176, y, z, 3.2, ORANGE, r1=1.2, edge=0.25)
            m.cyl(-1, 4, y, z, 3.2, None, edge=0.25, carve=True)
    hazard(m, 150, 160, -20, 20, 0, 40, step=2.5)
    m.recolour(lambda x, y, z: 20 < x < 26, CAUTION)
    # the front cover, flipped up on its hinge
    m.part = 'cover'
    m.box(178, 180, -TUBE, TUBE, Z_AXIS + TUBE, Z_AXIS + TUBE + 18, fp.metal(OLIVE_DK), size=0.5, bevel=0.5)
    m.part = 'body'
    m.cyl(-TUBE, TUBE, 179, Z_AXIS + TUBE, 1.0, fp.metal(METAL_HI), axis='y', edge=0.25)
    # sight frame on the left, grips, firing box, shoulder pad
    m.cbox(100, 104, 4.0, Z_AXIS + TUBE, Z_AXIS + TUBE + 2, fp.metal(METAL), size=0.5)
    m.box(100, 104, TUBE, TUBE + 10, Z_AXIS + TUBE - 2, Z_AXIS + TUBE, fp.metal(METAL), size=0.5)
    m.prism([(100, Z_AXIS + TUBE), (100, Z_AXIS + TUBE + 12), (104, Z_AXIS + TUBE + 12), (104, Z_AXIS + TUBE)],
            TUBE + 8, TUBE + 10, fp.metal(METAL), size=0.5)
    m.prism([(101, Z_AXIS + TUBE + 2), (101, Z_AXIS + TUBE + 10), (103, Z_AXIS + TUBE + 10),
             (103, Z_AXIS + TUBE + 2)], TUBE + 8, TUBE + 10, None, size=0.5, carve=True)
    m.box(101.5, 102.5, TUBE + 8.5, TUBE + 9.5, Z_AXIS + TUBE + 5.5, Z_AXIS + TUBE + 6.5, GREEN, size=0.25)
    m.cprism([(70, Z_AXIS - TUBE), (62, Z_AXIS - TUBE - 4), (58, -14), (68, -16), (74, -4), (80, Z_AXIS - TUBE)],
             9.0, fp.metal(METAL), bevel=2.0, edge=0.5)
    fp.trigger(m, 82, Z_AXIS - TUBE, fp.metal(METAL_HI), length=6)
    m.cbox(84, 104, 10.0, -2, Z_AXIS - TUBE, fp.metal(OLIVE_DK), bevel=1.5, edge=0.5)
    m.cprism([(120, Z_AXIS - TUBE), (116, -10), (124, -12), (130, Z_AXIS - TUBE)], 8.0, fp.metal(METAL), bevel=1.5,
             edge=0.5)
    m.cbox(10, 40, 12.0, Z_AXIS - TUBE - 4, Z_AXIS - TUBE, (36, 34, 30), bevel=1.0, edge=0.25)
    for side in ('+y', '-y'):
        m.decal(HAZARD_TRI, 60, Z_AXIS + 6, side, CAUTION, mode='paint')
        m.decal(["#...#.###.###.###", "##.##.#.....#.#.#", "#.#.#.#...###.#.#", "#...#.#...#...#.#",
                 "#...#.###.###.###"], 110, Z_AXIS + 5, side, WHITE, mode='paint')        # "M202"
        for x in (8, 172):
            m.bolt(x, Z_AXIS, side, SCREW)
    finish(m, 1910, (0, 180, Z_AXIS - TUBE, Z_AXIS + TUBE), grime=0.25, scratches=18, cracks=3)
    return m
