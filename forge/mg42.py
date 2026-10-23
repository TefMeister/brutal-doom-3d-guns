# Brutal Doom: the MG42, forge cube version. Faithful in shape, Brutal Doom in finish: the long perforated barrel
# jacket with its oval cooling holes, the square receiver with the feed cover on top, a belt of brass hanging out of the
# left, the bipod folded forward, a wooden stock and pistol grip, a muzzle booster cone.
import math

from _common import (Model, fp, METAL, METAL_HI, METAL_MID, PANEL, WHITE, BRASS, DARK, SCREW, finish, mul)

WOOD = (110, 66, 36)
WOOD_DK = (64, 34, 16)
Z_BORE = 16.0


def build():
    m = Model("bd_mg42")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (64, 0, 0)
    m.cbox(40, 110, 12.0, 4, 26, fp.metal(METAL_MID), bevel=1.5, edge=0.5)                 # receiver
    m.part = 'cover'
    m.cbox(50, 108, 12.5, 24, 30, fp.metal(METAL), bevel=1.5, edge=0.5)                    # feed cover
    m.part = 'body'
    m.part = 'sight'
    m.cbox(60, 74, 3.0, 30, 34, fp.metal(METAL), size=0.5)                                 # rear sight
    m.part = 'jacket'
    # the jacket: a long square-ish tube with rows of oval holes
    m.cbox(110, 230, 11.0, Z_BORE - 5.5, Z_BORE + 5.5, fp.metal(METAL), bevel=2.0, edge=0.5)
    for x in range(116, 222, 8):
        for side in ('+y', '-y'):
            m.groove([(x, Z_BORE - 0.5), (x + 4, Z_BORE - 0.5)], side, depth=4, width=4, dark=0.15)
        m.groove([(x, -1.5), (x + 4, -1.5)], '+z', depth=4, width=6, dark=0.15)
    m.part = 'barrel'
    fp.barrel(m, 114, 240, Z_BORE, 2.2, fp.metal(METAL_HI), bore=1.2)
    m.cyl(230, 246, 0, Z_BORE, 4.0, fp.metal(METAL), r1=5.0, edge=0.25)                    # booster cone
    m.cyl(244, 247, 0, Z_BORE, 2.0, None, edge=0.25, carve=True)
    m.part = 'sight'
    m.cbox(222, 226, 3.0, Z_BORE + 5, Z_BORE + 12, fp.metal(METAL), size=0.5)              # front sight
    m.part = 'bipod'
    # bipod folded forward under the jacket
    for y in (-4, 4):
        m.box(124, 176, y - 0.75, y + 0.75, Z_BORE - 8, Z_BORE - 6.5, fp.metal(METAL_HI), size=0.5)
        m.box(174, 178, y - 1.25, y + 1.25, Z_BORE - 9, Z_BORE - 6, fp.metal(METAL), size=0.5)
    m.part = 'stock'
    # wooden stock and grip
    m.cprism([(-10, -10), (-10, 20), (-4, 22), (40, 22), (40, 6), (20, 2), (-4, -10)], 10.0,
             fp.wood(WOOD, WOOD_DK), bevel=2.5, edge=0.5)
    m.cbox(-12, -10, 10.5, -11, 21, fp.metal(METAL), size=0.5)
    m.part = 'grip'
    m.cprism([(66, 4), (58, 4), (52, -16), (62, -18), (68, -4), (74, 4)], 9.0, fp.wood(WOOD, WOOD_DK), bevel=2.0,
             edge=0.5)
    m.part = 'guard'
    fp.guard(m, 70, 86, -6, 4, fp.metal(METAL))
    fp.trigger(m, 76, 4, fp.metal(METAL_HI), length=5)
    m.part = 'belt'
    # the belt hanging out of the left side
    for i in range(24):
        t = i / 23
        x = 78 - t * 4
        z = 20 - t * 30 - math.sin(t * 3) * 3
        y = 7 + t * 4
        m.cyl(x - 3, x + 4, y, z, 1.1, BRASS, edge=0.25)
        m.box(x - 3.5, x + 4.5, y - 0.5, y + 0.5, z - 1.5, z - 1.0, fp.metal(METAL), size=0.25)
    for side in ('+y', '-y'):
        for x in (44, 104):
            m.screw(x, 8, side, SCREW, kind='slot')
        m.screw(60, 20, side, SCREW, kind='hex')
    finish(m, 1510, (40, 230, 4, 26), grime=0.25, scratches=16, cracks=2)
    return m
