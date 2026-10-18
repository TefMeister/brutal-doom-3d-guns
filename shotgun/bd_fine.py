# Fine detail on the Brutal Doom cube shotgun, in the OPEN Blender file, after bd_live.run() and before bd_wear.run():
# panel lines and vents cut with the kit's smallest cubes (0.85 mm), screw heads, trims and arrow marks built of them.
# MCP: import bd_fine; bd_fine.run(). The numbers are FINE_* in bd_settings.py.
import random

import bpy

import bl
import edit
import carve_wear as cw
import edit_small as small
import bd_gun
from bd_settings import (VOXEL_M, SHADE, FINE_LINES, FINE_SCREWS, FINE_VENTS, FINE_TRIMS, FINE_MARKS, FINE_NUMBER, FONT,
                         FINE_COL)

F = edit.FINE
OB = "BD_body"


def rgb01(name):
    return tuple(c / 255.0 for c in FINE_COL[name])


class Gun:
    """Gun cube space (x along, y left, z up) in quarter cubes, on the body object's own cube grid."""

    def __init__(self, s, cells):
        sc = s.cells
        # gun (x, y, z) -> solid cell (-y + b, x + a, z + c)
        self.a = min(c[1] for c in sc) - min(c[0] for c in cells)
        self.b = min(c[0] for c in sc) + max(c[1] for c in cells)
        self.c = min(c[2] for c in sc) - min(c[2] for c in cells)
        miss = sum((-y + self.b, x + self.a, z + self.c) not in sc for x, y, z in list(cells)[:500])
        if miss:
            raise RuntimeError("gun cubes and the Blender object do not line up (%d of 500 missing)" % miss)

    def fine(self, x, y, z):
        """Fine position of the quarter cube at gun cubes (x, y, z), each a float."""
        X, Y, Z = int(round(x * F)), int(round(y * F)), int(round(z * F))
        return (F * self.b + F - 1 - Y, X + F * self.a, Z + F * self.c)


def out_dir(sign):
    """The solid-space direction of the gun's left (+1) or right (-1) side."""
    return (-sign, 0, 0)


def sides(side):
    return {'both': (1, -1), 'left': (1,), 'right': (-1,)}[side]


def surface(s, g, sign, y, x, z, tol=1.0):
    """The outermost solid quarter cube at (x, z) seen from that side, starting two cubes out from y; None when the
    surface there lies more than `tol` cubes deeper than y (a port, a slot) or nothing is there."""
    for k in range(int((2 + tol + 1) * F)):
        yy = sign * (y + 2 - k / F)
        p = g.fine(x, yy, z)
        if small.occupied(s, p):
            return p if k / F <= 2 + tol else None
    return None


def raster(points, step=1.0 / F):
    """Every quarter-cube spot on the straight lines joining the points."""
    out = []
    for (x0, z0), (x1, z1) in zip(points, points[1:]):
        n = max(1, int(round(max(abs(x1 - x0), abs(z1 - z0)) / step)))
        for i in range(n + 1):
            p = (x0 + (x1 - x0) * i / n, z0 + (z1 - z0) * i / n)
            if not out or out[-1] != p:
                out.append(p)
    return out


def shaded(rgb, d):
    k = SHADE.get(tuple(d), 1.0)
    return tuple(min(1.0, c * k) for c in rgb)


class Detail:
    def __init__(self, s):
        self.s = s
        self.cut_rgb = {}       # fine position -> colour of the faces a cut leaves showing
        self.stats = dict(cut=0, built=0)

    def cut(self, p, rgb):
        if cw.carve(self.s, p, 1):
            self.cut_rgb[p] = rgb
            self.stats['cut'] += 1

    def build(self, p, rgb):
        if small.occupied(self.s, p):
            return
        small._place_unit(self.s, p, 1, rgb)
        cell, idx = small.split_fpos(p)
        for d in edit.DIRS:
            self.s.sfaces[(cell, idx, d)] = shaded(rgb, d)
        self.stats['built'] += 1

    def paint_cuts(self):
        """Every face a cut left showing takes that cut's colour."""
        s = self.s
        for p, rgb in self.cut_rgb.items():
            for d in edit.DIRS:
                q = tuple(p[i] + d[i] for i in range(3))
                cell, idx = small.split_fpos(q)
                fc = s.fine.get(cell)
                if fc and idx in fc.subs:
                    face = tuple(-v for v in d)
                    s.sfaces[(cell, idx, face)] = shaded(rgb, face)


