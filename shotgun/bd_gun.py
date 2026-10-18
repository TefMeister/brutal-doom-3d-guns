# The Brutal Doom cube shotgun's shape, split into parts: {part: {(x, y, z): colour name}}. No Blender here.
# Built one part at a time with Tefa (2026-10-18 on): the stock first, then the metal, square and bulky.
# Parts: 'body' (stock, receiver, barrel, magazine - never moves), 'pump' (fore-end and action bars - slides back to
# pump), 'trigger'.
import math

from bd_settings import (STOCK_X, STOCK_TOP, STOCK_BOTTOM, STOCK_HALF_WIDTH, BUTT_PAD, GRAIN_STEP, GRAIN_WAVE,
                         RECEIVER, PORT, BOLTS, BARREL, MUZZLE, RIB, SIGHT, MAGTUBE, MAGCAP, CLAMP, PUMP, ACTION_BARS,
                         GUARD, TRIGGER)
from parts import Parts


def along(points, x):
    """The edge's height at x, on the straight line between the two points either side of it."""
    for (x0, z0), (x1, z1) in zip(points, points[1:]):
        if x0 <= x <= x1:
            return z0 + (z1 - z0) * (x - x0) / (x1 - x0) if x1 != x0 else z0
    return points[-1][1]


def stock(g):
    x0, x1 = STOCK_X
    w_butt, w_wrist = STOCK_HALF_WIDTH
    for x in range(x0, x1 + 1):
        t = (x - x0) / (x1 - x0)
        top, bot = round(along(STOCK_TOP, x)), round(along(STOCK_BOTTOM, x))
        w = round(w_butt + (w_wrist - w_butt) * t)
        for z in range(bot, top + 1):
            for y in range(-w, w + 1):
                edge_y = abs(y) == w
                if edge_y and z in (top, bot):
                    continue                                   # rounded long edges
                if x - x0 < BUTT_PAD:
                    g.put('body', x, y, z, 'butt_pad')
                    continue
                wave = GRAIN_WAVE[0] * math.sin(x / GRAIN_WAVE[1])
                c = 'wood'
                if z <= bot + 1:
                    c = 'wood_dark'
                elif z >= top - 1 and abs(y) < w:
                    c = 'wood_hi'
                elif round(z + wave) % GRAIN_STEP == 0:
                    c = 'wood_grain'
                g.put('body', x, y, z, c)


def box(g, part, x0, x1, y, z0, z1, c, bevel=0):
    """A square bar along x, its four long edges cut back by `bevel` cubes (0 = sharp corners)."""
    for x in range(x0, x1 + 1):
        for yy in range(-y, y + 1):
            for z in range(z0, z1 + 1):
                if bevel and (y - abs(yy)) + min(z - z0, z1 - z) < bevel:
                    continue
                g.put(part, x, yy, z, c)


def receiver(g):
    R = RECEIVER
    box(g, 'body', R['x0'], R['x1'], R['y'], R['z0'], R['z1'], 'metal', R['bevel'])
    P = PORT
    g.cut(P['x0'], P['x1'], -R['y'], -R['y'], P['z0'], P['z1'])                    # ejection port, right side
    g.fill('body', P['x0'], P['x1'], -R['y'] + 1, -R['y'] + 1, P['z0'], P['z1'], 'port')
    b = BOLTS
    for x in range(R['x0'] + b['start'], R['x1'] - b['end_gap'], b['step']):         # big square bolts, both sides
        for yy in (-R['y'] - 1, R['y'] + 1):
            g.fill('body', x, x + 1, yy, yy, R['z0'] + b['z'], R['z0'] + b['z'] + 1, 'metal_hi')


def barrel(g):
    B, M = BARREL, MUZZLE
    box(g, 'body', B['x0'], B['x1'], B['y'], B['z0'], B['z1'], 'metal', 1)
    g.tube('body', M['x0'], M['x1'], M['zc'], M['r'], 'metal')                       # round tip
    g.tube('body', M['x1'] - 1, M['x1'], M['zc'], M['bore'], 'bore')                 # the bore
    for x in range(B['x0'] + 2, M['x0'] + 1):                                        # vent rib, notched
        if (x - B['x0']) % RIB['notch_step']:
            g.fill('body', x, x, -RIB['y'], RIB['y'], RIB['z'], RIB['z'], 'metal')
    g.fill('body', SIGHT['x0'], SIGHT['x1'], 0, 0, RIB['z'], SIGHT['z1'], 'sight')
    T, C, K = MAGTUBE, CLAMP, MAGCAP
    box(g, 'body', T['x0'], T['x1'], T['y'], T['z0'], T['z1'], 'metal', 1)
    box(g, 'body', K['x0'], K['x1'], K['y'], K['z0'], K['z1'], 'metal_dark', 1)
    box(g, 'body', C['x0'], C['x1'], C['y'], C['z0'], C['z1'], 'metal_dark', 1)


def pump(g):
    P = PUMP
    for x in range(P['x0'], P['x1'] + 1):
        end = min(x - P['x0'], P['x1'] - x)
        bev = max(0, P['end_bevel'] - end)                                           # squared-off, slightly bevelled ends
        for y in range(-P['y'] + bev, P['y'] - bev + 1):
            for z in range(P['z0'] + bev, P['z1'] - bev + 1):
                if MAGTUBE['z0'] <= z <= MAGTUBE['z1'] and abs(y) <= MAGTUBE['y']:
                    continue                                                         # the tube runs through it
                outer = abs(y) == P['y'] - bev or z == P['z0'] + bev
                c = 'wood'
                if outer and (z - P['z0']) % P['groove_step'] == 0 and end > 3:
                    c = 'wood_grain'                                                 # grip grooves along its sides
                elif z == P['z1'] - bev:
                    c = 'wood_hi'
                g.put('pump', x, y, z, c)
    A = ACTION_BARS
    for yy in (-A['y'], A['y']):
        g.fill('pump', RECEIVER['x1'] - 8, P['x0'] - 1, yy, yy, A['z'], A['z'], 'metal_hi')


def guard(g):
    G = GUARD
    g.fill('body', G['x0'], G['x1'], -G['y'], G['y'], G['z_bottom'], G['z_bottom'] + 1, 'metal')
    g.fill('body', G['x1'] - 1, G['x1'], -G['y'], G['y'], G['z_bottom'], RECEIVER['z0'], 'metal')
    g.fill('body', G['x0'], G['x0'] + 1, -G['y'], G['y'], G['z_bottom'], RECEIVER['z0'], 'metal')
    for x, z in TRIGGER:
        g.put('trigger', x, 0, z, 'metal_hi')


def build():
    g = Parts()
    stock(g)
    receiver(g)
    barrel(g)
    pump(g)
    guard(g)
    return g
