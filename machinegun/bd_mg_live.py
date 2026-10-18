# Builds the Brutal Doom cube machine gun into the OPEN Blender file, for working on it together with Tefa
# (MCP: import bd_mg_live; bd_mg_live.run(<atlas folder>)). The pistol's bd_pistol_live.py, renamed. Replaces its
# own objects each time and never touches anything else in the file.
import importlib
import os

import bpy

import bd_mg_settings
import bd_mg_gun
importlib.reload(bd_mg_settings)
importlib.reload(bd_mg_gun)
from bd_mg_settings import VOXEL_M, PIVOT, COL, SHADE, NOISE, EDGE_WEAR
from bl import mix
from bl import Space, make_objects

COLLECTION = "BD machine gun"
ROOT = "BDM_Root"
PARTS = {"body": "BDM_body", "mag": "BDM_mag", "trigger": "BDM_trigger", "charge": "BDM_charge"}


def paint(cells):
    """Colour names -> sRGB, with the metal's long edges worn lighter where two of its sides are open."""
    out = {}
    for (x, y, z), name in cells.items():
        rgb = COL[name]
        if name == 'metal':
            open_up = ((x, y, z + 1) not in cells) + ((x, y, z - 1) not in cells)
            open_side = ((x, y + 1, z) not in cells) + ((x, y - 1, z) not in cells)
            if open_up and open_side:
                rgb = mix(rgb, COL['metal_hi'], EDGE_WEAR)
        out[(x, y, z)] = rgb
    return out


def run(atlas_dir):
    col = bpy.data.collections.get(COLLECTION) or bpy.data.collections.new(COLLECTION)
    if col.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(col)
    for o in list(col.objects):
        bpy.data.objects.remove(o)
    root = bpy.data.objects.new(ROOT, None)
    col.objects.link(root)
    g = bd_mg_gun.build()
    specs = [(PARTS[k], paint(v), PIVOT) for k, v in g.p.items() if k in PARTS and v]
    os.makedirs(atlas_dir, exist_ok=True)
    objs = make_objects(specs, root, os.path.join(atlas_dir, "bd_mg_atlas.png"), Space(VOXEL_M, PIVOT),
                        SHADE, NOISE)
    for o in objs.values():
        for c in list(o.users_collection):
            c.objects.unlink(o)
        col.objects.link(o)
    print("cubes:", {k: len(v) for k, v in g.p.items()})
    return objs
