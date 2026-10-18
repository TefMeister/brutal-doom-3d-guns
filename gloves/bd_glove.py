# One of Doomguy's gloves as cubes: {(x, y, z): colour name}. No Blender here.
# Built as the right hand; the left is its exact mirror across x. The finger, thumb and slab builders are the Ashes
# gloves' (ashes-2063-weapons, gl_hand.py, 2026-09-23), copied so this project stands on its own.
import math

from bd_glove_settings import (PALM_W, PALM_L, PALM_T, PALM_CORNER, DOME, EDGE_ROUND, TAPER, FINGERS, FINGER_W,
                               FINGER_T, CURL, SPLAY, THUMB_BASE, THUMB_W, THUMB_T, THUMB_SEGS,
                               CREASE, TIP_ROUND, PLATE_GAP, PLATE_RAISE, PLATE_OVERHANG, KNUCKLE_PLATE, BACK_PLATE,
                               BACK_PLATE_TOP, RIVETS, GREEN_PLATES, JOINT_RAISE, ARMOUR_CUFF,
                               CUFF_BANDS, CUFF_PANEL, CUFF_RIVETS, THUMB_PAD, PALM_LINES, LEATHER_PALM, STRAP, BUCKLE)

FINGER_METAL = 'green' if 'finger' in GREEN_PLATES else 'steel'


def _plate_steps(segs, start=1):
    """{step: 'lead', 'mid' or 'joint'} along a finger: every segment its own plate, and the steps between two
    plates, where the finger bends, a joint."""
    out, s0 = {}, 0
    for n, _side, _down in segs:
        first = max(s0 + PLATE_GAP, start) if s0 else start
        for step in range(first, s0 + n - (PLATE_GAP if s0 + n < sum(s[0] for s in segs) else 0)):
            out[step] = 'lead' if step == first else 'mid'
        s0 += n
    plated = sorted(out)
    for step in range(plated[0], plated[-1]):
        out.setdefault(step, 'joint')
    return out


