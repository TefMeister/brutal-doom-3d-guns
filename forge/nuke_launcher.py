# Brutal Doom: the nuke launcher, forge cube version. Free design, bold: a huge shoulder tube in faded olive with a
# fat nuclear warhead poking out of the front, yellow radiation trefoils and black-yellow stripes, a heavy blast
# shield, a big analog arming dial, a flip-up targeting screen glowing green, a hefty grip and front handle.
import math

from _common import (Model, fp, METAL, METAL_HI, METAL_MID, PANEL, PANEL_DK, CAUTION, WHITE, GREEN, DARK, SCREW,
                     corner_screws, hazard, finish, vents, mul)

OLIVE = (90, 96, 60)
WARHEAD = (196, 196, 186)
Z_AXIS = 22.0
TREFOIL = [".....###.....", "....#####....", "...#######...", "#.....#.....#", "##...###...##",
           "###..#.#..###", "####.....####", ".............", "....#####....", "...#######...", "....#####...."]


def build():
    m = Model("bd_nuke_launcher")
    m.pivot = (80, 0, 0)
    m.cyl(0, 200, 0, Z_AXIS, 14.0, fp.rusty(OLIVE, (80, 70, 40), 0.25, seed=2701), edge=0.5)
    m.cyl(-2, 6, 0, Z_AXIS, 15.0, fp.metal(METAL), edge=0.25)
    m.cyl(-3, 4, 0, Z_AXIS, 11.0, None, edge=0.25, carve=True)
    for x in (40, 120, 190):
        m.cyl(x, x + 4, 0, Z_AXIS, 15.0, fp.metal(METAL), edge=0.25)
    hazard(m, 150, 170, -16, 16, Z_AXIS - 16, Z_AXIS + 16, step=3.0)
    # the warhead: a fat rounded nose with a fin ring, poking out of the front
    m.part = 'warhead'
    m.cyl(196, 220, 0, Z_AXIS, 12.0, fp.metal(WARHEAD), edge=0.5)
    m.ball(220, 0, Z_AXIS, 12.0, fp.metal(WARHEAD), edge=0.5)
    m.recolour(lambda x, y, z: x > 226, CAUTION)
    m.cyl(202, 206, 0, Z_AXIS, 12.5, DARK, size=0.5, edge=0.25)
    m.part = 'body'
    # the blast shield, the arming dial, the targeting screen
    m.cbox(96, 100, 40.0, Z_AXIS - 10, Z_AXIS + 22, fp.metal(METAL_MID), bevel=2.0, edge=0.5)
    m.cyl(14, 18, 60, Z_AXIS + 2, 6.0, fp.metal(METAL_HI), axis='y', edge=0.25)
    m.cyl(17.5, 18, 60, Z_AXIS + 2, 5.0, (230, 226, 210), axis='y', size=0.25, edge=0.25)
    for t in range(8):
        m.box(60 + t * 0.5, 60.25 + t * 0.5, 18, 18.25, Z_AXIS + 2 - t * 0.3, Z_AXIS + 2.25 - t * 0.3,
              (200, 30, 20), size=0.25)
    m.part = 'screen'
    m.box(70, 90, 10, 12, Z_AXIS + 14, Z_AXIS + 28, fp.metal(METAL), size=0.5)
    m.box(72, 88, 9.75, 10, Z_AXIS + 16, Z_AXIS + 26, (20, 80, 30), size=0.25)
    for i in range(6):
        m.box(74 + i * 2, 75 + i * 2, 9.5, 9.75, Z_AXIS + 18 + (i % 3), Z_AXIS + 19 + (i % 3), GREEN, size=0.25)
    m.part = 'body'
    # grip, front handle, shoulder pad
    m.cprism([(80, Z_AXIS - 13), (72, Z_AXIS - 15), (66, -10), (76, -12), (84, 0), (90, Z_AXIS - 13)], 11.0,
             fp.metal(METAL), bevel=2.0, edge=0.5)
    fp.trigger(m, 94, Z_AXIS - 13, fp.metal(METAL_HI), length=7)
    m.cprism([(130, Z_AXIS - 13), (126, -6), (134, -8), (140, Z_AXIS - 13)], 9.0, fp.metal(METAL), bevel=1.5,
             edge=0.5)
    m.cbox(20, 60, 16.0, Z_AXIS - 18, Z_AXIS - 12, (40, 36, 30), bevel=1.0, edge=0.25)
    for side in ('+y', '-y'):
        m.decal(TREFOIL, 104, Z_AXIS + 8, side, CAUTION, dot=2, mode='paint')
        m.decal(["#..#.#.#.#.#.###", "##.#.#.#.##..#..", "#.##.#.#.#.#.##.", "#..#.###.#.#.###"], 50,
                Z_AXIS + 8, side, WHITE, dot=2, mode='paint')                              # NUKE
    finish(m, 2710, (0, 200, Z_AXIS - 12, Z_AXIS + 12), grime=0.25, scratches=18, cracks=3)
    return m
