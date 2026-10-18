# Carved wear on the Brutal Doom cube shotgun, in the OPEN Blender file, after bd_live.run(): fine scratches dug out
# with the kit's smallest cubes (0.85 mm), bare metal inside each cut (blender-cubekit carve_wear.py).
# MCP: import bd_wear; bd_wear.run(). bd_live.run() rebuilds the parts plain, so run this again after it.
# carve() is shared: the gloves use it with their own numbers.
import random
import zlib

import bpy

import bl
import edit
import carve_wear as cw
from bd_settings import VOXEL_M, WEAR, COL

PARTS = ("BD_body", "BD_pump")


def carve(names, wear, bare_rgb=None, lighten=None):
    """Scratches only, on metal and paint, never on wood: wear = the WEAR dict. Inside the cuts: bare_rgb (sRGB 0-255),
    or, with lighten, each cut's own colour times lighten (1.4 = 40% lighter)."""
    cw.SCRATCH_PER_CM2 = wear['scratch_per_cm2']
    cw.SCRATCH_MM = wear['scratch_mm']
    cw.ALONG_SHARE = wear['along_share']
    cw.GOUGE_SHARE = wear['gouge_share']
    cw.ZIGZAG_SHARE = wear['zigzag_share']
    cw.SOFT_SCRATCH_PER_CM2 = cw.CHIP_PER_CM = cw.SOFT_CHIP_PER_CM = cw.PIT_PER_CM2 = 0
    if lighten:
        def bare(rgb):
            return tuple(min(1.0, c * lighten) for c in rgb)
    else:
        bare = tuple(c / 255.0 for c in bare_rgb)
    for name in names:
        ob = bpy.data.objects[name]
        if not edit.has_colours(ob):
            if not bl.pick_mode_check(ob, VOXEL_M):
                bl.split_to_cubes(ob, VOXEL_M)
            edit.convert(ob, VOXEL_M)
        rng = random.Random(wear['seed'] + zlib.crc32(name.encode()))
        print(name, cw.carve_object(ob, rng, bare=bare))


def run():
    carve(PARTS, WEAR, COL['bare_steel'])
