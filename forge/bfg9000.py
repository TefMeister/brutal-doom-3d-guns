# Brutal Doom: the BFG 9000, forge cube version. Free design, as big and bold as it gets: a massive armoured body in
# gun metal and dark-red paint, a huge round emitter mouth with a green energy core and six heavy fins round it, glass
# charge windows along the sides glowing green, two cooling barrels, a top carry rail, hazard stripes, skull marks.
import math

from _common import (Model, fp, METAL, METAL_HI, METAL_MID, PANEL, PANEL_DK, RED, RED_HI, CAUTION, WHITE, GREEN,
                     DARK, SCREW, UAC, SKULL, armour, corner_screws, hazard, worn_paint, finish, vents, mul)

Z_AXIS = 20.0
CORE = (120, 255, 120)


def build():
    m = Model("bd_bfg9000")
    m.pivot = (70, 0, 0)
    armour(m, 0, 150, 36.0, 0, 42, worn_paint(RED, RED_HI, 0.25, 1001), bevel=5.0, panel=PANEL_DK)
    m.cbox(10, 140, 30.0, 42, 46, fp.metal(METAL), bevel=2.0, edge=0.5)
    # glass charge windows along each side, green inside, with bars
    for side, ys in (('+y', 1), ('-y', -1)):
        m.box(30, 110, ys * 17 - 1.5 if ys > 0 else -18.5, ys * 17 + 1.5 if ys > 0 else -15.5, 22, 32, None,
              size=0.5, carve=True)
        m.box(30, 110, 14.5 if ys > 0 else -15.5, 15.5 if ys > 0 else -14.5, 22, 32, (60, 200, 70), size=0.5)
        for x in range(36, 110, 10):
            m.box(x, x + 2, 15.5 if ys > 0 else -18.5, 18.5 if ys > 0 else -15.5, 22, 32, fp.metal(METAL_HI),
                  size=0.5)
    # the emitter: a huge collar, six fins, and a glowing green core in its mouth
    m.cyl(150, 176, 0, Z_AXIS, 18.0, fp.metal(METAL_MID), edge=0.5)
    m.cyl(170, 178, 0, Z_AXIS, 14.0, None, edge=0.5, carve=True)
    m.ball(166, 0, Z_AXIS, 10.0, CORE, edge=0.25)
    m.ball(168, 0, Z_AXIS, 6.0, (220, 255, 220), edge=0.25)
    for k in range(6):
        a = k * math.pi / 3
        for t in range(10):
            r = 18 + t * 0.6
            yc, zc = math.cos(a) * r, Z_AXIS + math.sin(a) * r
            m.box(150 + t * 1.5, 178, yc - 1.5, yc + 1.5, zc - 1.5, zc + 1.5, fp.metal(METAL), size=0.5, keep=True)
    for x in (152, 160):
        m.cyl(x, x + 2, 0, Z_AXIS, 18.5, fp.metal(METAL_HI), edge=0.25)
    # two cooling barrels under the body, vented
    for y in (-10, 10):
        m.cyl(120, 170, y, -4, 4.0, fp.metal(METAL), edge=0.25)
        for x in range(124, 168, 4):
            m.cyl(x, x + 1.5, y, -4, 5.0, fp.metal(PANEL), edge=0.25)
    # grip, guard, front handle, top rail
    m.cprism([(60, 2), (50, 0), (44, -22), (56, -24), (64, -6), (72, 2)], 12.0, fp.metal(METAL), bevel=2.0,
             edge=0.5)
    fp.guard(m, 66, 86, -10, 0, fp.metal(METAL))
    fp.trigger(m, 74, 0, fp.metal(METAL_HI), length=7)
    m.cprism([(110, 2), (104, -20), (114, -22), (120, 2)], 10.0, fp.metal(METAL), bevel=2.0, edge=0.5)
    for x in range(14, 138, 4):
        m.box(x, x + 1.5, -4, 4, 46, 47.5, fp.metal(METAL_HI), size=0.5)
    hazard(m, 0, 12, -20, 20, 0, 42, step=3.0)
    vents(m, 116, 146, 8, 34, step=4.0, glow=(60, 160, 60))
    for side in ('+y', '-y'):
        m.decal(UAC, 116, 40, side, WHITE, dot=2, mode='paint')
        m.decal(["###.###.###", "#.#.#...#..", "###.###.#.#", "#.#.#...#.#", "###.#...###"], 30, 40, side, WHITE,
                dot=2, mode='raise')                                                       # "BFG"
        m.decal(SKULL, 14, 18, side, (230, 230, 220), dot=1, mode='raise')
    corner_screws(m, 0, 150, 0, 42, inset=4, kind='hex')
    finish(m, 1010, (0, 150, 0, 42), grime=0.22, scratches=20, cracks=4)
    return m
