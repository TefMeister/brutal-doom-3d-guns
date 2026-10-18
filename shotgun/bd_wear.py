# Carved wear on the Brutal Doom cube shotgun, in the OPEN Blender file, after bd_live.run(): fine scratches dug out
# with the kit's smallest cubes (0.85 mm), bright bare steel inside each cut (blender-cubekit carve_wear.py).
# MCP: import bd_wear; bd_wear.run(). bd_live.run() rebuilds the parts plain, so run this again after it.
import random
import zlib

import bpy

import bl
import edit
import carve_wear as cw
from bd_settings import VOXEL_M, WEAR, COL

PARTS = ("BD_body", "BD_pump")


def run():
    cw.SCRATCH_PER_CM2 = WEAR['scratch_per_cm2']
    cw.SCRATCH_MM = WEAR['scratch_mm']
    cw.ALONG_SHARE = WEAR['along_share']
    cw.GOUGE_SHARE = WEAR['gouge_share']
    cw.SOFT_SCRATCH_PER_CM2 = cw.CHIP_PER_CM = cw.SOFT_CHIP_PER_CM = cw.PIT_PER_CM2 = 0
    bare = tuple(c / 255.0 for c in COL['bare_steel'])
    for name in PARTS:
        ob = bpy.data.objects[name]
        if not edit.has_colours(ob):
            if not bl.pick_mode_check(ob, VOXEL_M):
                bl.split_to_cubes(ob, VOXEL_M)
            edit.convert(ob, VOXEL_M)
        rng = random.Random(WEAR['seed'] + zlib.crc32(name.encode()))
        print(name, cw.carve_object(ob, rng, bare=bare))
