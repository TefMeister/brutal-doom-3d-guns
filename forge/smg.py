# Brutal Doom: the SMG, forge cube version. Free design, bold: a compact bullpup-ish box in grey panels and gun metal,
# a long side-loading magazine on the left, a vertical fore-grip, a fat suppressor-like compensator with heat holes,
# a top rail with a green holo sight, and a folding wire stock.
from _common import (Model, fp, METAL, METAL_HI, METAL_MID, PANEL, PANEL_DK, RED, CAUTION, WHITE, GREEN, DARK, SCREW,
                     UAC, ARROW, armour, corner_screws, hazard, finish, vents)

Z_BORE = 12.0


def build():
    m = Model("bd_smg")
    m.pivot = (36, 0, 0)
    armour(m, 10, 96, 12.0, 0, 22, fp.metal(PANEL), bevel=2.5, panel=PANEL_DK)
    m.cbox(14, 94, 6.0, 22, 24, fp.metal(METAL), size=0.5)
    for x in range(16, 92, 3):
        m.box(x, x + 1, -3, 3, 23.25, 24, None, size=0.25, carve=True)
    # magazine sticking out of the left side, straight out, with a red base
    m.part = 'mag'
    m.box(52, 62, 6, 34, 4, 14, fp.metal(METAL_MID), size=1.0, edge=0.5, bevel=1.0)
    m.box(52, 62, 34, 36, 3, 15, fp.metal(RED), size=0.5)
    for y in range(10, 32, 4):
        m.groove([(53, y), (61, y)], '+z', depth=1, dark=0.5)                      # ribs across the top
    m.part = 'body'
    # compensator with heat holes
    m.cyl(96, 128, 0, Z_BORE, 4.5, fp.metal(METAL), edge=0.25)
    for x in range(100, 124, 4):
        for side in ('+y', '-y', '+z'):
            m.groove([(x, Z_BORE) if side != '+z' else (x, 0), (x + 1, Z_BORE) if side != '+z' else (x + 1, 0)],
                     side, depth=3, width=3, col=(150, 60, 20))
    m.cyl(127, 129, 0, Z_BORE, 1.4, None, edge=0.25, carve=True)
    # fore-grip, pistol grip, guard
    m.cprism([(80, 0), (76, -18), (84, -20), (88, 0)], 7.0, fp.metal(METAL), bevel=1.5, edge=0.5)
    m.cprism([(36, 2), (28, 0), (24, -18), (34, -20), (40, -6), (44, 2)], 9.0, fp.metal(METAL), bevel=2.0, edge=0.5)
    fp.guard(m, 42, 56, -7, 0, fp.metal(METAL))
    fp.trigger(m, 48, 0, fp.metal(METAL_HI), length=5)
    # holo sight: a frame with a green dot
    m.cbox(40, 58, 8.0, 24, 26, fp.metal(METAL), size=0.5)
    m.prism([(42, 26), (42, 34), (56, 34), (56, 26)], -4, 4, fp.metal(METAL), size=0.5)
    m.prism([(43, 27), (43, 33), (55, 33), (55, 27)], -3, 3, None, size=0.5, carve=True)
    m.box(49, 49.5, -0.25, 0.25, 30, 30.5, GREEN, size=0.25)
    m.box(43, 43.5, -3, 3, 27, 33, (60, 120, 90), size=0.25)
    # the folding wire stock
    for z in (4, 18):
        m.box(-28, 10, 6, 7, z, z + 1, fp.metal(METAL_HI), size=0.5)
        m.box(-28, 10, -7, -6, z, z + 1, fp.metal(METAL_HI), size=0.5)
    m.cbox(-30, -27, 15.0, 0, 22, fp.metal(METAL), bevel=1.0, edge=0.25)
    for side in ('+y', '-y'):
        m.decal(UAC, 66, 18, side, WHITE, mode='paint')
        m.decal(ARROW, 80, 18, side, CAUTION, mode='paint')
    corner_screws(m, 10, 96, 0, 22, inset=3, kind='hex')
    finish(m, 1210, (10, 96, 0, 22), grime=0.18, scratches=12, cracks=2)
    return m
