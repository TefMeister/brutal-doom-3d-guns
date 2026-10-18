# Puts Doomguy's gloves on the Brutal Doom shotgun in the OPEN Blender file, in place of the Ashes hands, for shaping
# them together with Tefa (MCP: import bd_glove_live; bd_glove_live.run(<atlas folder>)). Replaces its own objects
# each time, hides the Ashes hands (never deletes them) and touches nothing else in the file.
import importlib
import os
import sys

import bpy

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shotgun"))   # bd_wear, bd_gun

import bd_glove_settings
import bd_glove
import bd_glove_pose
import bd_glove_fine
importlib.reload(bd_glove_settings)
importlib.reload(bd_glove)
importlib.reload(bd_glove_pose)
importlib.reload(bd_glove_fine)
from bd_glove_settings import VOXEL_M, COL, SHADE, NOISE, WEAR, SCRATCH_LIGHTEN
from bd_settings import PIVOT
import bd_gun
import bd_wear
import bl
import edit
from bl import Space, make_objects

COLLECTION = "BD gloves"
ROOT = "BD_Gloves_Root"
NAMES = {"right": "BD_glove_right", "left": "BD_glove_left"}
# the Ashes hands copied into this file, hidden once the gloves take their place
ASHES_HANDS = ("Hand_right_hand", "Hand_right_thumb", "Hand_right_tip", "Hand_left_hand", "Hand_left_thumb")


def run(atlas_dir, gun_parts=None, pivot=PIVOT, right=None, left=None, sides=('right', 'left'), names=NAMES,
        collection=COLLECTION, root_name=ROOT, atlas="bd_gloves_atlas.png"):
    """The shotgun's gloves by default. Another gun passes its parts ({part: cells}), its pivot, its poses (see
    bd_glove_pose.use), which hands, and its own object names, collection and atlas file."""
    col = bpy.data.collections.get(collection) or bpy.data.collections.new(collection)
    if col.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(col)
    for o in list(col.objects):
        bpy.data.objects.remove(o)
    root = bpy.data.objects.new(root_name, None)
    col.objects.link(root)
    gun = set()
    for cells in (gun_parts or bd_gun.build().p).values():
        gun |= set(cells)
    bd_glove_pose.use(right, left)
    posed = bd_glove_pose.gloves(gun, sides)
    specs = [(names[k], {c: COL[n] for c, n in v.items()}, pivot) for k, v in posed.items()]
    os.makedirs(atlas_dir, exist_ok=True)
    objs = make_objects(specs, root, os.path.join(atlas_dir, atlas), Space(VOXEL_M, pivot), SHADE, NOISE)
    for o in objs.values():
        for c in list(o.users_collection):
            c.objects.unlink(o)
        col.objects.link(o)
        # colours onto the mesh as well, like the carved shotgun, so both show in the same viewport mode
        if not bl.pick_mode_check(o, VOXEL_M):
            bl.split_to_cubes(o, VOXEL_M)
        edit.convert(o, VOXEL_M)
    bd_glove_fine.run(posed, names)                    # the small-cube detail and the Slayer's mark
    # each glove its own scratches: the seed is mixed with the object's name
    bd_wear.carve([o.name for o in objs.values()], WEAR, lighten=SCRATCH_LIGHTEN)
    for n in ASHES_HANDS:
        o = bpy.data.objects.get(n)
        if o:
            o.hide_set(True)
            o.hide_render = True
    print("glove cubes:", {k: len(v) for k, v in posed.items()})
    return objs
