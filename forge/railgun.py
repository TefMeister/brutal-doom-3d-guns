# Brutal Doom: the railgun, forge cube version. Free design, bold: two long parallel conductor rails with a gap
# between them where blue-white light runs, wrapped every few inches by copper coils, a bulky capacitor bank at the
# back with a charge meter of lights, a heavy stock, a long scope, warning stripes.
from _common import (Model, fp, METAL, METAL_HI, METAL_MID, PANEL, PANEL_DK, CAUTION, WHITE, GREEN, CYAN, DARK,
                     SCREW, UAC, armour, corner_screws, hazard, finish, vents)

COPPER = (190, 104, 52)
RAIL_LIGHT = (170, 220, 255)
Z_AXIS = 18.0


def build():
    m = Model("bd_railgun")
    m.pivot = (70, 0, 0)
    armour(m, 30, 120, 22.0, 2, 32, fp.metal(METAL_MID), bevel=3.0, panel=PANEL)
    m.cprism([(-10, -6), (-10, 26), (30, 30), (30, 6), (10, -6)], 14.0, fp.metal(METAL), bevel=2.5, edge=0.5)
    m.cbox(-12, -10, 14.5, -7, 27, (30, 30, 32), size=0.5)
    # the capacitor bank: three fat cells on top with a light meter
    for i, y in enumerate((-6, 0, 6)):
        m.cyl(40, 100, y, 36, 3.0, fp.metal(PANEL_DK), edge=0.25)
        for x in range(44, 98, 6):
            m.box(x, x + 1, y - 0.5, y + 0.5, 38.75, 39.25, GREEN if x < 80 else (40, 70, 40), size=0.25)
    # the two rails out front, with light in the gap, coils round them
    for z in (Z_AXIS - 5, Z_AXIS + 5):
        m.cbox(120, 270, 8.0, z - 2.5, z + 2.5, fp.metal(METAL_HI), bevel=1.0, edge=0.25)
    m.cbox(120, 266, 2.0, Z_AXIS - 2.5, Z_AXIS + 2.5, RAIL_LIGHT, size=0.5)
    for x in range(126, 262, 12):
        m.cyl(x, x + 4, 0, Z_AXIS, 9.0, COPPER, hollow=7.0, edge=0.25)
        for t in range(4):
            m.cyl(x + t, x + t + 0.5, 0, Z_AXIS, 9.25, (120, 60, 30), hollow=8.75, size=0.25, edge=0.25)
    m.cbox(262, 274, 14.0, Z_AXIS - 10, Z_AXIS + 10, fp.metal(METAL), bevel=2.0, edge=0.5)
    m.cbox(266, 275, 3.0, Z_AXIS - 2.5, Z_AXIS + 2.5, None, size=0.5, carve=True)
    hazard(m, 112, 120, -12, 12, 2, 32, step=2.0)
    # scope, grip, guard
    m.cyl(70, 140, 0, 44, 3.4, fp.metal(METAL), edge=0.25)
    m.cyl(136, 146, 0, 44, 4.6, fp.metal(METAL), edge=0.25)
    m.cyl(145.5, 146.5, 0, 44, 4.0, (90, 160, 210), size=0.25, edge=0.25)
    for x in (76, 128):
        m.cbox(x, x + 3, 4.0, 39, 42, fp.metal(METAL), size=0.5)
    m.cprism([(56, 4), (48, 2), (42, -16), (52, -18), (60, -4), (66, 4)], 10.0, fp.metal(METAL), bevel=2.0, edge=0.5)
    fp.guard(m, 62, 78, -6, 2, fp.metal(METAL))
    fp.trigger(m, 68, 2, fp.metal(METAL_HI), length=6)
    vents(m, 34, 56, 8, 26, step=4.0, glow=(60, 120, 180))
    for side in ('+y', '-y'):
        m.decal(UAC, 92, 28, side, WHITE, mode='paint')
        m.decal(["###.###.#.#..", "#.#.#.#.#.#..", "###.###.#.#..", "##..#.#.#.#..", "#.#.#.#.#.###"], 62, 28,
                side, CYAN, mode='paint')                                                  # "RAIL"
    corner_screws(m, 30, 120, 2, 32, inset=4, kind='hex')
    finish(m, 2110, (30, 120, 2, 32), grime=0.18, scratches=18, cracks=2)
    return m
