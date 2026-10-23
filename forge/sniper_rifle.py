# Brutal Doom: the sniper rifle, forge cube version. Free design, bold: a long heavy anti-materiel rifle: a fluted
# bull barrel ending in a huge two-chamber muzzle brake, a bolt handle with a ball knob, a big scope with turrets and
# a green-tinted lens, a skeleton stock with an adjustable cheek rest and a spike, a bipod, worn dark-red panels.
from _common import (Model, fp, METAL, METAL_HI, METAL_MID, PANEL, PANEL_DK, RED, RED_HI, CAUTION, WHITE, GREEN,
                     DARK, SCREW, UAC, ARROW, armour, corner_screws, worn_paint, finish, vents)

Z_BORE = 16.0
LENS = (60, 140, 90)


def build():
    m = Model("bd_sniper_rifle")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (80, 0, 0)
    armour(m, 60, 140, 12.0, 4, 22, worn_paint(RED, RED_HI, 0.25, 1601), bevel=2.0, panel=PANEL_DK)
    m.part = 'stock'
    # skeleton stock
    m.cprism([(0, -12), (0, 18), (60, 20), (60, 6), (40, 0), (10, -12)], 9.0, fp.metal(METAL), bevel=2.0, edge=0.5)
    m.prism([(8, -4), (8, 10), (48, 12), (48, 4), (34, 0)], -5, 5, None, size=0.5, carve=True)
    m.cbox(6, 40, 7.0, 20, 25, fp.metal(PANEL), bevel=1.0, edge=0.25)
    m.cbox(-2, 0, 9.5, -13, 19, (30, 30, 32), size=0.5)
    m.cprism([(4, -12), (6, -20), (8, -12)], 2.0, fp.metal(METAL_HI), size=0.5)             # monopod spike
    m.part = 'barrel'
    # barrel: fluted bull barrel and the big brake
    fp.barrel(m, 140, 300, Z_BORE, 3.6, fp.metal(METAL_MID), bore=1.6)
    for side in ('+y', '-y', '+z'):
        for off in (-1.5, 1.5):
            pts = [(146, Z_BORE + off), (280, Z_BORE + off)] if side != '+z' else [(146, off), (280, off)]
            m.groove(pts, side, depth=2, dark=0.4)
    m.cbox(292, 314, 12.0, Z_BORE - 5, Z_BORE + 5, fp.metal(METAL), bevel=2.0, edge=0.5)
    for x0 in (295, 304):
        m.cbox(x0, x0 + 5, 14.0, Z_BORE - 3.5, Z_BORE + 3.5, None, size=0.5, carve=True)
    m.cyl(313, 315, 0, Z_BORE, 1.6, None, edge=0.25, carve=True)
    # bolt with a ball knob on the right
    m.part = 'bolt'
    m.cyl(-14, -6, 104, 18, 1.0, fp.metal(METAL_HI), axis='y', edge=0.25)
    m.ball(104, -15, 18, 2.4, fp.metal(METAL_HI), edge=0.25)
    m.part = 'body'
    m.part = 'scope'
    # scope with rings, turrets and a green-tinted lens
    for x in (80, 124):
        m.cbox(x, x + 4, 7.0, 22, 30, fp.metal(METAL), size=0.5)
    m.cyl(60, 150, 0, 32, 4.2, fp.metal(METAL), edge=0.25)
    m.cyl(140, 160, 0, 32, 6.5, fp.metal(METAL), r1=7.5, edge=0.25)
    m.cyl(60, 72, 0, 32, 5.5, fp.metal(METAL_MID), edge=0.25)
    m.cyl(159.5, 160.5, 0, 32, 6.0, LENS, size=0.25, edge=0.25)
    m.cyl(59.5, 60.5, 0, 32, 4.5, LENS, size=0.25, edge=0.25)
    m.cyl(36, 42, 100, 0, 2.6, fp.metal(METAL_HI), axis='z', edge=0.25)
    m.cyl(-8, 8, 100, 32, 2.6, fp.metal(METAL_HI), axis='y', edge=0.25)
    m.part = 'bipod'
    # bipod folded under, grip, guard
    for y in (-4, 4):
        m.box(150, 210, y - 0.75, y + 0.75, 11, 12.5, fp.metal(METAL_HI), size=0.5)
    m.cbox(146, 152, 12.0, 6, 12, fp.metal(METAL), size=0.5)
    m.part = 'grip'
    m.cprism([(76, 4), (68, 2), (62, -16), (72, -18), (80, -4), (84, 4)], 9.0, fp.metal(METAL), bevel=2.0, edge=0.5)
    m.part = 'guard'
    fp.guard(m, 82, 98, -6, 4, fp.metal(METAL))
    fp.trigger(m, 88, 4, fp.metal(METAL_HI), length=5)
    m.part = 'mag'
    m.cbox(106, 122, 8.0, -8, 4, fp.metal(METAL_HI), bevel=1.0, edge=0.5)
    m.part = 'body'
    for side in ('+y', '-y'):
        m.decal(UAC, 64, 18, side, WHITE, mode='paint')
        m.decal(ARROW, 126, 18, side, CAUTION, mode='paint')
    corner_screws(m, 60, 140, 4, 22, inset=3, kind='hex')
    finish(m, 1610, (60, 300, 4, 22), grime=0.18, scratches=18, cracks=2)
    return m
