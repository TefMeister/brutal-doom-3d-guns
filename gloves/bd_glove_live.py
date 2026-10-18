# Builds Doomguy's right glove into the OPEN Blender file, beside the shotgun, for shaping it together with Tefa
# (MCP: import bd_glove_live; bd_glove_live.run(<atlas folder>)). Replaces its own objects each time and never touches
# anything else in the file.
import importlib
import os
import sys

import bpy

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shotgun"))   # bd_wear.carve

import bd_glove_settings
import bd_glove
importlib.reload(bd_glove_settings)
importlib.reload(bd_glove)
from bd_glove_settings import VOXEL_M, COL, SHADE, NOISE, SHOW_AT, WEAR, BARE
import bl
import edit
import bd_wear
from bl import Space, make_objects

COLLECTION = "BD gloves"
ROOT = "BD_Gloves_Root"


def run(atlas_dir):
    col = bpy.data.collections.get(COLLECTION) or bpy.data.collections.new(COLLECTION)
    if col.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(col)
    for o in list(col.objects):
        bpy.data.objects.remove(o)
    root = bpy.data.objects.new(ROOT, None)
    root.location = SHOW_AT
    col.objects.link(root)
    cells = {c: COL[n] for c, n in bd_glove.right_glove().items()}
    os.makedirs(atlas_dir, exist_ok=True)
    objs = make_objects([("BD_glove_right", cells, (0, 0, 0))], root, os.path.join(atlas_dir, "bd_gloves_atlas.png"),
                        Space(VOXEL_M, (0, 0, 0)), SHADE, NOISE)
    for o in objs.values():
        for c in list(o.users_collection):
            c.objects.unlink(o)
        col.objects.link(o)
        # colours onto the mesh as well, like the carved shotgun, so both show in the same viewport mode
        if not bl.pick_mode_check(o, VOXEL_M):
            bl.split_to_cubes(o, VOXEL_M)
        edit.convert(o, VOXEL_M)
    bd_wear.carve([o.name for o in objs.values()], WEAR, BARE)
    print("glove cubes:", len(cells))
    return objs
