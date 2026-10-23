# Brutal Doom: the assault rifle (Rifle slot), forge cube version. Free design, bold: a UAC service rifle: a long
# angular receiver in gun metal with a dark-red upper, a curved magazine with a brass round showing, an under-barrel
# shroud with diagonal heat slots, a box sight with a green dot, a big muzzle brake, and a solid stock with a cheek
# piece and a hazard-striped butt.
from _common import (Model, fp, METAL, METAL_HI, METAL_MID, PANEL, PANEL_DK, RED, RED_HI, CAUTION, WHITE, GREEN,
                     BRASS, DARK, SCREW, UAC, ARROW, armour, corner_screws, hazard, worn_paint, finish, vents)

Z_BORE = 16.0


def build():
    m = Model("bd_assault_rifle")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (72, 0, 0)
    armour(m, 50, 150, 12.0, 2, 18, fp.metal(METAL_MID), bevel=2.0, panel=PANEL)
    m.cprism([(54, 18), (54, 22), (60, 26), (140, 26), (148, 22), (148, 18)], 11.0,
             worn_paint(RED, RED_HI, 0.3, 1301), bevel=2.0, edge=0.5)
    m.part = 'stock'
    # stock: solid, a cheek piece, a hazard-striped butt
    m.cprism([(0, -14), (0, 20), (6, 24), (50, 22), (50, 4), (30, -2), (8, -14)], 11.0, fp.metal(METAL),
             bevel=2.5, edge=0.5)
    m.cbox(10, 40, 9.0, 22, 26, fp.metal(PANEL_DK), bevel=1.0, edge=0.25)
    hazard(m, -1, 4, -10, 10, -14, 22, step=2.0)
    # magazine, curved, a brass round on top
    m.part = 'mag'
    m.cprism([(100, 2), (99, -12), (103, -26), (115, -28), (114, -12), (115, 2)], 8.0, fp.metal(METAL_HI),
             bevel=1.0, edge=0.5)
    m.cyl(103, 112, 0, 2.5, 1.2, BRASS, size=0.25, edge=0.25)                          # the top round
    m.part = 'body'
    m.part = 'handguard'
    # the front: a shroud with diagonal slots under a barrel, the muzzle brake
    m.cbox(150, 210, 12.0, 4, 20, fp.metal(METAL), bevel=2.0, edge=0.5)
    vents(m, 156, 204, 7, 17, step=5.0, slant=3.0)
    m.part = 'barrel'
    fp.barrel(m, 210, 250, Z_BORE, 2.2, fp.metal(METAL_MID), bore=1.2)
    m.cbox(240, 256, 8.0, Z_BORE - 3.5, Z_BORE + 3.5, fp.metal(METAL_HI), bevel=1.5, edge=0.25)
    for x in (243, 247, 251):
        for side in ('+y', '-y'):
            m.groove([(x, Z_BORE - 2), (x, Z_BORE + 2)], side, depth=3, width=2, dark=0.15)
    m.cyl(255, 257, 0, Z_BORE, 1.2, None, edge=0.25, carve=True)
    m.part = 'sight'
    # box sight with a green dot, a front post
    m.cbox(100, 124, 9.0, 26, 34, fp.metal(METAL), bevel=1.0, edge=0.5)
    m.cbox(99, 125, 5.0, 28, 32, None, size=0.5, carve=True)
    m.box(118, 118.5, -0.25, 0.25, 29.75, 30.25, GREEN, size=0.25)
    fp.sight_post(m, 204, 20, 8.0, fp.metal(METAL), w=1.5, dot=GREEN)
    m.part = 'grip'
    # grip, guard, trigger
    m.cprism([(76, 2), (68, 0), (62, -16), (72, -18), (80, -4), (84, 2)], 9.0, fp.metal(METAL), bevel=2.0,
             edge=0.5)
    m.part = 'guard'
    fp.guard(m, 82, 98, -7, 2, fp.metal(METAL))
    fp.trigger(m, 88, 2, fp.metal(METAL_HI), length=5)
    for side in ('+y', '-y'):
        m.decal(UAC, 60, 14, side, WHITE, mode='paint')
        m.decal(ARROW, 134, 14, side, WHITE, mode='paint')
        m.bolt(20, 4, side, SCREW)
    m.part = 'body'
    m.box(126, 128, 5.5, 6.25, 20, 22, GREEN, size=0.25)
    corner_screws(m, 50, 150, 2, 18, inset=3, kind='hex')
    finish(m, 1310, (50, 210, 2, 26), grime=0.2, scratches=18, cracks=3)
    return m
