# Put our cube guns into GZDoom VR over Brutal Doom's weapons: a first, static test build (2026-10-19).
#   blender.exe -b <gun.blend> --python tools/gz_vr_export.py -- <gun> <out folder>
#   gun: pistol | shotgun | machinegun
#
# Tefa 2026-10-19: "can you see if you can get DOOM 1 working in VR with the brutal doom mod and our first 3 weapons
# in it?" Each gun is exported as it stands in its .blend (gun + Doomguy's gloves), one pose for every sprite frame
# of the Brutal Doom weapon it replaces: no animation yet.
# 2026-10-19 (Tefa: "please animate the shooting animations, pump after each shotgun shot ... only the initial weapon
# pick up animation"): the poses per sprite frame come from tools/gz_anim.py. The gun is written as one MD3 per slot
# (<gun>_body.md3 + <gun>_<part>.md3), each with one frame per distinct pose it takes, and MODELDEF draws both.
#
# Why not ashes-2063-weapons/kit/gz_export.py as it is: our cube models keep their colours ON THE FACES (the corner
# colour layer `cubekit_view`, what the viewport shows), with no UV map; the atlas images in the .blend are empty.
# So this writes its own palette: every distinct face colour is one pixel of a small PNG, and every corner of a face
# points at the middle of its colour's pixel, so even a smoothed texture shows the exact colour. The whole gun (parts +
# gloves) is one MD3; the writer is the kit's (gz_md3.py, unchanged; it splits big models into surfaces), and the VR
# placement follows the Ashes revolver as Tefa tuned it in the headset (hand space, 100 units per metre, the grip 0.20 m
# ahead of and 0.16 m above the model origin; kit/gz_revolver.py).
import bpy, sys, os, zipfile
from mathutils import Vector

args = sys.argv[sys.argv.index("--") + 1:]
GUN, OUT = args[0], os.path.abspath(args[1])
KIT = os.path.join(os.path.expanduser("~"), "github-backups", "ashes-2063-weapons", "kit")
exec(open(os.path.join(KIT, "gz_md3.py")).read())
# GZDoom takes at most 32 surfaces per MD3 ("Invalid MD3 Surface 32", first launch 2026-10-19) and the kit splits at
# 4,000 vertices; these guns have 340,000-730,000, so the surfaces are made much bigger (GZDoom indexes them in 32 bit)
MAX_SURFACE_VERTS = 60000

