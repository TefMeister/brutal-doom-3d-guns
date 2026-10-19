# Brutal Doom: the plasma rifle, forge cube version. Free design, bold: a squat heavy receiver in gun metal and grey
# panels with a glass plasma cell on top glowing cyan, a three-prong emitter at the front with cyan coils between the
# prongs, cooling fins along the barrel shroud, a battery magazine with a charge bar, green sights.
import math

from _common import (Model, fp, METAL, METAL_HI, METAL_MID, PANEL, PANEL_DK, CAUTION, WHITE, GREEN, CYAN, DARK, SCREW,
                     UAC, ARROW, armour, corner_screws, hazard, finish, vents, mul, mix)

Z_AXIS = 16.0
CELL_GLOW = (120, 230, 255)


def build():
    m = Model("bd_plasma_rifle")
    m.pivot = (60, 0, 0)
    armour(m, 20, 130, 20.0, 0, 30, fp.metal(METAL_MID), bevel=3.0, panel=PANEL)
    m.cprism([(0, 4), (0, 26), (20, 28), (20, 2)], 16.0, fp.metal(METAL), bevel=2.0, edge=0.5)    # stock block
    m.cbox(-4, 0, 16.0, 2, 28, (30, 30, 32), size=0.5)
    # the plasma cell on top: a glass tube with a glowing core, caged
    m.cbox(40, 104, 12.0, 30, 34, fp.metal(METAL), size=0.5)
    m.cyl(44, 100, 0, 38, 4.5, (40, 120, 140), edge=0.25)
    m.cyl(44, 100, 0, 38, 2.6, CELL_GLOW, edge=0.25)
    for x in range(48, 100, 8):
        m.cyl(x, x + 1.5, 0, 38, 5.2, fp.metal(METAL_HI), edge=0.25)
    for x in (42, 100):
        m.cbox(x, x + 3, 12.0, 30, 44, fp.metal(METAL), bevel=1.0, edge=0.25)
    # barrel shroud with fins, then the emitter with three prongs and coils
    m.cyl(130, 180, 0, Z_AXIS, 6.0, fp.metal(METAL), edge=0.25)
    for x in range(134, 178, 4):
        m.cyl(x, x + 1.5, 0, Z_AXIS, 8.0, fp.metal(PANEL_DK), edge=0.25)
    for k in range(3):
        a = k * math.tau / 3 + math.pi / 2
        yc, zc = math.cos(a) * 6.5, Z_AXIS + math.sin(a) * 6.5
        m.cyl(178, 204, yc, zc, 1.6, fp.metal(METAL_HI), edge=0.25)
        m.ball(204, yc, zc, 2.0, fp.metal(METAL_HI), edge=0.25)
    for x in range(182, 202, 3):
        m.cyl(x, x + 1, 0, Z_AXIS, 4.0, CYAN, hollow=2.0, size=0.25, edge=0.25)
    m.cyl(178, 196, 0, Z_AXIS, 1.6, CELL_GLOW, edge=0.25)
    # battery magazine with a charge bar, grip, guard
    m.part = 'mag'
    m.cbox(86, 112, 14.0, -24, 1, fp.metal(PANEL_DK), bevel=1.5, edge=0.5)
    for i in range(6):
        m.box(90 + i * 3, 92 + i * 3, 7.0, 7.5, -20, -14, CYAN if i < 4 else (30, 60, 70), size=0.25)
    hazard(m, 86, 112, -8, 8, -24, -20)
    m.part = 'body'
    m.cprism([(60, 2), (52, 0), (46, -18), (56, -20), (64, -6), (70, 2)], 10.0, fp.metal(METAL), bevel=2.0,
             edge=0.5)
    fp.guard(m, 64, 82, -8, 0, fp.metal(METAL))
    fp.trigger(m, 72, 0, fp.metal(METAL_HI), length=6)
    fp.rear_sight(m, 24, 30, 3.0, fp.metal(METAL), w=6.0, notch=2.0, dots=GREEN)
    fp.sight_post(m, 124, 30, 4.0, fp.metal(METAL), w=1.5, dot=GREEN)
    vents(m, 26, 40, 6, 22, step=3.5, glow=(40, 140, 160))
    for side in ('+y', '-y'):
        m.decal(UAC, 106, 24, side, WHITE, mode='paint')
        m.decal(ARROW, 116, 12, side, CYAN, mode='paint')
    corner_screws(m, 20, 130, 0, 30, inset=4, kind='hex')
    finish(m, 910, (20, 130, 0, 30), grime=0.18, scratches=16, cracks=2)
    return m
