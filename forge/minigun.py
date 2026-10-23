# Brutal Doom: the minigun (chaingun slot), forge cube version. Free design, bold: six barrels in three clamp
# rings round a spinning hub (its own part), a fat motor housing with cooling fins and a red stripe, an ammo box
# hung on the left with a brass belt feeding into the side, a carry handle on top, twin spade grips at the back.
import math

from _common import (Model, fp, METAL, METAL_HI, METAL_MID, PANEL, PANEL_DK, RED, RED_HI, CAUTION, WHITE, GREEN,
                     BRASS, DARK, SCREW, UAC, ARROW, armour, corner_screws, hazard, worn_paint, finish, vents, mul)

Z_AXIS = 16.0
HOUSING = (20, 84, 2, 30, 26.0)
BARREL_R = 2.2
BARREL_RING = 6.0                      # how far each barrel sits off the axis


def build():
    m = Model("bd_minigun")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (30, 0, 0)
    hx0, hx1, hz0, hz1, hw = HOUSING
    armour(m, hx0, hx1, hw, hz0, hz1, fp.metal(METAL_MID), bevel=4.0, panel=PANEL_DK)
    vents(m, hx0 + 6, hx0 + 30, hz0 + 6, hz1 - 6, step=3.0)
    m.recolour(lambda x, y, z: 60 < x < 66, worn_paint(RED, RED_HI, 0.3, 701))
    m.cyl(hx1, hx1 + 8, 0, Z_AXIS, 11.0, fp.metal(METAL), edge=0.5)                    # front bearing
    m.part = 'barrels'
    for k in range(6):
        a = k * math.pi / 3
        yc, zc = math.cos(a) * BARREL_RING, Z_AXIS + math.sin(a) * BARREL_RING
        fp.barrel(m, hx1 + 8, 220, zc, BARREL_R, fp.metal(METAL_HI), bore=1.0, yc=yc)
    for x in (110, 160, 210):
        m.cyl(x, x + 4, 0, Z_AXIS, BARREL_RING + BARREL_R + 1.0, fp.metal(METAL), edge=0.25)
        for k in range(6):
            a = k * math.pi / 3
            m.cyl(x - 0.5, x + 4.5, math.cos(a) * BARREL_RING, Z_AXIS + math.sin(a) * BARREL_RING, BARREL_R,
                  fp.metal(METAL_HI), edge=0.25)
    m.cyl(hx1 + 8, 214, 0, Z_AXIS, 2.4, fp.metal(METAL_MID), edge=0.25)                 # the hub
    m.part = 'body'
    m.part = 'handle'
    # carry handle: an arch on top with a grip wrapped in tape
    for i in range(60):
        t = i / 59
        x, z = 34 + t * 40, hz1 + math.sin(t * math.pi) * 12
        m.ball(x, 0, z, 2.0, fp.metal(METAL) if t < 0.2 or t > 0.8 else (34, 34, 36), edge=0.25)
    m.part = 'grips'
    # spade grips at the back, a thumb trigger between them
    for y in (-8, 8):
        m.cyl(-14, hx0, y, 10, 2.4, fp.metal(METAL), edge=0.25)
        m.cyl(2, 20, -14, y, 3.0, (36, 36, 38), axis='z', edge=0.25)
    m.cbox(-16, -12, 4.0, 8, 12, fp.metal((200, 40, 30)), size=0.5)
    # the ammo box on the left, hazard-striped, and the brass belt into the side
    m.part = 'ammo'
    armour(m, 30, 70, 14.0, -26, 2, fp.metal(PANEL), bevel=2.0)
    hazard(m, 30, 70, -8, 8, -26, -20)
    for i in range(16):
        x = 34 + i * 2
        m.box(x, x + 1.5, 9, 12, -2 + i * 0.6, 2 + i * 0.6, BRASS, size=0.25)
        m.box(x, x + 1.5, 9, 12, -2 + i * 0.6, -0.5 + i * 0.6, (120, 80, 30), size=0.25)
    m.part = 'body'
    for side in ('+y', '-y'):
        m.decal(UAC, 26, 26, side, WHITE, mode='paint')
        m.decal(ARROW, 70, 24, side, WHITE, mode='paint')
    m.box(80, 82, 5, 6, 26, 28, GREEN, size=0.25)
    m.box(80, 82, -6, -5, 26, 28, GREEN, size=0.25)
    corner_screws(m, hx0, hx1, hz0, hz1, inset=4, kind='hex')
    finish(m, 710, (hx0, hx1, hz0, hz1), grime=0.25, scratches=16, cracks=2)
    return m
