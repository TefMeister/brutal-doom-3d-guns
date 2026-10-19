# Brutal Doom: the assault shotgun (an AA-12 kind of gun), forge cube version. Free design, bold: a boxy armoured
# receiver in dark-red paint over gun metal, a huge 20-shell drum underneath with a window showing red shells, a
# vented barrel jacket ending in a slotted breaching muzzle, a carry handle with an iron sight, a stubby stock.
import math

from _common import (Model, fp, METAL, METAL_HI, METAL_MID, PANEL, PANEL_DK, RED, RED_HI, CAUTION, WHITE, GREEN,
                     BRASS, DARK, SCREW, UAC, ARROW, armour, corner_screws, hazard, worn_paint, finish, vents)

SHELL_RED = (170, 30, 24)
Z_BORE = 16.0


def build():
    m = Model("bd_assault_shotgun")
    m.pivot = (60, 0, 0)
    armour(m, 30, 120, 16.0, 2, 26, worn_paint(RED, RED_HI, 0.3, 1101), bevel=3.0, panel=PANEL_DK)
    m.cprism([(-6, -6), (-6, 22), (30, 24), (30, 4), (10, 0)], 12.0, fp.metal(METAL), bevel=2.5, edge=0.5)
    m.prism([(2, 4), (2, 16), (24, 18), (24, 8)], -7, 7, None, size=0.5, carve=True)          # skeleton window
    m.cbox(-8, -6, 12.5, -7, 23, (30, 30, 32), size=0.5)
    # the drum: a fat cylinder under the receiver, lying along y, with a window of red shells
    m.part = 'drum'
    m.cyl(-9, 9, 80, -8, 13.0, fp.metal(METAL_MID), axis='y', edge=0.5)
    m.cyl(-9.5, 9.5, 80, -8, 4.0, fp.metal(METAL_HI), axis='y', edge=0.25)
    for k in range(10):
        a = k * math.tau / 10
        xc, zc = 80 + math.cos(a) * 9, -8 + math.sin(a) * 9
        m.cyl(8.5, 9.5, xc, zc, 1.8, SHELL_RED, axis='y', size=0.25, edge=0.25)
        m.cyl(8.5, 9.5, xc, zc, 0.8, BRASS, axis='y', size=0.25, edge=0.25)
    hazard(m, 66, 94, -10, 10, -22, -18)
    m.part = 'body'
    # barrel jacket, slotted muzzle
    m.cbox(120, 190, 12.0, Z_BORE - 6, Z_BORE + 6, fp.metal(METAL), bevel=2.0, edge=0.5)
    vents(m, 124, 184, Z_BORE - 3, Z_BORE + 3, step=6.0)
    fp.barrel(m, 186, 206, Z_BORE, 3.4, fp.metal(METAL_MID), bore=2.2)
    m.cbox(196, 208, 10.0, Z_BORE - 5, Z_BORE + 5, fp.metal(METAL_HI), bevel=1.5, edge=0.25)
    for x in (199, 203):
        for side in ('+y', '-y', '+z'):
            m.groove([(x, Z_BORE - 3) if side != '+z' else (x, -3), (x, Z_BORE + 3) if side != '+z' else (x, 3)],
                     side, depth=3, width=2, dark=0.15)
    m.cyl(206, 209, 0, Z_BORE, 2.2, None, edge=0.25, carve=True)
    # carry handle with a rear peep, front post
    for i in range(50):
        t = i / 49
        m.box(44 + t * 56, 45 + t * 56, -2, 2, 30 + (0 if 0.1 < t < 0.9 else -4 * (abs(t - 0.5) * 2 - 0.8) / 0.2),
              33, fp.metal(METAL), size=0.5)
    m.cbox(44, 50, 4.0, 26, 30, fp.metal(METAL), size=0.5)
    m.cbox(96, 102, 4.0, 26, 30, fp.metal(METAL), size=0.5)
    m.cbox(46, 50, 3.0, 33, 36, fp.metal(METAL), size=0.5)
    m.cyl(46, 50, 0, 34.5, 0.6, None, edge=0.25, carve=True)
    fp.sight_post(m, 186, Z_BORE + 6, 5.0, fp.metal(METAL), w=1.5, dot=GREEN)
    # grip and guard
    m.cprism([(50, 4), (42, 2), (36, -18), (46, -20), (54, -6), (60, 4)], 10.0, fp.metal(METAL), bevel=2.0,
             edge=0.5)
    fp.guard(m, 56, 70, -8, 2, fp.metal(METAL))
    fp.trigger(m, 62, 2, fp.metal(METAL_HI), length=6)
    for side in ('+y', '-y'):
        m.decal(UAC, 92, 22, side, WHITE, mode='paint')
        m.decal(ARROW, 106, 22, side, WHITE, mode='paint')
        m.bolt(80, -8, side, SCREW)                                                # the drum's axle
    corner_screws(m, 30, 120, 2, 26, inset=3, kind='hex')
    finish(m, 1110, (30, 120, 2, 26), grime=0.2, scratches=16, cracks=2)
    return m
