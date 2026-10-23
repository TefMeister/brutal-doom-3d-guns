# Brutal Doom: the chainsaw, forge cube version. Free design, bold: a red-painted engine block with deep cooling
# fins, a tubular top handle wrapped in grip tape, a front handle loop, an exhaust stack, a hazard-striped chain
# guard, and a long guide bar with every chain tooth built from small cubes (it is a separate part, so it can run).
import math

from _common import (Model, fp, METAL, METAL_HI, METAL_MID, PANEL, RED, RED_HI, RED_DK, CAUTION, WHITE, DARK, SCREW,
                     ORANGE, ARROW, armour, corner_screws, hazard, worn_paint, finish, mul)

BAR = (60, 190, -2, 10)                # x0, x1, z0, z1 of the guide bar
TAPE = (30, 30, 30)


def build():
    m = Model("bd_chainsaw")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (20, 0, 0)
    # engine: red block, fins cut across it, a grey panel over the cylinder
    armour(m, 0, 60, 24.0, -10, 24, worn_paint(RED, RED_HI, 0.3, 401), bevel=3.0, panel=None)
    for x in range(6, 40, 3):
        for side in ('+y', '-y'):
            m.groove([(x, 4), (x, 21)], side, depth=3, width=2, dark=0.35)
    m.cbox(40, 58, 26.0, 2, 20, fp.metal(PANEL), bevel=2.0, edge=0.5)
    hazard(m, 40, 58, -14, 14, 2, 8, step=2.0)
    m.part = 'starter'
    m.cyl(-4, 2, 0, 6, 6.0, fp.metal(METAL), edge=0.25)                                    # starter housing
    m.cyl(-6, -4, 0, 6, 3.0, fp.metal(METAL_HI), edge=0.25)
    m.cbox(-10, -6, 6.0, 4, 8, fp.metal((200, 40, 30)), size=0.5)                           # pull handle
    m.box(-6.5, -3.5, -0.25, 0.25, 5.75, 6.25, (200, 196, 180), size=0.25)                 # and its cord
    m.part = 'exhaust'
    # exhaust stack on the right, glowing hot at the mouth
    m.cyl(24, 34, -14, 18, 2.5, fp.metal(METAL_HI), axis='y', edge=0.25)
    m.cyl(20, 34, 29, -15, 2.4, fp.metal(METAL), axis='z', edge=0.25)
    m.cyl(33.5, 34.5, 29, -15, 1.4, ORANGE, axis='z', size=0.25, edge=0.25)
    m.part = 'handle'
    # top handle: a tube from the back over to the front, taped
    for i in range(80):
        t = i / 79
        x = -2 + t * 50
        z = 24 + math.sin(t * math.pi) * 12
        m.ball(x, 0, z, 2.2, TAPE if 0.2 < t < 0.8 else fp.metal(METAL), edge=0.25)
    for i in range(18):
        x = 10 + i * 1.5
        m.box(x, x + 0.5, -2.5, 2.5, 33, 37, (60, 60, 60), size=0.25, keep=True)
    m.part = 'front_handle'
    # front handle loop round the body
    for i in range(70):
        a = i / 69 * math.pi
        m.ball(56, math.cos(a) * 16, 6 + math.sin(a) * 26, 1.6, fp.metal(METAL_HI), edge=0.25)
    m.part = 'bar'
    # the guide bar and its chain (the chain is its own part)
    bx0, bx1, bz0, bz1 = BAR
    m.prism([(bx0, bz0), (bx1 - 6, bz0), (bx1, (bz0 + bz1) / 2), (bx1 - 6, bz1), (bx0, bz1)], -1.0, 1.0,
            fp.metal((150, 152, 156)), size=0.5)
    for x in range(bx0 + 10, bx1 - 10, 12):
        m.cyl(-1.5, 1.5, x, (bz0 + bz1) / 2, 1.2, None, axis='y', edge=0.25, carve=True)
    m.part = 'chain'
    L = 2 * (bx1 - bx0) + 12
    for i in range(int(L / 1.5)):
        s = i * 1.5
        if s < bx1 - bx0:
            x, z, up = bx0 + s, bz1 + 0.25, 1
        elif s < bx1 - bx0 + 6:
            a = (s - (bx1 - bx0)) / 6 * math.pi
            x, z, up = bx1 + math.sin(a) * 2, (bz0 + bz1) / 2 + math.cos(a) * 6.5, 0
        else:
            x, z, up = bx1 - (s - (bx1 - bx0) - 6), bz0 - 0.75, -1
        if x < bx0:
            break
        m.box(x, x + 1.0, -1.25, 1.25, z, z + 0.5, fp.metal((90, 92, 98)), size=0.25)
        if up and i % 2 == 0:                                                               # the teeth
            zt = z + (0.5 if up > 0 else -0.75)
            m.prism([(x, zt), (x + 1.25, zt + 0.75 * up), (x + 1.25, zt)], -1.0, 1.0, fp.metal((200, 200, 204)),
                    size=0.25)
    m.part = 'body'
    m.part = 'clamp'
    m.cbox(56, 66, 6.0, -4, 12, fp.metal(METAL), bevel=1.0, edge=0.5)                       # bar clamp
    for side in ('+y', '-y'):
        m.bolt(60, 0, side, SCREW)
        m.bolt(60, 8, side, SCREW)
        m.decal(ARROW, 44, 18, side, WHITE, dot=2, mode='paint')
    m.decal(["###.###.###", "#...#...#..", "###.###.#..", "..#.#...#..", "###.###.###"], 8, 0, '+y', WHITE,
            mode='paint')
    corner_screws(m, 0, 60, -10, 24, inset=3, kind='slot')
    fp.trigger(m, 8, -10, fp.metal(CAUTION), length=6, curve=1.0)
    m.part = 'grip'
    m.cprism([(14, -10), (6, -12), (2, -24), (12, -26), (18, -14)], 8.0, TAPE, bevel=1.5, edge=0.5)
    finish(m, 410, (0, 60, -10, 24), grime=0.3, scratches=16, cracks=3)
    return m
