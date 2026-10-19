# Render chosen frames of an animation preview blend (tools/gz_anim_preview.py) to a picture sheet, from the side and
# from behind the gun as the player sees it, to check the poses without opening Blender (2026-10-19).
#   blender.exe -b <gun>_anim_preview.blend --python tools/gz_anim_shots.py -- <out.png> <marker>+<offset> ...
# e.g. fire+0 fire+2 first_pickup+20. Workbench, the faces' own colours (the cubekit colour layer).
import bpy, sys, os, math
from mathutils import Vector

args = sys.argv[sys.argv.index("--") + 1:]
OUT, SHOTS = args[0], args[1:]
sc = bpy.context.scene
markers = {m.name: m.frame for m in sc.timeline_markers}
for o in sc.objects:   # only the animated gun: the pistol and machine gun blends still hold an old shotgun copy
    if o.type == 'MESH' and not (o.animation_data and o.animation_data.action):
        o.hide_render = True
sc.render.engine = 'BLENDER_WORKBENCH'
sc.display.shading.light = 'STUDIO'
sc.display.shading.color_type = 'VERTEX'
sc.render.resolution_x, sc.render.resolution_y = 360, 270
sc.render.film_transparent = False
sc.world.color = (0.08, 0.08, 0.1) if sc.world else None

cam_data = bpy.data.cameras.new("shots_cam")
cam_data.lens = 50
cam = bpy.data.objects.new("shots_cam", cam_data)
sc.collection.objects.link(cam)
sc.camera = cam
VIEWS = {   # (camera position, looks at): the gun lies along +Y, grip near the origin
    "side": (Vector((-1.6, 0.25, 0.05)), Vector((0.0, 0.25, 0.0))),
    "player": (Vector((0.25, -0.75, 0.30)), Vector((0.0, 0.30, 0.0))),
}
tiles = []
tmp = os.path.join(os.path.dirname(OUT), "_shots_tmp")
os.makedirs(tmp, exist_ok=True)
for shot in SHOTS:
    name, off = shot.split("+")
    f = markers[name] + int(off)
    sc.frame_set(f)
    for vname, (pos, at) in VIEWS.items():
        cam.location = pos
        cam.rotation_euler = (at - pos).to_track_quat('-Z', 'Y').to_euler()
        p = os.path.join(tmp, f"{shot.replace('+', '_')}_{vname}.png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        tiles.append((f"{shot} {vname}", p))

# stitch: one row per shot, side then player view
W, H = sc.render.resolution_x, sc.render.resolution_y
img = bpy.data.images.new("sheet", W * 2, H * len(SHOTS))
px = [0.0] * (W * 2 * H * len(SHOTS) * 4)
for k, (_, p) in enumerate(tiles):
    im = bpy.data.images.load(p)
    src = list(im.pixels)
    row = len(SHOTS) - 1 - k // 2       # Blender images start at the bottom
    col = k % 2
    for y in range(H):
        a = (y * W) * 4
        b = ((row * H + y) * W * 2 + col * W) * 4
        px[b:b + W * 4] = src[a:a + W * 4]
img.pixels = px
img.filepath_raw = OUT
img.file_format = 'PNG'
img.save()
print("sheet:", OUT, [t[0] for t in tiles])
