# Doomguy's gloves on one forge gun, in its own .blend, with no Blender window (2026-10-19, a first pass done alone,
# looked at together later: Tefa "can you do gloves on all the other weapons now?" then "Yes, alone, review later").
#   blender -b <forge blend> --python gloves/forge_gloves_run.py -- <gun> <check picture dir>
# Builds the gun's cubes again from forge/<gun>.py (to know where the gun is), fits the gloves with fit_gloves.py, makes
# them with the gloves' own builder (bd_glove_live.run, the same as the shotgun / pistol / machine gun), saves the
# .blend (Blender keeps the old one as .blend1) and renders two check pictures of gun + gloves.
import importlib.util
import math
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
for p in (HERE, os.path.join(REPO, "forge"), os.path.join(REPO, "shotgun"),
          os.path.abspath(os.path.join(REPO, "..", "blender-cubekit"))):
    sys.path.insert(0, p)

import bd_glove_live                       # noqa: E402
import fit_gloves                          # noqa: E402
from bd_glove_settings import RIGHT_POSE, LEFT_POSE   # noqa: E402

args = sys.argv[sys.argv.index("--") + 1:]
GUN, SHOTS = args[0], args[1]

spec = importlib.util.spec_from_file_location("design", os.path.join(REPO, "forge", GUN + ".py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
model = mod.build()
cells = set(model.full) | set(model.fine)               # everything the gloves must not go inside
body = {c for c, v in model.full.items() if v[2] != 'mag'}   # where hands may hold: not the magazines
body |= {c for c, subs in model.fine.items() if any(s[2] != 'mag' for s in subs.values())}
right, left, sides, found = fit_gloves.poses(GUN, body, model.pivot)
print(f"GLOVES {GUN}: {found}")

tag = "BDF_" + GUN
folder = os.path.dirname(bpy.data.filepath)
upright = bool(left and left.pop('upright', False))
objs = bd_glove_live.run(folder, gun_parts={"all": cells}, pivot=model.pivot, right=dict(RIGHT_POSE, **right),
                         left=dict(LEFT_POSE, **left) if left and not upright else None,
                         sides=sides if not upright else ('right',),
                         names={"right": tag + "_glove_right", "left": tag + "_glove_left"},
                         collection=GUN + " gloves", root_name=tag + "_Gloves_Root", atlas=GUN + "_gloves_atlas.png")
if upright:
    # the left hand on an upright front grip: a right-hand grip pose there, built against the mirrored gun, then the
    # object mirrored across the gun's middle (Blender x is the gun's -y about the pivot), faces turned back outward
    import bmesh
    from mathutils import Matrix
    mirrored = {(x, 2 * model.pivot[1] - y, z) for x, y, z in cells}
    more = bd_glove_live.run(folder, gun_parts={"all": mirrored}, pivot=model.pivot, right=dict(RIGHT_POSE, **left),
                             sides=('right',), names={"right": tag + "_glove_left"}, collection=GUN + " left glove",
                             root_name=tag + "_Left_Glove_Root", atlas=GUN + "_left_glove_atlas.png")
    for o in more.values():
        o.data.transform(Matrix.Scale(-1, 4, (1, 0, 0)))
        bm = bmesh.new()
        bm.from_mesh(o.data)
        bmesh.ops.reverse_faces(bm, faces=bm.faces[:])
        bm.to_mesh(o.data)
        bm.free()
        o.data.update()
    objs = dict(objs, **{"left": o for o in more.values()})
bpy.ops.file.pack_all()
bpy.ops.wm.save_mainfile()

# two check pictures: from the right side, and from behind as the player holds it
sc = bpy.context.scene
sc.render.engine = 'BLENDER_WORKBENCH'
sc.display.shading.light = 'STUDIO'
sc.display.shading.color_type = 'TEXTURE'
sc.render.resolution_x, sc.render.resolution_y = 640, 400
meshes = [o for o in sc.objects if o.type == 'MESH' and not o.hide_render]
pts = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
mid, size = (lo + hi) / 2, max((hi - lo).length, 0.1)
cam = bpy.data.objects.new("glove_check_cam", bpy.data.cameras.new("glove_check_cam"))
sc.collection.objects.link(cam)
sc.camera = cam
os.makedirs(SHOTS, exist_ok=True)
for view, d in (("side", Vector((-1, 0, 0.15))), ("player", Vector((0.35, -1, 0.45)))):
    cam.location = mid + d.normalized() * size * 1.35
    cam.rotation_euler = (mid - cam.location).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = os.path.join(SHOTS, f"{GUN}_{view}.png")
    bpy.ops.render.render(write_still=True)
bpy.data.objects.remove(cam)
print(f"GLOVES {GUN}: done, {len(objs)} gloves")
