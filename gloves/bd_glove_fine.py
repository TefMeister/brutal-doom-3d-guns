# Fine detail on Doomguy's gloves, with the kit's smallest cubes (0.85 mm): an engraved line round each back plate, a
# stud on every knuckle, stitching along the cuff's leather strap, grooves across the cuff's panel, and the Slayer's
# mark standing proud on the LEFT back plate (Tefa, 2026-10-18). Called by bd_glove_live.run() after the gloves are
# placed and turned into colour cubes, before their scratches. The numbers are in bd_glove_settings.py.
import bpy

import edit
import edit_small as small
import bd_glove_pose
from bd_fine import Gun, Detail
from bd_glove_settings import (BACK_PLATE, KNUCKLE_PLATE, FINGERS, ARMOUR_CUFF, STRAP, BUCKLE, CUFF_PANEL, VOXEL_M,
                               SLAYER_MARK, PLATE_GROOVE, KNUCKLE_STUD, STITCH, CUFF_VENTS,
                               FINE_COL, COL)
from slayer_mark import MARK

F = edit.FINE
TOP = 20 * F                  # the hand-space height a downward search starts from, above every part of the glove


def rgb01(rgb):
    return tuple(c / 255.0 for c in rgb)


class Hand:
    """Hand space (quarter cubes) -> the glove object's own small-cube grid, for one posed glove."""

    def __init__(self, side, s, cells):
        self.side, self.s = side, s
        self.g = Gun(s, cells)

    def solid(self, P):
        cell = tuple(p // F for p in P)
        sub = tuple(p % F for p in P)
        if self.side == 'right':                                     # the axes of bd_glove_pose._right_axes
            x, y, z = bd_glove_pose._right_axes(*cell)
            shift, gs = bd_glove_pose.RIGHT['shift'], (sub[1], F - 1 - sub[2], F - 1 - sub[0])
        else:                                                        # and _left_axes
            x, y, z = bd_glove_pose._left_axes(*cell)
            shift, gs = bd_glove_pose.LEFT['shift'], (sub[0], F - 1 - sub[1], F - 1 - sub[2])
        return self.g.at(F * (x + shift[0]) + gs[0], F * (y + shift[1]) + gs[1], F * (z + shift[2]) + gs[2])

    def mirror(self, X):
        """A right-hand x (quarter cubes) on this glove: the left glove is the mirror."""
        return X if self.side == 'right' else F - 1 - X

    def surface(self, X, Y):
        """The hand-space height of the back of the glove at (X, Y), or None."""
        for Z in range(TOP, -TOP, -1):
            if small.occupied(self.s, self.solid((X, Y, Z))):
                return Z
        return None


def q(v):
    return int(round(v * F))


def raster(points):
    out = []
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        n = max(1, int(round(max(abs(x1 - x0), abs(y1 - y0)) * F)))
        for i in range(n + 1):
            p = (q(x0 + (x1 - x0) * i / n), q(y0 + (y1 - y0) * i / n))
            if not out or out[-1] != p:
                out.append(p)
    return out


def detail(side, ob, cells):
    s = edit.Solid(ob, VOXEL_M)
    h = Hand(side, s, cells)
    dt = Detail(s)

    def build(X, Y, height, rgb):
        Z = h.surface(X, Y)
        if Z is not None:
            for k in range(1, height + 1):
                dt.build(h.solid((X, Y, Z + k)), rgb)

    def cut(X, Y, rgb):
        Z = h.surface(X, Y)
        if Z is not None:
            dt.cut(h.solid((X, Y, Z)), rgb)

    groove, stitch, stud = rgb01(FINE_COL['groove']), rgb01(FINE_COL['stitch']), rgb01(FINE_COL['stud'])

    P, g = BACK_PLATE, PLATE_GROOVE                                  # the engraved line round the back plate
    xa, xb, ya, yb = P['x0'] + g, P['x1'] + 1 - g, P['y0'] + g, P['y1'] + 1 - g
    c = max(0, P['corner'] - 1)
    for X, Y in raster([(xa + c, ya), (xb - c, ya), (xb, ya + c), (xb, yb - c), (xb - c, yb), (xa + c, yb),
                        (xa, yb - c), (xa, ya + c), (xa + c, ya)]):
        cut(h.mirror(X), Y, groove)

    K, S = KNUCKLE_PLATE, KNUCKLE_STUD                               # a stud on every knuckle
    for _name, xc, _y0, _len in FINGERS:
        X0, Y0 = q(xc + 0.5) - S['size'] // 2, q((K['y0'] + K['y1'] + 1) / 2.0) - S['size'] // 2
        for i in range(S['size']):
            for j in range(S['size']):
                build(h.mirror(X0 + i), Y0 + j, S['height'], stud)

    C, B = ARMOUR_CUFF, BUCKLE                                       # stitching along the strap's two edges
    for y in (STRAP['y0'] + 0.25, STRAP['y1'] + 0.5):
        for X in range(q(-C['half_w'] + 1), q(C['half_w'] - 1), STITCH['step']):
            if q(B['x0']) - 1 <= X <= q(B['x1'] + 1):
                continue                                             # not through the buckle
            cut(h.mirror(X), q(y), stitch)

    V, Pn = CUFF_VENTS, CUFF_PANEL                                   # grooves across the cuff's panel
    span = Pn['y1'] + 1 - Pn['y0']
    for k in range(V['n']):
        y = Pn['y0'] + span * (k + 1) / (V['n'] + 1)
        for X, Y in raster([(Pn['x0'] + 1.5, y), (Pn['x1'] - 0.5, y)]):
            cut(h.mirror(X), Y, rgb01(COL[V['colour']]))

    if side == 'left':                                               # the Slayer's mark, standing proud
        M = SLAYER_MARK
        rows, cols = len(MARK), len(MARK[0])
        X0, Y0 = q(M['x']) - cols // 2, q(M['y'])
        mark = rgb01(FINE_COL[M['colour']])
        for r, line in enumerate(MARK):
            for col, ch in enumerate(line):
                if ch == '#':
                    build(X0 + col, Y0 + rows - 1 - r, M['height'], mark)   # left-hand space as it is: not mirrored

    dt.paint_cuts()
    small.tidy(s)
    f0 = len(ob.data.polygons)
    s.write()
    dt.stats.update(faces_before=f0, faces_after=len(ob.data.polygons))
    print(ob.name, dt.stats)
    return dt.stats


def run(posed, names):
    """posed: {'right': cells, 'left': cells} in gun space; names: {'right': object name, ...}."""
    return {side: detail(side, bpy.data.objects[names[side]], set(cells)) for side, cells in posed.items()}
