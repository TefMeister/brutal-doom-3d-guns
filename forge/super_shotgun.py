# Brutal Doom: the Super Shotgun (SSG), forge cube version. Free design, bold: two fat side-by-side barrels in a
# heavy steel jacket with heat-cut windows and brass end rings, a hinge block with a huge pin and a top lever, a sawn
# stock wrapped in leather straps, a carved skull on the action and red worn paint on the fore-end.
from _common import (Model, fp, METAL, METAL_HI, METAL_MID, PANEL, RED, RED_HI, WHITE, GREEN, BRASS, DARK, SCREW,
                     SKULL, armour, corner_screws, worn_paint, finish, mul)

LEATHER = (92, 56, 32)
LEATHER_DK = (54, 30, 16)
Z_BORE = 14.0
GAP = 3.6
BARRELS = (60, 230, 3.4, 2.4)
ACTION = (30, 62, -2, 22, 15.0)
FOREEND = (66, 140, 0, 9, 13.0)
STOCK = [(-30, -20), (-34, -12), (-20, 14), (32, 18), (32, 2), (10, -4), (-6, -20)]


def build():
    m = Model("bd_super_shotgun")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (24, 0, 0)
    bx0, bx1, br, bore = BARRELS
    m.part = 'barrels'
    for y in (-GAP, GAP):
        fp.barrel(m, bx0, bx1, Z_BORE, br, fp.metal(METAL_MID), bore=bore, yc=y, muzzle_ring=(br + 0.5, 3, BRASS))
    m.part = 'jacket'
    # the jacket over both barrels: a long box, windows cut along its sides showing the barrels inside
    m.cbox(bx0 + 4, bx1 - 30, 2 * GAP + 2 * br + 2, Z_BORE - br - 1, Z_BORE + br + 1.5, fp.metal(METAL),
           bevel=1.5, edge=0.5)
    for x in range(bx0 + 12, bx1 - 40, 14):
        for side in ('+y', '-y'):
            m.groove([(x, Z_BORE - 1.5), (x + 8, Z_BORE - 1.5)], side, depth=2, width=6, dark=0.25)
        m.groove([(x, -1.5), (x + 8, -1.5)], '+z', depth=2, width=3, dark=0.25)
    m.cbox(bx1 - 32, bx1 - 26, 2 * GAP + 2 * br + 3, Z_BORE - br - 1.5, Z_BORE + br + 2, fp.metal(METAL_HI),
           bevel=1.0, edge=0.25)
    m.part = 'sight'
    m.box(bx1 - 6, bx1 - 4, -0.75, 0.75, Z_BORE + br + 0.5, Z_BORE + br + 2.5, GREEN, size=0.25)   # front bead
    ax0, ax1, az0, az1, aw = ACTION
    m.part = 'body'
    armour(m, ax0, ax1, aw, az0, az1, fp.metal(METAL_MID), bevel=2.0, panel=PANEL)
    m.part = 'hinge'
    m.cyl(-aw / 2 - 1, aw / 2 + 1, ax1 - 3, 4, 3.0, fp.metal(METAL_HI), axis='y', edge=0.25)   # the hinge pin
    for y in (-aw / 2 - 1.25, aw / 2 + 0.75):
        m.box(ax1 - 4, ax1 - 2, y, y + 0.5, 3.5, 4.5, DARK, size=0.25)
    m.part = 'lever'
    m.cprism([(ax0 + 4, az1), (ax0 + 4, az1 + 2), (ax0 + 22, az1 + 3), (ax0 + 24, az1 + 1), (ax0 + 20, az1)], 4.0,
             fp.metal(METAL_HI), size=0.5, edge=0.25)
    m.part = 'body'
    ux0, ux1, uz0, uz1, uw = FOREEND
    m.part = 'foreend'
    m.cbox(ux0, ux1, uw, uz0, uz1, worn_paint(RED, RED_HI, 0.3, 301), bevel=2.0, bevel_x=1.0, edge=0.5)
    for x in range(ux0 + 6, ux1 - 4, 5):
        for side in ('+y', '-y'):
            m.groove([(x, uz0 + 1), (x + 2, uz1 - 1)], side, depth=2, dark=0.35)
    m.part = 'stock'
    # the sawn stock wrapped in leather straps, its cut end left rough
    m.cprism(STOCK, 12.0, fp.wood(LEATHER, LEATHER_DK), bevel=3.0, edge=0.5)
    for x0 in (-20, -6, 8):                                         # black straps wound round the stock
        m.recolour(lambda x, y, z, a=x0: 0 <= (x - a) - (z + 22) * 0.2 < 3.5, (34, 30, 28))
        for side in ('+y', '-y'):
            m.groove([(x0, -22), (x0 + 8.4, 20)], side, depth=1, dark=0.5)
    for i in range(12):
        m.box(-35, -33, -6 + i, -5 + i, -14 + (i % 3) * 3, -12 + (i % 3) * 3, None, size=0.5, carve=True)
    m.part = 'guard'
    fp.guard(m, 40, 58, -10, az0, fp.metal(METAL))
    fp.trigger(m, 46, az0, fp.metal(METAL_HI), length=6)
    fp.trigger(m, 52, az0, fp.metal(METAL_HI), length=6)
    m.decal(SKULL, 39, 16, '+y', WHITE, mode='carve')
    m.decal(SKULL, 39, 16, '-y', WHITE, mode='carve')
    corner_screws(m, ax0, ax1, az0, az1, inset=3, kind='hex')
    for side in ('+y', '-y'):
        for x in (ux0 + 3, ux1 - 3):
            m.bolt(x, (uz0 + uz1) / 2, side, SCREW)
    finish(m, 310, (ax0, bx1 - 30, -2, Z_BORE + 4), grime=0.18, scratches=18, cracks=3)
    return m
