# Fine detail on the Brutal Doom cube machine gun, in the OPEN Blender file, after bd_mg_live.run(): panel lines cut
# with the kit's smallest cubes (0.85 mm), screw heads and marks built of them, fine blood spatter around the dried
# stains, then the carved scratches. The pistol's bd_pistol_fine.py way (shotgun/bd_fine.py, bd_wear.py).
# Numbers: FINE_*, BLOOD and WEAR in bd_mg_settings.py. MCP: import bd_mg_fine; bd_mg_fine.run().
import math
import os
import random
import sys

import bpy

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shotgun"))   # bd_fine

import bl
import edit
import edit_small as small
import bd_mg_gun
import bd_wear
from bd_fine import Gun, Detail, surface, raster, sides, out_dir
from bd_mg_settings import VOXEL_M, FINE_LINES, FINE_SCREWS, FINE_STAMPS, FINE_COL, WEAR, SCRATCH_LIGHTEN, BLOOD
from bd_mg_live import PARTS

F = edit.FINE
SPATTER_SCAN = dict(y=10, tol=20)   # spatter looks for the surface from just outside the widest part, this far in


def rgb01(name):
    return tuple(c / 255.0 for c in FINE_COL[name])


def spatter(s, g, dt, stains):
    """Small dark dots flung around each side stain, one small cube deep."""
    rng = random.Random(BLOOD['seed'] + 1)
    for side, x, z, r in stains:
        if not side:
            continue
        for _ in range(rng.randint(*BLOOD['spatter'])):
            a = rng.uniform(0, 2 * math.pi)
            d = r * rng.uniform(*BLOOD['spatter_reach'])
            q = surface(s, g, side, SPATTER_SCAN['y'], x + d * math.cos(a), z + d * math.sin(a),
                        tol=SPATTER_SCAN['tol'])
            if q:
                dt.cut(q, rgb01('spatter'))


def part_detail(part, ob, cells, stains):
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

    if part == 'body':
        spatter(s, g, dt, stains)

    dt.paint_cuts()
    small.tidy(s)
    s.write()
    print(ob.name, dt.stats)
    return dt.stats


def run():
    """The fine detail, then scratches on every part (bd_wear.carve, as on the shotgun and pistol)."""
    g = bd_mg_gun.build()
    out = {}
    for part in {p for p, *_ in FINE_LINES + FINE_SCREWS + FINE_STAMPS} | {'body'}:
        out[part] = part_detail(part, bpy.data.objects[PARTS[part]], set(g.p[part]), g.stains)
    bd_wear.carve([PARTS[k] for k in g.p if k in PARTS and g.p[k]], WEAR, lighten=SCRATCH_LIGHTEN)
    return out