# gun -> (root empty, glove root, right glove object, Brutal Doom weapon class, its sprites)
GUNS = {
    "pistol":     ("BDP_Root", "BDP_Glove_Root", "BDP_glove_right", "BrutalPistol", ["PIST", "PISR", "PISS", "PISI", "2ISR"]),
    "shotgun":    ("BD_Root",  "BD_Gloves_Root", "BD_glove_right",  "Shot_Gun",     ["SHTA", "SHTN", "SHT8"]),
    "machinegun": ("BDM_Root", "BDM_Gloves_Root", "BDM_glove_right", "Rifle",       ["RIFG", "RIFF", "RIFR", "RIFZ", "RI2G", "2IFR", "3IFR"]),
}
ROOT, GLOVES, RIGHT_GLOVE, ACTOR, SPRITES = GUNS[GUN]
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ["   # every frame letter of those sprites shows the gun ("[" = Doom's 27th)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gz_anim
ANIM = gz_anim.GUNS[GUN]
UNITS_PER_M = 100                        # VR: the model hangs off the controller in centimetres
GRIP_FROM_ORIGIN = Vector((0.0, 0.20, -0.16))   # the Ashes revolver's tuned grip spot (see the header)
MODEL_PATH = "models/bd3dguns/" + GUN

sc = bpy.context.scene
root = sc.objects[ROOT]
inv = root.matrix_world.inverted()


def under(o, name):
    while o is not None:
        if o.name == name:
            return True
        o = o.parent
    return False


meshes = [o for o in sc.objects if o.type == 'MESH' and not o.hide_render and (under(o, ROOT) or under(o, GLOVES))]
meshes.sort(key=lambda o: o.name)

# the grip: the middle of the right glove, in the root's space
g = sc.objects[RIGHT_GLOVE]
pts = [inv @ (g.matrix_world @ Vector(c)) for c in g.bound_box]
grip = sum(pts, Vector()) / len(pts)
origin = grip - GRIP_FROM_ORIGIN
print(f"{GUN}: {len(meshes)} parts, grip {tuple(round(v, 3) for v in grip)}, origin {tuple(round(v, 3) for v in origin)}")


def to_md3(p):   # GZDoom draws MD3 +Y on the viewer's RIGHT (the kit's note): MD3 x = forward, y = right, z = up
    q = p - origin
    return (q.y * UNITS_PER_M, q.x * UNITS_PER_M, q.z * UNITS_PER_M)


os.makedirs(OUT, exist_ok=True)
import struct, zlib


def srgb(c):   # the colour layer is linear; the PNG is sRGB
    c = max(0.0, min(1.0, c))
    return int(round(255 * (12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055)))


dg = bpy.context.evaluated_depsgraph_get()
slot_of = {}                   # mesh name -> slot index; a part no slot names goes with the body (slot 0)
for si, (_, names) in enumerate(ANIM["slots"]):
    for nm in names:
        slot_of[nm] = si
slot_faces = [[] for _ in ANIM["slots"]]   # per slot: (three corners [(pos m, normal)], colour key)
for o in meshes:
    eo = o.evaluated_get(dg)
    me = eo.to_mesh()
    col = me.attributes.get("cubekit_view") or me.attributes.get("cubekit_base")
    if col is None or col.domain != 'CORNER':
        print(f"  skipped {o.name}: no cubekit colour layer")
        eo.to_mesh_clear()
        continue
    if o.name not in slot_of:
        print(f"  {o.name}: in no animation slot, moves with the body")
    faces = slot_faces[slot_of.get(o.name, 0)]
    M = inv @ eo.matrix_world
    R = M.to_3x3()
    n_before = len(faces)
    for poly in me.polygons:
        c = col.data[poly.loop_start].color
        key = (srgb(c[0]), srgb(c[1]), srgb(c[2]))
        n = (R @ poly.normal).normalized()
        loops = list(poly.loop_indices)
        for k in range(1, len(loops) - 1):
            tri = [(tuple(M @ me.vertices[me.loops[li].vertex_index].co), tuple(n)) for li in (loops[0], loops[k + 1], loops[k])]
            faces.append((tri, key))
    eo.to_mesh_clear()
    print(f"  {o.name}: {len(faces) - n_before} triangles (slot {ANIM['slots'][slot_of.get(o.name, 0)][0]})")
faces = [f for fs in slot_faces for f in fs]

palette = sorted({key for _, key in faces})
side = 1
while side * side < len(palette):
    side *= 2
index = {key: i for i, key in enumerate(palette)}
rows = []
for y in range(side):
    row = bytearray(b"\x00")
    for x in range(side):
        i = y * side + x
        row += bytes(palette[i]) if i < len(palette) else b"\x00\x00\x00"
    rows.append(bytes(row))


def chunk(tag, data):
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


png = f"{GUN}.png"
with open(os.path.join(OUT, png), "wb") as f:
    f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", side, side, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(b"".join(rows), 9)) + chunk(b"IEND", b""))

# the poses: every sprite frame the gun shows -> (pose, travel); the rest pose is always frame 0
keys = {(spr, L): gz_anim.pose_of(GUN, spr, L) for spr in SPRITES for L in LETTERS}
pivot = tuple(grip)


import numpy as np
O = np.array(tuple(origin))


def md3_frame(P, N, R, tr):   # every corner of a slot in one pose, as the MD3 writer wants them (numpy: 2026-10-19,
    R = np.array(R)            # the per-corner Python maths took over 20 minutes for the shotgun)
    q = (P @ R.T + np.array(tr) - O) * UNITS_PER_M
    m = N @ R.T
    return list(zip(map(tuple, q[:, [1, 0, 2]].tolist()), map(tuple, m[:, [1, 0, 2]].tolist())))


models = []                    # (md3 file, surfaces, {pose key: frame number})
for si, (sname, _) in enumerate(ANIM["slots"]):
    faces_s = slot_faces[si]
    if not faces_s:
        print(f"{GUN}: slot {sname} is empty")
        continue
    poses = [("rest", 0.0)]
    for k in sorted(set(keys.values())):
        k = k if si > 0 else (k[0], 0.0)   # the body never slides
        if k not in poses:
            poses.append(k)
    uvs = []
    for tri, key in faces_s:
        i = index[key]
        uvs += [((i % side + 0.5) / side, 1.0 - (i // side + 0.5) / side)] * 3   # the writer flips t back
    tris = [(j, j + 1, j + 2) for j in range(0, len(uvs), 3)]
    P = np.array([p for tri, _ in faces_s for p, _ in tri])
    N = np.array([n for tri, _ in faces_s for _, n in tri])
    frames = []
    for pose, travel in poses:
        R, tr = gz_anim.pose_transform(GUN, pose, travel, pivot, si)
        frames.append(md3_frame(P, N, R, tr))
    md3 = f"{GUN}_{sname}.md3"
    nsurf, nv, nt = write_md3(os.path.join(OUT, md3), f"{GUN}_{sname}", frames, (tris, uvs), f"{MODEL_PATH}/{png}")
    models.append((md3, nsurf, {k: fi for fi, k in enumerate(poses)}))
    print(f"{GUN}: {md3}: {nt} triangles, {nsurf} surfaces, {len(frames)} frames "
          f"({os.path.getsize(os.path.join(OUT, md3)) // 1048576} MB)")
print(f"{GUN}: {len(palette)} colours in a {side}x{side} palette")

lines = [f"// Generated by brutal-doom-3d-guns/tools/gz_vr_export.py ({GUN}) with tools/gz_anim.py. Do not edit by hand.",
         f"Model {ACTOR}", "{", f'   Path "{MODEL_PATH}"']
for mi, (md3, nsurf, _) in enumerate(models):
    lines += [f'   Model {mi} "{md3}"', f'   Skin {mi} "{png}"']
    lines += [f'   SurfaceSkin {mi} {i} "{png}"' for i in range(nsurf)]
lines += ["   Scale 1.0 1.0 1.0", "   NOINTERPOLATION", ""]
for spr in SPRITES:
    for L in LETTERS:
        pose, travel = keys[(spr, L)]
        for mi, (_, _, frame_of) in enumerate(models):
            lines.append(f"   FrameIndex {spr} {L} {mi} {frame_of[(pose, travel if mi > 0 else 0.0)]}")
lines += ["}"]
with open(os.path.join(OUT, f"modeldef.{GUN}.txt"), "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"{GUN}: modeldef written")
