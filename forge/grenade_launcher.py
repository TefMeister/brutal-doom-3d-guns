# Brutal Doom: the grenade launcher, forge cube version. Free design, bold: a six-shot revolving launcher: a big
# cylinder drum with grenade noses showing green, a short fat barrel with a heavy front ring, a folding ladder sight,
# a skeleton stock, a fore-grip, hazard stripes round the drum.
import math

from _common import (Model, fp, METAL, METAL_HI, METAL_MID, PANEL, PANEL_DK, CAUTION, WHITE, GREEN, DARK, SCREW, UAC,
                     armour, corner_screws, hazard, finish)

Z_AXIS = 16.0
NADE = (70, 110, 50)


def build():
    m = Model("bd_grenade_launcher")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (48, 0, 0)
    armour(m, 30, 70, 14.0, 2, 26, fp.metal(METAL_MID), bevel=2.5, panel=PANEL)
    # the drum
    m.part = 'drum'
    m.cyl(70, 110, 0, Z_AXIS, 14.0, fp.metal(PANEL_DK), edge=0.5)
    for k in range(6):
        a = k * math.pi / 3
        yc, zc = math.cos(a) * 8.5, Z_AXIS + math.sin(a) * 8.5
        m.cyl(70, 111, yc, zc, 3.4, None, edge=0.25, carve=True)
        m.cyl(106, 110, yc, zc, 3.4, NADE, edge=0.25)
        m.cyl(105.5, 106, yc, zc, 3.4, (200, 170, 60), size=0.25, edge=0.25)
    hazard(m, 70, 76, -16, 16, 0, 32, step=2.0)
    m.cyl(68, 112, 0, Z_AXIS, 2.4, fp.metal(METAL_HI), edge=0.25)
    m.part = 'body'
    m.part = 'barrel'
    # barrel and front ring, a frame round the drum
    m.cyl(110, 150, 0, Z_AXIS + 8.5, 4.6, fp.metal(METAL), edge=0.25)
    m.cyl(144, 152, 0, Z_AXIS + 8.5, 5.6, fp.metal(METAL_HI), edge=0.25)
    m.cyl(146, 153, 0, Z_AXIS + 8.5, 3.4, None, edge=0.25, carve=True)
    m.part = 'frame'
    for z in (Z_AXIS - 15, Z_AXIS + 15):
        m.cbox(70, 112, 4.0, z - 1, z + 1, fp.metal(METAL), size=0.5)
    m.cbox(110, 116, 10.0, Z_AXIS - 16, Z_AXIS + 14, fp.metal(METAL), bevel=1.5, edge=0.5)
    m.part = 'sight'
    # ladder sight
    m.cbox(126, 132, 6.0, Z_AXIS + 13, Z_AXIS + 15, fp.metal(METAL), size=0.5)
    for y in (-2.5, 2.0):
        m.box(128, 130, y, y + 0.5, Z_AXIS + 15, Z_AXIS + 24, fp.metal(METAL), size=0.25)
    for z in range(int(Z_AXIS) + 16, int(Z_AXIS) + 24, 2):
        m.box(128, 130, -2.5, 2.5, z, z + 0.25, GREEN if z == int(Z_AXIS) + 20 else fp.metal(METAL_HI), size=0.25)
    m.part = 'stock'
    # skeleton stock, grip, fore-grip
    m.cprism([(-10, -6), (-10, 22), (30, 24), (30, 6), (10, -6)], 8.0, fp.metal(METAL), bevel=2.0, edge=0.5)
    m.prism([(-4, 0), (-4, 16), (24, 18), (24, 8), (10, 0)], -5, 5, None, size=0.5, carve=True)
    m.part = 'grip'
    m.cprism([(44, 2), (36, 0), (30, -18), (40, -20), (48, -6), (52, 2)], 9.0, fp.metal(METAL), bevel=2.0, edge=0.5)
    m.part = 'guard'
    fp.guard(m, 50, 66, -7, 2, fp.metal(METAL))
    fp.trigger(m, 56, 2, fp.metal(METAL_HI), length=6)
    m.part = 'foregrip'
    m.cprism([(118, Z_AXIS - 15), (114, -14), (122, -16), (126, Z_AXIS - 15)], 7.0, fp.metal(METAL), bevel=1.5,
             edge=0.5)
    for side in ('+y', '-y'):
        m.decal(UAC, 36, 22, side, WHITE, mode='paint')
    corner_screws(m, 30, 70, 2, 26, inset=3, kind='hex')
    finish(m, 1710, (30, 116, 2, 30), grime=0.2, scratches=14, cracks=2)
    return m
