# Brutal Doom: the Devastator (Duke's twin mini-rocket launcher), forge cube version. Free design, bold: two
# rotating clusters of four mini-rocket tubes side by side on one armoured body, red-tipped rockets showing, a yellow
# and black painted housing, a big side magazine drum, a top handle and a reflex sight.
import math

from _common import (Model, fp, METAL, METAL_HI, METAL_MID, PANEL, PANEL_DK, CAUTION, WHITE, GREEN, DARK, SCREW,
                     ARROW, armour, corner_screws, hazard, finish, vents)

YELLOW = (206, 160, 40)
Z_AXIS = 18.0


def build():
    m = Model("bd_devastator")
    m.pivot = (50, 0, 0)
    armour(m, 20, 96, 30.0, 2, 34, fp.metal(YELLOW, 0.08), bevel=3.0, panel=PANEL_DK)
    hazard(m, 20, 30, -16, 16, 2, 34, step=2.5)
    for y in (-8, 8):
        m.part = 'cluster_l' if y > 0 else 'cluster_r'
        m.cyl(96, 104, y, Z_AXIS, 7.5, fp.metal(METAL), edge=0.25)
        for k in range(4):
            a = k * math.pi / 2 + math.pi / 4
            yc, zc = y + math.cos(a) * 4, Z_AXIS + math.sin(a) * 4
            m.cyl(100, 170, yc, zc, 2.4, fp.metal(METAL_MID), edge=0.25)
            m.cyl(166, 171, yc, zc, 1.5, None, edge=0.25, carve=True)
            m.cyl(163, 166, yc, zc, 1.5, (200, 34, 26), r1=0.6, edge=0.25)
        for x in (124, 150, 166):
            m.cyl(x, x + 3, y, Z_AXIS, 7.0, fp.metal(METAL_HI), edge=0.25)
    m.part = 'body'
    # the side magazine drum on the left
    m.cyl(15, 25, 58, 14, 10.0, fp.metal(PANEL), axis='y', edge=0.5)
    m.cyl(25, 26, 58, 14, 4.0, fp.metal(METAL_HI), axis='y', edge=0.25)
    # top handle, reflex sight, grip, fore-grip
    for i in range(50):
        t = i / 49
        m.ball(30 + t * 50, 0, 34 + math.sin(t * math.pi) * 10, 2.0, fp.metal(METAL), edge=0.25)
    m.cbox(84, 94, 6.0, 34, 36, fp.metal(METAL), size=0.5)
    m.prism([(86, 36), (86, 44), (92, 44), (92, 36)], -3, 3, fp.metal(METAL), size=0.5)
    m.prism([(87, 37), (87, 43), (91, 43), (91, 37)], -2, 2, None, size=0.5, carve=True)
    m.box(89, 89.5, -0.25, 0.25, 40, 40.5, (255, 40, 30), size=0.25)
    m.cprism([(46, 2), (38, 0), (32, -18), (42, -20), (50, -6), (56, 2)], 10.0, fp.metal(METAL), bevel=2.0, edge=0.5)
    fp.guard(m, 54, 68, -6, 2, fp.metal(METAL))
    fp.trigger(m, 60, 2, fp.metal(METAL_HI), length=6)
    m.cprism([(110, Z_AXIS - 8), (106, -12), (114, -14), (120, Z_AXIS - 8)], 8.0, fp.metal(METAL), bevel=1.5,
             edge=0.5)
    vents(m, 70, 92, 8, 28, step=4.0)
    for side in ('+y', '-y'):
        m.decal(ARROW, 34, 28, side, DARK, dot=2, mode='paint')
    corner_screws(m, 20, 96, 2, 34, inset=4, kind='hex')
    finish(m, 2610, (20, 96, 2, 34), grime=0.25, scratches=18, cracks=3)
    return m
