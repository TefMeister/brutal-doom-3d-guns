# The Brutal Doom cube shotgun's shape, split into parts: {part: {(x, y, z): colour name}}. No Blender here.
# Built one part at a time with Tefa (2026-10-18 on): the stock first.
import math

from bd_settings import (STOCK_X, STOCK_TOP, STOCK_BOTTOM, STOCK_HALF_WIDTH, BUTT_PAD, GRAIN_STEP, GRAIN_WAVE)
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


def build():
    g = Parts()
    stock(g)
    return g
