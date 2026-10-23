# Brutal Doom: the MP40 (from the Wolfenstein levels), forge cube version. Faithful to the real gun's shape, with a
# Brutal Doom finish: a black tube receiver, a ribbed bakelite grip frame, a long straight magazine, the barrel with
# its resting hook underneath, a folding steel stock folded under, chipped paint and grime.
from _common import (Model, fp, METAL, METAL_HI, METAL_MID, PANEL, WHITE, DARK, SCREW, finish, mul)

BAKELITE = (66, 40, 30)
Z_BORE = 14.0


def build():
    m = Model("bd_mp40")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (40, 0, 0)
    m.cyl(20, 110, 0, Z_BORE, 5.0, fp.metal(METAL_MID), edge=0.5)                         # receiver tube
    m.cyl(18, 22, 0, Z_BORE, 5.5, fp.metal(METAL), edge=0.25)
    m.box(60, 86, -6, -3.5, Z_BORE - 2, Z_BORE + 2, None, size=0.25, carve=True)          # ejection port, right
    m.box(30, 90, 4, 6, Z_BORE - 0.5, Z_BORE + 0.5, None, size=0.25, carve=True)          # bolt slot, left
    m.part = 'bolt'
    m.box(46, 49, 5, 9, Z_BORE - 1, Z_BORE + 1, fp.metal(METAL_HI), size=0.5, edge=0.25)
    m.part = 'body'
    m.part = 'barrel'
    # barrel, its resting bar, front sight hood
    fp.barrel(m, 110, 160, Z_BORE, 2.4, fp.metal(METAL), bore=1.2)
    m.part = 'rest'
    m.cbox(110, 126, 5.0, Z_BORE - 8, Z_BORE - 4, fp.metal(METAL), bevel=1.0, edge=0.25)
    m.cbox(122, 126, 3.0, Z_BORE - 10, Z_BORE - 4, fp.metal(METAL), size=0.5)
    m.part = 'sight'
    m.cyl(152, 156, 0, Z_BORE + 4, 3.0, fp.metal(METAL), hollow=2.0, edge=0.25)
    m.box(153, 155, -0.5, 0.5, Z_BORE + 2, Z_BORE + 5.5, fp.metal(METAL_HI), size=0.25)
    m.cbox(30, 36, 4.0, Z_BORE + 4, Z_BORE + 8, fp.metal(METAL), size=0.5)                 # rear sight
    m.part = 'frame'
    # the lower frame in ribbed bakelite, the grip, the guard
    m.cprism([(26, 9), (100, 9), (100, 4), (70, 2), (40, 2), (26, 4)], 9.0, fp.metal(BAKELITE, 0.08), bevel=1.5,
             edge=0.5)
    for x in range(72, 98, 3):
        for side in ('+y', '-y'):
            m.groove([(x, 3), (x, 8)], side, depth=1, dark=0.5)
    m.part = 'grip'
    m.cprism([(44, 2), (36, 2), (30, -18), (40, -20), (46, -6), (50, 2)], 8.5, fp.metal(BAKELITE, 0.08), bevel=2.0,
             edge=0.5)
    m.part = 'guard'
    fp.guard(m, 48, 64, -7, 2, fp.metal(METAL))
    fp.trigger(m, 55, 2, fp.metal(METAL_HI), length=5)
    # the magazine, long and straight, ribbed
    m.part = 'mag'
    m.cbox(84, 94, 6.0, -42, 2, fp.metal(METAL), bevel=1.0, edge=0.5)
    m.cbox(82, 96, 7.0, -4, 4, fp.metal(METAL_HI), bevel=1.0, edge=0.25)                   # mag well
    for side in ('+y', '-y'):
        m.groove([(86, -38), (86, -8)], side, depth=1, dark=0.5)
        m.groove([(92, -38), (92, -8)], side, depth=1, dark=0.5)
    m.part = 'body'
    m.part = 'stock'
    # the steel stock, unfolded: two struts back from the receiver to a butt plate
    for y in (-3, 3):
        m.box(-40, 22, y - 0.75, y + 0.75, Z_BORE - 1, Z_BORE + 0.5, fp.metal(METAL_HI), size=0.5)
        m.box(-40, 30, y - 0.75, y + 0.75, 2, 3.5, fp.metal(METAL_HI), size=0.5)
    m.cprism([(-44, -2), (-44, Z_BORE + 3), (-40, Z_BORE + 3), (-40, -2)], 8.0, fp.metal(METAL), bevel=1.0,
             edge=0.25)
    for side in ('+y', '-y'):
        m.screw(40, 6, side, SCREW, kind='slot')
        m.screw(96, 6, side, SCREW, kind='slot')
        m.decal(["#...#.###..###", "##.##.#..#.#.#", "#.#.#.###..#.#", "#...#.#....#.#", "#...#.#....###"], 64,
                Z_BORE + 3, side, mul(METAL_HI, 1.6), mode='carve')                       # "MP40"
    finish(m, 1410, (20, 110, 2, Z_BORE + 5), grime=0.28, scratches=14, cracks=2)
    return m