def _chain(cells, xc, w, t, start, segs, colour_at, plates=None, metal='steel'):
    """A finger or thumb: boxes w wide, t thick, laid along a bent path.
    segs: (length, degrees sideways [+ = towards +x], degrees down). Returns the tip point.
    plates: {step: 'lead'/'mid'/'joint'}: plated steps get a `metal` plate over their top and upper sides, joints a
    narrower, lower steel band."""
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
                    cells[(ix + xc, cy, iz)] = colour_at(step, iz == cz - t // 2 + t - 1, iz == cz - t // 2)
            kind = (plates or {}).get(step)
            top = cz - t // 2 + t - 1
            if kind == 'joint':
                for ix in range(cx - w // 2 + 1, cx - w // 2 + w - 1):
                    for pz in range(top, top + JOINT_RAISE + 1):
                        cells[(ix + xc, cy, pz)] = 'steel_hi' if pz == top + JOINT_RAISE else 'steel'
                for ix in (cx - w // 2, cx - w // 2 + w - 1):
                    cells[(ix + xc, cy, top - 1)] = 'steel_dark'
            elif kind:
                x_lo, x_hi = cx - w // 2 - PLATE_OVERHANG, cx - w // 2 + w - 1 + PLATE_OVERHANG
                for ix in range(x_lo, x_hi + 1):
                    edge = ix in (x_lo, x_hi)                        # the plate's sides, wrapping down
                    for pz in range(top - 1, top + PLATE_RAISE + 1):
                        if edge and pz == top + PLATE_RAISE:
                            continue                                 # bevelled top edges
                        if pz == top + PLATE_RAISE or (pz == top + PLATE_RAISE - 1 and ix in (x_lo + 1, x_hi - 1)):
                            c = metal + '_hi' if kind == 'lead' else metal
                        else:
                            c = metal + '_dark' if edge or pz < top else metal
                        cells[(ix + xc, cy, pz)] = c
            step += 1
    return (x + xc, y, z)


def _joints(segs):
    """The steps at which a finger bends: the first cubes of its second and third segments."""
    return {segs[0][0], segs[0][0] + segs[1][0]} if len(segs) > 2 else {segs[0][0]}


def _finger(cells, name, xc, y0, length, curl=None):
    a, b, c = curl or CURL
    segs = [(length * 4 // 10, SPLAY[name] * 3, a), (length * 3 // 10, SPLAY[name] * 2, a + b),
            (length - length * 4 // 10 - length * 3 // 10, 0, a + b + c)]
    joints = _joints(segs)

    def colour_at(step, top, bottom):
        if bottom and LEATHER_PALM:
            return 'leather_dark' if any(j <= step < j + CREASE for j in joints) else 'leather'
        if any(j <= step < j + CREASE for j in joints) and top:
            return 'under_dark'
        return 'under_hi' if step == 0 and top else 'under'

    return _chain(cells, xc, FINGER_W, FINGER_T, (0, y0, 1), segs, colour_at, _plate_steps(segs), FINGER_METAL)


def _thumb(cells, path=None, base=None, size=None):
    """path: [(length, degrees outward, degrees down)], base: where it leaves the palm, size: (width, thickness)."""
    segs = [(n, -side, down) for n, side, down in (path or THUMB_SEGS)]   # -side: out towards -x
    joints = _joints(segs)

    def colour_at(step, top, bottom):
        if bottom and LEATHER_PALM:
            return 'leather'
        return 'under_dark' if any(j <= step < j + CREASE for j in joints) and top else 'under'

    bx, by, bz = base or THUMB_BASE
    w, t = size or (THUMB_W, THUMB_T)
    return _chain(cells, bx, w, t, (0, by, bz), segs, colour_at, _plate_steps(segs, start=3),
                  FINGER_METAL)


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

    L = PALM_LINES
    palm = 'leather' if LEATHER_PALM else 'under'
    palm_dark = 'leather_dark' if LEATHER_PALM else 'under_dark'

    def colour_at(x, y, z, top, bottom):
        if bottom and abs(x) == L['x'] and L['y0'] <= y <= L['y1']:
            return palm_dark                                         # the palm's lines
        if bottom:
            return palm
        if top and y == PALM_L - 1 and abs(x) < hw - 2:
            return 'under_hi'                                        # the knuckle ridge
        return 'under'

    _slab(cells, 0, PALM_L, hw, PALM_T, PALM_CORNER, colour_at, dome=DOME, taper=TAPER)
    T = THUMB_PAD
    z_lo = -PALM_T // 2 + 1
    for y in range(T['y0'], T['y1'] + 1):                            # the pad of the thumb, low and wide
        r = (y - T['yc']) / float(T['ry'])
        reach = T['reach'] * math.sqrt(max(0.0, 1 - r * r))
        for x in range(-hw - T['reach'], -hw + 1):
            if abs(x + hw) > reach:
                continue
            for z in range(z_lo, PALM_T // 2 - 1):
                cells[(x, y, z)] = palm if z == z_lo else 'under'


def _cuff(cells):
    C = ARMOUR_CUFF

    S = STRAP

    def colour_at(x, y, z, top, bottom):
        if y == C['y0']:
            return 'under_dark'                                      # the leather lining at the open end
        if y in CUFF_BANDS:
            return 'gunmetal_hi' if top else 'gunmetal'
        if S['y0'] <= y <= S['y1']:
            return 'leather'
        return 'cuff'

    _slab(cells, C['y0'], C['y1'], C['half_w'], C['thick'], C['corner'], colour_at)
    strap = [c for c in cells if S['y0'] <= c[1] <= S['y1']]          # the strap stands one cube proud all round
    for x, y, z in strap:
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y, z + dz)
            if n not in cells:
                cells[n] = 'leather_hi' if dz == 1 else 'leather'
    B = BUCKLE
    for x in range(B['x0'], B['x1'] + 1):                            # a square steel frame on top of the strap
        for y in range(B['y0'], B['y1'] + 1):
            if x in (B['x0'], B['x1']) or y in (B['y0'], B['y1']):
                z = _top(cells, x, y)
                if z is not None:
                    cells[(x, y, z + 1)] = 'steel_hi' if y == B['y1'] else 'steel'
    P = CUFF_PANEL
    _plate(cells, range(P['x0'], P['x1'] + 1), range(P['y0'], P['y1'] + 1), P['corner'], P['y1'], P['raise_'],
           'cuff')
    for x, y in CUFF_RIVETS:
        cells[(x, y, _top(cells, x, y) + 1)] = 'rivet'


def _top(cells, x, y):
    zs = [z for (cx, cy, z) in cells if cx == x and cy == y]
    return max(zs) if zs else None


def _plate(cells, xs, ys, corner, lead_y, raise_, metal='steel'):
    """A plate lying on the back of the hand: the top cube of every column turned to `metal` (steel or green),
    `raise_` rows on it, corners rounded, and its knuckle-side edge (lead_y) catching the light."""
    x0, x1, y0, y1 = xs[0], xs[-1], ys[0], ys[-1]
    for x in xs:
        for y in ys:
            cx, cy = min(x - x0, x1 - x), min(y - y0, y1 - y)
            if cx < corner and cy < corner and (corner - cx) ** 2 + (corner - cy) ** 2 > corner ** 2:
                continue
            z = _top(cells, x, y)
            if z is None:
                continue
            edge = cx == 0 or cy == 0
            cells[(x, y, z)] = metal + '_dark' if edge else metal
            for r in range(1, raise_ + 1):
                if r == raise_ and y == lead_y:
                    c = metal + '_hi'
                else:
                    c = metal + '_dark' if edge else metal
                cells[(x, y, z + r)] = c


def _plates(cells, back_top=True):
    def metal(name):
        return 'green' if name in GREEN_PLATES else 'steel'

    K = KNUCKLE_PLATE
    for _name, xc, _y0, _len in FINGERS:
        _plate(cells, range(xc - K['half_w'], xc + K['half_w'] + 1), range(K['y0'], K['y1'] + 1), 1, K['y1'],
               K['raise_'], metal('knuckle'))
    for name, P in (('back', BACK_PLATE), ('back_top', BACK_PLATE_TOP))[:2 if back_top else 1]:
        _plate(cells, range(P['x0'], P['x1'] + 1), range(P['y0'], P['y1'] + 1), P['corner'], P['y1'], P['raise_'],
               metal(name))
    for x, y in RIVETS:
        cells[(x, y, _top(cells, x, y) + 1)] = 'rivet'


def right_glove(curls=None, thumb=None, thumb_base=None, thumb_size=None, back_top=True):
    """Relaxed and flat by default; curls ({finger: (a, b, c) degrees}) and a thumb path pose it round a gun.
    back_top=False leaves off the small plate stacked on the back plate (the left glove: the Slayer mark goes there)."""
    cells = {}
    _palm(cells)
    _cuff(cells)
    _plates(cells, back_top)
    curls = curls or {}
    for name, xc, y0, length in FINGERS:
        _finger(cells, name, xc, y0, length, curls.get(name))
    tip = _thumb(cells, thumb, thumb_base, thumb_size)
    if thumb is None:
        assert tip[0] < THUMB_BASE[0], "the built glove is not a right hand"     # thumb out towards -x
    else:
        assert thumb[0][1] > 0, "a right hand's thumb must leave the palm outwards (side > 0)"
    return cells


def left_glove(**pose):
    """The exact mirror of the right glove across x: the only way the left hand is made."""
    return {(-x, y, z): c for (x, y, z), c in right_glove(**pose).items()}
