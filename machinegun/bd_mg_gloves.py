# Doomguy's gloves on the Brutal Doom cube machine gun, in the OPEN Blender file, after bd_mg_live.run() and
# bd_mg_fine.run(): the gloves' own builder (gloves/bd_glove_live.py) with this gun's parts, pivot and poses.
# MCP: import bd_mg_gloves; bd_mg_gloves.run(<atlas folder>). Numbers: RIGHT_HAND, LEFT_HAND in bd_mg_settings.py.
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gloves"))

import bd_glove_live
import bd_mg_gun
from bd_glove_settings import RIGHT_POSE, LEFT_POSE
from bd_mg_settings import PIVOT, RIGHT_HAND, LEFT_HAND


def run(atlas_dir):
    return bd_glove_live.run(atlas_dir, gun_parts=bd_mg_gun.build().p, pivot=PIVOT,
                             right=dict(RIGHT_POSE, **RIGHT_HAND), left=dict(LEFT_POSE, **LEFT_HAND),
                             names={'right': 'BDM_glove_right', 'left': 'BDM_glove_left'},
                             collection="BD machine gun gloves", root_name="BDM_Gloves_Root",
                             atlas="bd_mg_gloves_atlas.png")
