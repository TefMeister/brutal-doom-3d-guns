# Key a gun's animations (tools/gz_anim.py) onto Blender's timeline and save them as a SEPARATE preview file, for
# looking at them together (2026-10-19, Tefa: "we'll look at them all together later and tweak what we have to then").
#   blender.exe -b <gun>.blend --python tools/gz_anim_preview.py -- <gun>
# Writes <gun blend>_anim_preview.blend next to the gun's .blend; the gun's own .blend is never saved over.
# One Blender frame per Doom tic, at Doom's 35 tics a second, stepped (constant keys) like the game shows it. A timeline
# marker names each animation (fire, first_pickup, raise) where it starts; ten rest frames separate them.
import bpy, sys, os
from mathutils import Matrix

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gz_anim

GUN = sys.argv[sys.argv.index("--") + 1]
ROOTS = {"shotgun": ("BD_Root", "BD_glove_right"), "pistol": ("BDP_Root", "BDP_glove_right"),
         "machinegun": ("BDM_Root", "BDM_glove_right")}
GAP = 10

sc = bpy.context.scene
A = gz_anim.GUNS[GUN]
root = sc.objects[ROOTS[GUN][0]]
inv = root.matrix_world.inverted()
g = sc.objects[ROOTS[GUN][1]]
from mathutils import Vector
pts = [inv @ (g.matrix_world @ Vector(c)) for c in g.bound_box]
pivot = tuple(sum(pts, Vector()) / len(pts))

slots = []                      # (slot index, object, its rest matrix in the root's space)
for si, (_, names) in enumerate(A["slots"]):
    for nm in names:
        o = sc.objects.get(nm)
        if o is None:
            print(f"  {nm}: not in this blend")
            continue
        o.animation_data_clear()
        o.rotation_mode = 'QUATERNION'
        slots.append((si, o, inv @ o.matrix_world.copy()))


def key(frame, pose, travel):
    for si, o, rest in slots:
        R, t = gz_anim.pose_transform(GUN, pose, travel if si > 0 else 0.0, pivot, si)
        P = Matrix(((R[0][0], R[0][1], R[0][2], t[0]), (R[1][0], R[1][1], R[1][2], t[1]),
                    (R[2][0], R[2][1], R[2][2], t[2]), (0, 0, 0, 1)))
        o.matrix_world = root.matrix_world @ P @ rest
        o.keyframe_insert("location", frame=frame)
        o.keyframe_insert("rotation_quaternion", frame=frame)


bpy.context.preferences.edit.keyframe_new_interpolation_type = 'CONSTANT'   # stepped, like the game (Blender 5's
frame = 1                                                                    # layered actions hide fcurves below)
sc.timeline_markers.clear()
for name, seq in A["sequences"].items():
    key(frame, "rest", 0.0)
    frame += GAP
    sc.timeline_markers.new(name, frame=frame)
    for spr, lets in seq:
        for L in lets:
            pose, travel = gz_anim.pose_of(GUN, spr, L)
            key(frame, pose, travel)
            frame += 1
key(frame, "rest", 0.0)
for _, o, _ in slots:
    if o.animation_data and o.animation_data.action:
        for fc in getattr(o.animation_data.action, "fcurves", []):
            for kp in fc.keyframe_points:
                kp.interpolation = 'CONSTANT'
sc.frame_start, sc.frame_end = 1, frame + GAP
sc.render.fps = 35
out = os.path.splitext(bpy.data.filepath)[0] + "_anim_preview.blend"
bpy.ops.wm.save_as_mainfile(filepath=out, copy=True)
print(f"{GUN}: preview with {len(A['sequences'])} animations, {frame} frames -> {out}")
