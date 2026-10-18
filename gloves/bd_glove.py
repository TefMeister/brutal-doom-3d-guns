# One of Doomguy's gloves as cubes: {(x, y, z): colour name}. No Blender here.
# Built as the right hand; the left is its exact mirror across x. The finger, thumb and slab builders are the Ashes
# gloves' (ashes-2063-weapons, gl_hand.py, 2026-09-23), copied so this project stands on its own.
import math

from bd_glove_settings import (PALM_W, PALM_L, PALM_T, PALM_CORNER, DOME, EDGE_ROUND, TAPER, FINGERS, FINGER_W,
                               FINGER_T, CURL, SPLAY, THUMB_BASE, THUMB_W, THUMB_T, THUMB_SEGS, CUFF_L, CUFF_W,
                               CREASE, TIP_ROUND)


def _chain(cells, xc, w, t, start, segs, colour_at):
    """A finger or thumb: boxes w wide, t thick, laid along a bent path.
    segs: (length, degrees sideways [+ = towards +x], degrees down). Returns the tip point."""
    x, y, z = start
    step = 0
    total = sum(s[0] for s in segs)
    for length, side, down in segs:
        dx = math.sin(math.radians(side)) * math.cos(math.radians(down))
        dy = math.cos(math.radians(side)) * math.cos(math.radians(down))
        dz = -math.sin(math.radians(down))
        for _ in range(length):
            x, y, z = x + dx, y + dy, z + dz
            cx, cy, cz = round(x), round(y), round(z)
            tip = step >= total - TIP_ROUND
            for ix in range(cx - w // 2, cx - w // 2 + w):
                for iz in range(cz - t // 2, cz - t // 2 + t):
                    side_x = ix in (cx - w // 2, cx - w // 2 + w - 1)
                    if side_x and (tip or iz in (cz - t // 2, cz - t // 2 + t - 1)):
                        continue                                     # rounded finger, rounder at the tip
                    cells[(ix + xc, cy, iz)] = colour_at(step, iz == cz - t // 2 + t - 1)
            step += 1
    return (x + xc, y, z)


def _joints(segs):
    """The steps at which a finger bends: the first cubes of its second and third segments."""
    return {segs[0][0], segs[0][0] + segs[1][0]} if len(segs) > 2 else {segs[0][0]}


def _finger(cells, name, xc, y0, length):
    a, b, c = CURL
    segs = [(length * 4 // 10, SPLAY[name] * 3, a), (length * 3 // 10, SPLAY[name] * 2, a + b),
            (length - length * 4 // 10 - length * 3 // 10, 0, a + b + c)]
    joints = _joints(segs)

    def colour_at(step, top):
        if any(j <= step < j + CREASE for j in joints) and top:
            return 'under_dark'
        return 'under_hi' if step == 0 and top else 'under'

    return _chain(cells, xc, FINGER_W, FINGER_T, (0, y0, 1), segs, colour_at)


def _thumb(cells):
    segs = [(n, -side, down) for n, side, down in THUMB_SEGS]       # -side: out towards -x
    joints = _joints(segs)

    def colour_at(step, top):
        return 'under_dark' if any(j <= step < j + CREASE for j in joints) and top else 'under'

    bx, by, bz = THUMB_BASE
    return _chain(cells, bx, THUMB_W, THUMB_T, (0, by, bz), segs, colour_at)


def _slab(cells, y0, y1, half_w, thick, corner, colour_at, dome=0, taper=0):
    """A rounded slab: corners rounded in plan, long edges shaved off, thinner at both ends."""
    for y in range(y0, y1 + 1):
        ends = min(y - y0, y1 - y)
        thin = taper if ends < 3 else 0
        for x in range(-half_w, half_w + 1):
            cx = half_w - abs(x)
            if ends < corner and cx < corner and (corner - ends) ** 2 + (corner - cx) ** 2 > corner ** 2:
                continue
            d = round(dome * (1 - (x / float(half_w)) ** 2)) if dome else 0
            z_lo, z_hi = -thick // 2 + thin, thick // 2 + d - 1 - thin
            shave = max(0, EDGE_ROUND - cx)                          # the long edges are rounded
            for z in range(z_lo + shave, z_hi - shave + 1):
                cells[(x, y, z)] = colour_at(x, y, z, z == z_hi - shave, z == z_lo + shave)


def _palm(cells):
    hw = PALM_W // 2

    def colour_at(x, y, z, top, bottom):
        if bottom and abs(x) == 4 and 3 <= y <= PALM_L - 4:
            return 'under_dark'                                      # the palm's lines
        if top and y == PALM_L - 1 and abs(x) < hw - 2:
            return 'under_hi'                                        # the knuckle ridge
        return 'under'

    _slab(cells, 0, PALM_L, hw, PALM_T, PALM_CORNER, colour_at, dome=DOME, taper=TAPER)
    for y in range(1, 16):                                           # the pad of the thumb, low and wide
        r = (y - 8) / 7.0
        reach = 5 * math.sqrt(max(0.0, 1 - r * r))
        for x in range(-hw - 5, -hw + 1):
            if abs(x + hw) > reach:
                continue
            for z in range(-PALM_T // 2 + 1, PALM_T // 2 - 1):
                cells[(x, y, z)] = 'under'


def _cuff(cells):
    def colour_at(x, y, z, top, bottom):
        return 'seam' if y == -1 and not top and not bottom else 'under'

    _slab(cells, -CUFF_L, -1, CUFF_W // 2, PALM_T, 2, colour_at)


def right_glove():
    cells = {}
    _palm(cells)
    _cuff(cells)
    for name, xc, y0, length in FINGERS:
        _finger(cells, name, xc, y0, length)
    tip = _thumb(cells)
    assert tip[0] < THUMB_BASE[0], "the built glove is not a right hand"     # thumb out towards -x
    return cells


def left_glove():
    return {(-x, y, z): c for (x, y, z), c in right_glove().items()}
