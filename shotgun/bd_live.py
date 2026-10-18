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
from bd_settings import VOXEL_M, PIVOT, COL, SHADE, NOISE, RIGHT_HAND_MOVE, EDGE_WEAR
from bl import mix
from bl import Space, make_objects

COLLECTION = "BD shotgun"
ROOT = "BD_Root"
PARTS = {"body": "BD_body", "pump": "BD_pump", "trigger": "BD_trigger"}     # cube part -> Blender object
# the Ashes gun's own pieces, hidden once ours has a body (2026-10-18, Tefa: it "has to be different"); its hands stay
ASHES_GUN = ("Shotgun_body", "Shotgun_pump", "Shotgun_trigger", "Shotgun_shield", "Shotgun_bolt", "Shotgun_flash",
             "Shotgun_casing", "Shotgun_loadshell", "Shotgun_portshell")
RIGHT_HAND = "Shotgun_righthand"   # the Ashes right hand's carrier, copied into this file as a reference


def paint(cells):
    """Colour names -> sRGB, with the metal's long edges worn lighter where two of its sides are open."""
    out = {}
    for (x, y, z), name in cells.items():
        rgb = COL[name]
        if name in ('metal', 'metal_mid'):
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
    g = bd_gun.build()
    specs = [(PARTS[k], paint(v), PIVOT) for k, v in g.p.items() if k in PARTS]
    os.makedirs(atlas_dir, exist_ok=True)
    objs = make_objects(specs, root, os.path.join(atlas_dir, "bd_shotgun_atlas.png"), Space(VOXEL_M, PIVOT),
                        SHADE, NOISE)
    for o in objs.values():
        for c in list(o.users_collection):
            c.objects.unlink(o)
        col.objects.link(o)
    move_right_hand()
    for n in ASHES_GUN:
        o = bpy.data.objects.get(n)
        if o:
            o.hide_set(True)
            o.hide_render = True
    print("cubes:", {k: len(v) for k, v in g.p.items()})
    return objs


def move_right_hand():
    """Put the copied Ashes right hand on this gun's wrist: its first place is remembered, so a rerun never adds up."""
    h = bpy.data.objects.get(RIGHT_HAND)
    if not h:
        return
    if "ashes_location" not in h:
        h["ashes_location"] = tuple(h.location)
    base = Space(VOXEL_M, PIVOT)
    shift = base.to_bl(PIVOT[0] + RIGHT_HAND_MOVE[0], PIVOT[1] + RIGHT_HAND_MOVE[1], PIVOT[2] + RIGHT_HAND_MOVE[2])
    h.location = tuple(a + b for a, b in zip(h["ashes_location"], shift))
