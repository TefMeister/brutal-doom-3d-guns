# Builds the Brutal Doom cube shotgun into the OPEN Blender file, beside the references, for working on it
# together with Tefa (MCP: import bd_live; bd_live.run(<atlas folder>)). Replaces its own objects each time and
# never touches anything else in the file.
import importlib
import os

import bpy

import bd_settings
import bd_gun
importlib.reload(bd_settings)
importlib.reload(bd_gun)
from bd_settings import VOXEL_M, PIVOT, COL, SHADE, NOISE
from bl import Space, make_objects

COLLECTION = "BD shotgun"
ROOT = "BD_Root"
PARTS = {"body": "BD_body"}        # cube part -> Blender object


def paint(cells):
    return {c: COL[name] for c, name in cells.items()}


def run(atlas_dir):
    col = bpy.data.collections.get(COLLECTION) or bpy.data.collections.new(COLLECTION)
    if col.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(col)
    for o in list(col.objects):
        bpy.data.objects.remove(o)
    root = bpy.data.objects.new(ROOT, None)
    col.objects.link(root)
    g = bd_gun.build()
    specs = [(PARTS[k], paint(v), PIVOT) for k, v in g.p.items() if k in PARTS]
    os.makedirs(atlas_dir, exist_ok=True)
    objs = make_objects(specs, root, os.path.join(atlas_dir, "bd_shotgun_atlas.png"), Space(VOXEL_M, PIVOT),
                        SHADE, NOISE)
    for o in objs.values():
        for c in list(o.users_collection):
            c.objects.unlink(o)
        col.objects.link(o)
    print("cubes:", {k: len(v) for k, v in g.p.items()})
    return objs