def run():
    ob = bpy.data.objects[OB]
    if not edit.has_colours(ob):
        if not bl.pick_mode_check(ob, VOXEL_M):
            bl.split_to_cubes(ob, VOXEL_M)
        edit.convert(ob, VOXEL_M)
    s = edit.Solid(ob, VOXEL_M)
    g = Gun(s, set(bd_gun.build().p['body']))
    dt = Detail(s)
    line, vent, screw, trim, mark = (rgb01(n) for n in ('line', 'vent', 'screw', 'trim', 'mark'))

    for side, y, pts in FINE_LINES:                                   # panel lines
        for sign in sides(side):
            for x, z in raster(pts):
                p = surface(s, g, sign, y, x, z)
                if p:
                    dt.cut(p, line)

    V = FINE_VENTS                                                    # vents: slots two small cubes tall and deep
    for sign in sides(V['side']):
        for z in V['z']:
            for x, zz in raster([(V['x0'], z), (V['x1'], z)]) + raster([(V['x0'], z + 0.25), (V['x1'], z + 0.25)]):
                p = surface(s, g, sign, V['y'], x, zz)
                if not p:
                    continue
                d = out_dir(sign)
                for k in range(V['depth']):
                    dt.cut(tuple(p[i] - d[i] * k for i in range(3)), vent)

    for side, y, centres in FINE_SCREWS:                              # raised screw heads, round-ish, with a slot
        for sign in sides(side):
            d = out_dir(sign)
            for cx, cz in centres:
                for i in range(-2, 3):
                    for j in range(-2, 3):
                        if abs(i) == abs(j) == 2 or (j == 0 and abs(i) <= 1):
                            continue                                  # the corners, and the slot across it
                        p = surface(s, g, sign, y, cx + i / F, cz + j / F)
                        if p:
                            dt.build(tuple(p[n] + d[n] for n in range(3)), screw)

    for side, y, pts in FINE_TRIMS:                                   # raised trims
        for sign in sides(side):
            d = out_dir(sign)
            for x, z in raster(pts):
                p = surface(s, g, sign, y, x, z)
                if p:
                    dt.build(tuple(p[n] + d[n] for n in range(3)), trim)

    for side, y, mx, mz, down in FINE_MARKS:                          # little raised arrows: 7, 5, 3, 1 small cubes
        for sign in sides(side):
            d = out_dir(sign)
            for row, half in enumerate((3, 2, 1, 0)):
                z = mz + (-row if down else row) / F
                for i in range(-half, half + 1):
                    p = surface(s, g, sign, y, mx + i / F, z)
                    if p:
                        dt.build(tuple(p[n] + d[n] for n in range(3)), mark)

    N = FINE_NUMBER                                                   # the serial number, carved and worn
    rng = random.Random(N['seed'])
    number = rgb01('number')
    step = 3 * N['dot'] + N['gap']                                    # small cubes from one letter to the next
    for sign in sides(N['side']):
        for i, ch in enumerate(N['text']):
            x0 = int(round(N['x'] * F)) + i * step
            for row, bits in enumerate(FONT[ch]):
                for col, bit in enumerate(bits):
                    if bit != '1':
                        continue
                    for a in range(N['dot']):
                        for b in range(N['dot']):
                            if rng.random() < N['wear']:
                                continue                              # worn away
                            X = x0 + col * N['dot'] + a
                            Z = int(round(N['z_top'] * F)) - row * N['dot'] - b
                            p = surface(s, g, sign, N['y'], X / F, Z / F)
                            if p:
                                dt.cut(p, number)

    dt.paint_cuts()
    small.tidy(s)
    f0 = len(ob.data.polygons)
    s.write()
    dt.stats.update(faces_before=f0, faces_after=len(ob.data.polygons))
    print(OB, dt.stats)
    return dt.stats
