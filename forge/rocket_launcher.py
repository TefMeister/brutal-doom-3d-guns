# Brutal Doom: the rocket launcher, forge cube version. Free design, bold: a fat launch tube in an armoured shroud
# with a flared, scorched muzzle, a rotating four-rocket drum behind the grip (its own part) with red warheads peeking
# out, a side-mounted box sight with a green reticle, hazard stripes on the shroud, and a back blast cone.
import math

from _common import (Model, fp, METAL, METAL_HI, METAL_MID, PANEL, PANEL_DK, RED, RED_HI, CAUTION, WHITE, GREEN,
                     ORANGE, DARK, SCREW, UAC, HAZARD_TRI, armour, corner_screws, hazard, worn_paint, finish, vents,
                     mul, hash01)

Z_AXIS = 18.0
TUBE = (0, 200, 9.0)


def build():
    m = Model("bd_rocket_launcher")
    m.pivot = (80, 0, 0)
    tx0, tx1, tr = TUBE
    m.cyl(tx0 + 20, tx1, 0, Z_AXIS, tr, fp.metal(METAL_MID), edge=0.5)
    m.cyl(tx1 - 1, tx1 + 12, 0, Z_AXIS, tr + 1, fp.metal(METAL), r1=tr + 4, edge=0.25)        # flared muzzle
    m.cyl(tx1 - 2, tx1 + 13, 0, Z_AXIS, tr - 1.5, None, r1=tr + 2.5, edge=0.25, carve=True)
    m.cyl(tx1 - 3, tx1 - 2, 0, Z_AXIS, tr - 1.5, (24, 18, 14), size=0.25, edge=0.25)
    m.recolour(lambda x, y, z: x > tx1 - 4 and hash01(int(x), int(z), 811) > 0.4, (20, 16, 12))                  # soot
    m.cyl(tx0, tx0 + 22, 0, Z_AXIS, tr + 1, fp.metal(METAL), r1=tr - 1, edge=0.25)           # back blast cone
    m.cyl(tx0 - 1, tx0 + 6, 0, Z_AXIS, tr - 2, None, edge=0.25, carve=True)
    # armoured shroud over the middle, red paint, hazard band
    armour(m, 60, 150, 2 * tr + 6, Z_AXIS - tr - 2, Z_AXIS + tr + 3, worn_paint(RED, RED_HI, 0.3, 801),
           bevel=4.0)
    hazard(m, 138, 150, -20, 20, Z_AXIS - 20, Z_AXIS + 20, step=2.5)
    vents(m, 70, 100, Z_AXIS + 2, Z_AXIS + 8, step=4.0, glow=(110, 40, 20))
    # the rocket drum behind the grip, four rockets showing red tips
    m.part = 'drum'
    m.cyl(26, 58, 0, Z_AXIS, tr + 6, fp.metal(PANEL), edge=0.5)
    for k in range(4):
        a = k * math.pi / 2 + math.pi / 4
        yc, zc = math.cos(a) * 9.5, Z_AXIS + math.sin(a) * 9.5
        m.cyl(25, 59, yc, zc, 3.4, None, edge=0.25, carve=True)
        m.cyl(30, 54, yc, zc, 3.0, fp.metal((90, 92, 80)), edge=0.25)
        m.cyl(54, 58, yc, zc, 3.0, (190, 30, 24), r1=1.0, edge=0.25)
    for x in (28, 54):
        m.cyl(x, x + 2, 0, Z_AXIS, tr + 6.5, fp.metal(METAL), edge=0.25)
    m.part = 'body'
    # grip, trigger, front grip
    m.cprism([(96, 6), (88, 4), (84, -14), (94, -16), (100, -2)], 9.0, fp.metal(METAL), bevel=2.0, edge=0.5)
    fp.guard(m, 98, 114, -6, Z_AXIS - tr - 1, fp.metal(METAL))
    fp.trigger(m, 104, Z_AXIS - tr - 1, fp.metal(METAL_HI), length=6)
    m.cprism([(160, 8), (154, -12), (162, -14), (168, 8)], 8.0, fp.metal(METAL), bevel=2.0, edge=0.5)
    # the box sight on the left: a housing with a green reticle at the back
    m.cbox(100, 128, 10.0, Z_AXIS + tr + 3, Z_AXIS + tr + 13, fp.metal(METAL), bevel=1.0, edge=0.5)
    m.cbox(99, 129, 6.0, Z_AXIS + tr + 5, Z_AXIS + tr + 11, None, size=0.5, carve=True)
    for dy, dz in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
        m.box(100 + 0.0, 100.25, dy * 0.75 - 0.25, dy * 0.75 + 0.25, Z_AXIS + tr + 8 + dz * 0.75 - 0.25,
              Z_AXIS + tr + 8 + dz * 0.75 + 0.25, GREEN, size=0.25)
    for side in ('+y', '-y'):
        m.decal(UAC, 108, Z_AXIS + 8, side, WHITE, mode='paint')
        m.decal(HAZARD_TRI, 124, Z_AXIS + 6, side, CAUTION, mode='paint')
        for x in (64, 146, 30, 54):
            m.bolt(x, Z_AXIS - 6, side, SCREW)
    corner_screws(m, 60, 150, Z_AXIS - tr - 2, Z_AXIS + tr + 3, inset=4, kind='hex')
    finish(m, 810, (60, 150, Z_AXIS - tr, Z_AXIS + tr), grime=0.25, scratches=16, cracks=3)
    return m

