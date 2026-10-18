# Doomguy's right glove on the Brutal Doom cube pistol, in the OPEN Blender file, after bd_pistol_live.run() and
# bd_pistol_fine.run(): the gloves' own builder (gloves/bd_glove_live.py) with this gun's parts, pivot and pose.
# MCP: import bd_pistol_gloves; bd_pistol_gloves.run(<atlas folder>). Numbers: RIGHT_HAND in bd_pistol_settings.py.
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gloves"))

import bd_glove_live
import bd_pistol_gun
from bd_glove_settings import RIGHT_POSE
from bd_pistol_settings import PIVOT, RIGHT_HAND


def run(atlas_dir):
    return bd_glove_live.run(atlas_dir, gun_parts=bd_pistol_gun.build().p, pivot=PIVOT,
                             right=dict(RIGHT_POSE, **RIGHT_HAND), sides=('right',),
                             names={'right': 'BDP_glove_right'}, collection="BD pistol glove",
                             root_name="BDP_Glove_Root", atlas="bd_pistol_glove_atlas.png")
