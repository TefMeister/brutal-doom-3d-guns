# Brutal Doom: the revolver, forge cube version. Free design, bold: a hand-cannon magnum: a slab-sided frame in worn
# dark-red paint, a fat fluted six-shot cylinder with brass showing, a full-lug barrel with a ported compensator and a
# heat shield, a green fibre front sight, a skeleton hammer, chunky rubber grips with a steel skull medallion.
import math

from _common import (Model, fp, METAL, METAL_HI, METAL_MID, PANEL, RED, RED_HI, WHITE, GREEN, BRASS, DARK, SCREW,
                     SKULL, UAC, worn_paint, finish, vents, mul)

RUBBER = (30, 30, 32)
Z_BORE = 12.0
FRAME = [(0, 2), (0, 18), (8, 20), (36, 20), (36, 3), (28, 0), (10, -2)]


def build():
    m = Model("bd_revolver")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (6, 0, 0)
    m.cprism(FRAME, 9.0, worn_paint(RED, RED_HI, 0.3, 601), bevel=1.5, edge=0.5)
    m.cbox(0, 38, 4.0, 20, 22, fp.metal(METAL), size=0.5, edge=0.25)                     # top strap
    # the cylinder: fat, deeply fluted, brass in the chambers
    m.part = 'cylinder'
    cz = Z_BORE - 2
    m.cyl(9, 33, 0, cz, 7.5, fp.metal(METAL_MID), edge=0.25)
    for k in range(6):
        a = k * math.pi / 3 + math.pi / 6
        m.cyl(12, 30, math.cos(a) * 8.4, cz + math.sin(a) * 8.4, 2.4, None, edge=0.25, carve=True)
        b = a + math.pi / 6
        yc, zc = math.cos(b) * 4.4, cz + math.sin(b) * 4.4
        m.cyl(31, 34, yc, zc, 1.5, None, edge=0.25, carve=True)
        m.cyl(30.5, 31, yc, zc, 1.5, BRASS, size=0.25, edge=0.25)
    m.part = 'body'
    m.part = 'barrel'
    # barrel with a full lug, a vented heat shield on top and a ported compensator
    m.cyl(36, 100, 0, Z_BORE, 3.2, fp.metal(METAL), edge=0.25)
    m.cbox(36, 96, 6.0, 4, Z_BORE, fp.metal(METAL_MID), bevel=1.0, edge=0.5)
    m.cbox(40, 96, 5.0, Z_BORE + 2, Z_BORE + 5, fp.metal(METAL_HI), bevel=1.0, edge=0.25)
    for x in range(44, 92, 6):
        m.box(x, x + 3, -1.5, 1.5, Z_BORE + 3.5, Z_BORE + 5, None, size=0.25, carve=True)
    m.cbox(96, 112, 8.0, 4, Z_BORE + 5, fp.metal(METAL), bevel=1.5, edge=0.5)
    vents(m, 99, 110, Z_BORE - 1, Z_BORE + 3, step=4.0, glow=(200, 80, 30))
    m.cyl(111, 113, 0, Z_BORE, 1.7, None, edge=0.25, carve=True)
    m.box(106, 109, -0.75, 0.75, Z_BORE + 5, Z_BORE + 8, fp.metal(METAL), size=0.25)
    m.box(106.5, 108.5, -0.5, 0.5, Z_BORE + 7, Z_BORE + 7.75, GREEN, size=0.25)
    m.part = 'sight'
    fp.rear_sight(m, 2, 22, 2.0, fp.metal(METAL), w=4.5, notch=1.5, dots=GREEN)
    # skeleton hammer
    m.part = 'hammer'
    m.cprism([(-1, 14), (-5, 21), (-8, 22), (-7, 24), (-2, 23), (3, 17), (2, 13)], 3.0, fp.metal(METAL_HI),
             size=0.5, edge=0.25)
    m.cyl(-2, 2, -3, 20, 1.0, None, axis='y', carve=True, edge=0.25)
    m.part = 'body'
    m.part = 'guard'
    fp.guard(m, 8, 28, -10, -1, fp.metal(METAL))
    fp.trigger(m, 18, -1, fp.metal(METAL_HI), length=7)
    m.part = 'grip'
    # chunky rubber grip with finger grooves and a skull medallion
    grip = [(4, 2), (-4, 0), (-14, -18), (-16, -34), (-2, -36), (4, -28), (10, -12), (12, 0)]
    m.cprism(grip, 10.0, fp.metal(RUBBER, 0.1), bevel=2.5, edge=0.5)
    for z in (-8, -16, -24):
        m.cyl(-6, 6, 11 - (-z) * 0.16, z, 1.6, None, axis='y', edge=0.25, carve=True)
    for side in ('+y', '-y'):
        for i in range(30):
            m.groove([(-12 + (i % 6) * 3, -32 + (i // 6) * 5), (-11 + (i % 6) * 3, -31 + (i // 6) * 5)], side,
                     depth=1, dark=0.6)
        m.decal(SKULL, -8, -12, side, (170, 172, 176), mode='raise')
        m.screw(6, 6, side, SCREW, kind='hex')
        m.screw(30, 6, side, SCREW, kind='hex')
        m.screw(80, 6, side, SCREW, kind='hex')
    m.decal(UAC, 50, Z_BORE - 2, '+y', WHITE, mode='paint')
    finish(m, 610, (0, 110, 0, Z_BORE + 5), grime=0.15, scratches=14, cracks=2)
    return m
