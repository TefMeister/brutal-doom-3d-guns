# Brutal Doom: the BFG 10K, forge cube version. Free design, bold: a long industrial energy cannon: a six-sided
# barrel of armour plates with green energy glowing through the seams, a big rotating cooling ring at the front
# (its own part), a heavy reactor drum behind the grip with warning stripes and a status display, twin side handles.
import math

from _common import (Model, fp, METAL, METAL_HI, METAL_MID, PANEL, PANEL_DK, CAUTION, WHITE, GREEN, DARK, SCREW, UAC,
                     armour, corner_screws, hazard, finish, vents, mul)

GLOW = (110, 255, 120)
Z_AXIS = 22.0


def build():
    m = Model("bd_bfg10k")
    m.pivot = (60, 0, 0)
    # the reactor drum at the back
    m.cyl(0, 60, 0, Z_AXIS, 18.0, fp.metal(PANEL_DK), edge=0.5)
    for x in (4, 26, 52):
        m.cyl(x, x + 4, 0, Z_AXIS, 19.0, fp.metal(METAL), edge=0.25)
    hazard(m, 8, 26, -20, 20, Z_AXIS - 20, Z_AXIS + 20, step=3.0)
    m.cyl(-2, 2, 0, Z_AXIS, 10.0, GLOW, edge=0.25)
    m.cyl(-3, 0, 0, Z_AXIS, 6.0, (230, 255, 230), edge=0.25)
    # the hexagonal barrel of plates, energy in the seams
    for k in range(6):
        a = k * math.pi / 3
        yc, zc = math.cos(a) * 9, Z_AXIS + math.sin(a) * 9
        m.cyl(60, 230, yc, zc, 5.0, fp.metal(METAL_MID), edge=0.25)
    m.cyl(60, 232, 0, Z_AXIS, 7.0, GLOW, edge=0.25)
    for x in range(70, 222, 14):
        m.cyl(x, x + 4, 0, Z_AXIS, 15.0, fp.metal(METAL), edge=0.25)
    # the cooling ring at the front, finned
    m.part = 'ring'
    m.cyl(214, 228, 0, Z_AXIS, 22.0, fp.metal(METAL_HI), hollow=14.0, edge=0.5)
    for k in range(12):
        a = k * math.tau / 12
        m.box(212, 230, math.cos(a) * 20 - 1.5, math.cos(a) * 20 + 1.5, Z_AXIS + math.sin(a) * 20 - 1.5,
              Z_AXIS + math.sin(a) * 20 + 1.5, fp.metal(METAL), size=0.5, keep=True)
    m.part = 'body'
    m.cyl(230, 240, 0, Z_AXIS, 12.0, fp.metal(METAL), edge=0.5)
    m.cyl(234, 241, 0, Z_AXIS, 8.0, None, edge=0.5, carve=True)
    m.ball(236, 0, Z_AXIS, 7.0, GLOW, edge=0.25)
    # grip, side handles, a status display
    m.cprism([(70, Z_AXIS - 10), (62, Z_AXIS - 12), (56, -10), (66, -12), (74, 0), (80, Z_AXIS - 10)], 11.0,
             fp.metal(METAL), bevel=2.0, edge=0.5)
    fp.trigger(m, 84, Z_AXIS - 10, fp.metal(METAL_HI), length=7)
    for y in (-1, 1):
        m.cyl(y * 16, y * 26, 140, Z_AXIS, 2.2, fp.metal(METAL), axis='y', edge=0.25)
        m.cyl(Z_AXIS - 12, Z_AXIS + 6, 140, y * 27, 2.6, (34, 34, 36), axis='z', edge=0.25)
    m.cbox(30, 50, 10.0, Z_AXIS + 17, Z_AXIS + 22, fp.metal(METAL), bevel=1.0, edge=0.25)
    m.box(32, 48, -3, 3, Z_AXIS + 21.75, Z_AXIS + 22.25, (10, 40, 14), size=0.25)
    for i in range(7):
        m.box(33 + i * 2, 34 + i * 2, -1, 1, Z_AXIS + 22, Z_AXIS + 22.25, GLOW if i < 5 else (30, 80, 30),
              size=0.25)
    for side in ('+y', '-y'):
        m.decal(UAC, 34, Z_AXIS + 6, side, WHITE, dot=2, mode='paint')
        m.decal(["###.###.###...#.###.#.#", "#.#.#...#....##.#.#.##.", "###.###.#.#...#.#.#.#..",
                 "#.#.#...#.#...#.#.#.##.", "###.#...###...#.###.#.#"], 90, Z_AXIS + 13, side, WHITE, mode='paint')
    finish(m, 2410, (0, 230, Z_AXIS - 14, Z_AXIS + 14), grime=0.2, scratches=18, cracks=3)
    return m
