# Brutal Doom: the flamethrower, forge cube version. Free design, bold: a long nozzle with a blue pilot flame, a
# red fuel tank slung under the gun with a pressure gauge and valve, an armoured braided hose, a scorched heat
# shield round the barrel, hazard stripes and FLAMMABLE stencils.
import math

from _common import (Model, fp, METAL, METAL_HI, METAL_MID, PANEL, PANEL_DK, RED, RED_HI, CAUTION, WHITE, ORANGE,
                     DARK, SCREW, HAZARD_TRI, armour, corner_screws, hazard, worn_paint, finish, vents, mix)

PILOT_BLUE = (90, 150, 255)
Z_AXIS = 18.0


def build():
    m = Model("bd_flamethrower")
    m.pivot = (60, 0, 0)
    armour(m, 30, 100, 16.0, 6, 30, fp.metal(METAL_MID), bevel=2.5, panel=PANEL)
    m.cprism([(-6, 0), (-6, 26), (30, 28), (30, 8), (10, 0)], 12.0, fp.metal(METAL), bevel=2.0, edge=0.5)
    # the red tank underneath, banded, a gauge and a valve wheel on its left
    m.part = 'tank'
    m.cyl(36, 104, 0, -2, 8.0, worn_paint(RED, RED_HI, 0.3, 2201), edge=0.5)
    m.ball(36, 0, -2, 8.0, worn_paint(RED, RED_HI, 0.3, 2201), edge=0.5)
    m.ball(104, 0, -2, 8.0, worn_paint(RED, RED_HI, 0.3, 2201), edge=0.5)
    for x in (48, 92):
        m.cyl(x, x + 2.5, 0, -2, 8.5, fp.metal(METAL), edge=0.25)
    m.cyl(8, 11, 70, -2, 3.2, fp.metal(METAL_HI), axis='y', edge=0.25)
    m.cyl(10.5, 11, 70, -2, 2.6, (230, 226, 210), axis='y', size=0.25, edge=0.25)
    for t in range(6):
        m.box(70 + t * 0.4, 70.25 + t * 0.4, 11, 11.25, -2 + t * 0.35, -1.75 + t * 0.35, (200, 30, 20), size=0.25)
    m.part = 'body'
    # the barrel inside a perforated heat shield, a scorched nozzle with a pilot light
    m.cyl(100, 190, 0, Z_AXIS, 3.0, fp.metal(METAL), edge=0.25)
    m.cyl(104, 176, 0, Z_AXIS, 6.0, fp.metal(PANEL_DK), hollow=4.5, edge=0.25)
    for x in range(108, 172, 6):
        for side in ('+y', '-y', '+z'):
            m.groove([(x, Z_AXIS) if side != '+z' else (x, 0), (x + 2, Z_AXIS) if side != '+z' else (x + 2, 0)],
                     side, depth=3, width=3, dark=0.2)
    m.cyl(186, 200, 0, Z_AXIS, 4.0, fp.metal((40, 30, 24)), r1=5.0, edge=0.25)
    m.cyl(194, 201, 0, Z_AXIS, 2.6, None, edge=0.25, carve=True)
    m.cyl(193, 194, 0, Z_AXIS, 2.6, ORANGE, size=0.25, edge=0.25)
    m.cyl(186, 196, 0, Z_AXIS - 6.5, 1.0, fp.metal(METAL_HI), edge=0.25)
    m.ball(197, 0, Z_AXIS - 6.5, 1.2, PILOT_BLUE, edge=0.25)
    # the braided hose from the tank up into the gun, on the right
    for i in range(50):
        t = i / 49
        x = 100 + t * 14
        z = -2 + math.sin(t * math.pi) * 4 + t * 16
        m.ball(x, -9, z, 1.6, fp.metal(mix(METAL_HI, METAL, (i % 2) * 0.7)), edge=0.25)
    # grip, fore-grip, guard
    m.cprism([(50, 6), (42, 4), (38, -14), (48, -16), (54, -2), (58, 6)], 9.0, fp.metal(METAL), bevel=2.0, edge=0.5)
    fp.guard(m, 56, 70, -4, 6, fp.metal(METAL))
    fp.trigger(m, 62, 6, fp.metal(METAL_HI), length=6)
    hazard(m, 94, 100, -10, 10, 6, 30, step=2.0)
    for side in ('+y', '-y'):
        m.decal(HAZARD_TRI, 40, 26, side, CAUTION, mode='paint')
        m.decal(["###.#...###.#...#.#...#.###.###.#...###", "#...#...#.#.##.##.##.##.#.#.#.#.#...#..",
                 "###.#...###.#.#.#.#.#.#.###.###.#...###", "#...#...#.#.#...#.#...#.#.#.#.#.#...#..",
                 "#...###.#.#.#...#.#...#.#.#.###.###.###"], 52, 14, side, WHITE, mode='paint')   # FLAMMABLE
    corner_screws(m, 30, 100, 6, 30, inset=3, kind='hex')
    finish(m, 2210, (30, 100, 6, 30), grime=0.3, scratches=14, cracks=2)
    return m
