# Fine detail on the Brutal Doom cube pistol, in the OPEN Blender file, after bd_pistol_live.run(): panel lines and
# the picture's slashes cut with the kit's smallest cubes (0.85 mm), screw heads and the red and white marks built of
# them, then the carved scratches. The shotgun's machinery (shotgun/bd_fine.py, bd_wear.py), one Blender object per
# part. Numbers: FINE_* and WEAR in
# bd_pistol_settings.py. MCP: import bd_pistol_fine; bd_pistol_fine.run().
import math
import os
import sys

import bpy

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shotgun"))   # bd_fine

import bl
import edit
import edit_small as small
import bd_pistol_gun
import bd_wear
from bd_fine import Gun, Detail, surface, raster, sides, out_dir
from bd_pistol_settings import (VOXEL_M, FINE_LINES, FINE_SCREWS, FINE_STAMPS, FINE_COL, WEAR, SCRATCH_LIGHTEN, LOGO,
                                GRIP, GRIP_PLATE)
from bd_pistol_live import PARTS

F = edit.FINE


def rgb01(name):
    return tuple(c / 255.0 for c in FINE_COL[name])


def in_star(u, v, r_out, r_in):
    """Is (u, v) inside a five-pointed star, point up, centred on 0?"""
    pts = []
    for k in range(10):
        a = math.pi / 2 + k * math.pi / 5
        r = r_out if k % 2 == 0 else r_in
        pts.append((r * math.cos(a), r * math.sin(a)))
    inside = False
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        if (y0 > v) != (y1 > v) and u < x0 + (v - y0) * (x1 - x0) / (y1 - y0):
            inside = not inside
    return inside


def logo(s, g, dt):
    """The military star in a ring on both grip plates: the ring engraved dark, the star standing proud and bright."""
    L, y = LOGO, GRIP['y'] + 1
    z = L['z']
    cx = (bd_pistol_gun.grip_back(z) + GRIP_PLATE['inset'] + bd_pistol_gun.grip_front(z) - GRIP_PLATE['inset']) / 2.0 + 0.5
    cz = z + 0.5
    reach = int(math.ceil(L['ring_r'] * F)) + 1
    for sign in sides('both'):
        d = out_dir(sign)
        for i in range(-reach, reach + 1):
            for j in range(-reach, reach + 1):
                u, v = (i + 0.5) / F, (j + 0.5) / F                     # this small cube's middle, from the centre
                r = math.hypot(u, v)
                q = surface(s, g, sign, y, cx + i / F, cz + j / F, tol=0)
                if not q:
                    continue
                if L['ring_r'] - L['ring_w'] <= r <= L['ring_r']:
                    dt.cut(q, rgb01('ring'))
                elif in_star(u, v, L['star_r'], L['star_in']):
                    for k in range(1, L['height'] + 1):
                        dt.build(tuple(q[n] + d[n] * k for n in range(3)), rgb01('star'))


def part_detail(part, ob, cells):
    if not edit.has_colours(ob):
        if not bl.pick_mode_check(ob, VOXEL_M):
            bl.split_to_cubes(ob, VOXEL_M)
        edit.convert(ob, VOXEL_M)
    s = edit.Solid(ob, VOXEL_M)
    g = Gun(s, cells)
    dt = Detail(s)

    for p, side, y, pts in FINE_LINES:                                # panel lines and slashes
        if p != part:
            continue
        for sign in sides(side):
            for x, z in raster(pts):
                q = surface(s, g, sign, y, x, z)
                if q:
                    dt.cut(q, rgb01('line'))

    for p, side, y, centres in FINE_SCREWS:                           # raised screw heads with a slot
        if p != part:
            continue
        for sign in sides(side):
            d = out_dir(sign)
            for cx, cz in centres:
                for i in range(-2, 3):
                    for j in range(-2, 3):
                        if abs(i) == abs(j) == 2 or (j == 0 and abs(i) <= 1):
                            continue
                        q = surface(s, g, sign, y, cx + i / F, cz + j / F)
                        if q:
                            dt.build(tuple(q[n] + d[n] for n in range(3)), rgb01('screw'))

    for p, side, y, x0, z_top, pattern, dot, colour in FINE_STAMPS:   # raised marks
        if p != part:
            continue
        for sign in sides(side):
            d = out_dir(sign)
            for r, line in enumerate(pattern):
                for c, ch in enumerate(line):
                    if ch != '#':
                        continue
                    for a in range(dot):
                        for b in range(dot):
                            q = surface(s, g, sign, y, x0 + (c * dot + a) / F, z_top - (r * dot + b) / F)
                            if q:
                                dt.build(tuple(q[n] + d[n] for n in range(3)), rgb01(colour))

    if part == 'frame':
        logo(s, g, dt)

    dt.paint_cuts()
    small.tidy(s)
    s.write()
    print(ob.name, dt.stats)
    return dt.stats


def run():
    """The fine detail, then scratches on every part (bd_wear.carve, as on the shotgun)."""
    g = bd_pistol_gun.build()
    out = {}
    for part in {p for p, *_ in FINE_LINES + FINE_SCREWS + FINE_STAMPS}:
        out[part] = part_detail(part, bpy.data.objects[PARTS[part]], set(g.p[part]))
    bd_wear.carve([PARTS[k] for k in g.p if k in PARTS and g.p[k]], WEAR, lighten=SCRATCH_LIGHTEN)
    return out
