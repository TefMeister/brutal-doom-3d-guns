# Put our cube guns into GZDoom VR over Brutal Doom's weapons: a first, static test build (2026-10-19).
#   blender.exe -b <gun.blend> --python tools/gz_vr_export.py -- <gun> <out folder>
#   gun: pistol | shotgun | machinegun
#
# Tefa 2026-10-19: "can you see if you can get DOOM 1 working in VR with the brutal doom mod and our first 3 weapons
# in it?" Each gun is exported as it stands in its .blend (gun + Doomguy's gloves), one pose for every sprite frame
# of the Brutal Doom weapon it replaces: no animation yet.
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
    "pistol":     ("BDP_Root", "BDP_Glove_Root", "BDP_glove_right", "BrutalPistol", ["PIST", "PISR", "PISS", "2ISR"]),
    "shotgun":    ("BD_Root",  "BD_Gloves_Root", "BD_glove_right",  "Shot_Gun",     ["SHTA", "SHTN", "SHT8"]),
    "machinegun": ("BDM_Root", "BDM_Gloves_Root", "BDM_glove_right", "Rifle",       ["RIFG", "RIFF", "RIFR", "RIFZ", "RI2G", "2IFR"]),
}
ROOT, GLOVES, RIGHT_GLOVE, ACTOR, SPRITES = GUNS[GUN]
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"   # every frame letter of those sprites shows the gun (no animation yet)
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
faces = []                     # (three corners [(pos, normal)], colour key)
for o in meshes:
    eo = o.evaluated_get(dg)
    me = eo.to_mesh()
    col = me.attributes.get("cubekit_view") or me.attributes.get("cubekit_base")
    if col is None or col.domain != 'CORNER':
        print(f"  skipped {o.name}: no cubekit colour layer")
        eo.to_mesh_clear()
        continue
    M = inv @ eo.matrix_world
    R = M.to_3x3()
    n_before = len(faces)
    for poly in me.polygons:
        c = col.data[poly.loop_start].color
        key = (srgb(c[0]), srgb(c[1]), srgb(c[2]))
        n = (R @ poly.normal).normalized()
        loops = list(poly.loop_indices)
        for k in range(1, len(loops) - 1):
            tri = [(to_md3(M @ me.vertices[me.loops[li].vertex_index].co), (n.y, n.x, n.z)) for li in (loops[0], loops[k + 1], loops[k])]
            faces.append((tri, key))
    eo.to_mesh_clear()
    print(f"  {o.name}: {len(faces) - n_before} triangles")

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

verts, uvs = [], []
for tri, key in faces:
    i = index[key]
    uv = ((i % side + 0.5) / side, 1.0 - (i // side + 0.5) / side)   # the writer flips t back
    for v in tri:
        verts.append(v)
        uvs.append(uv)
tris = [(j, j + 1, j + 2) for j in range(0, len(uvs), 3)]
nsurf, nv, nt = write_md3(os.path.join(OUT, GUN + ".md3"), GUN, [verts], (tris, uvs), f"{MODEL_PATH}/{png}")
print(f"{GUN}: {nt} triangles, {nsurf} surfaces, {len(palette)} colours in a {side}x{side} palette")

lines = [f"// Generated by brutal-doom-3d-guns/tools/gz_vr_export.py ({GUN}). Do not edit by hand.",
         f"Model {ACTOR}", "{", f'   Path "{MODEL_PATH}"', f'   Model 0 "{GUN}.md3"', f'   Skin 0 "{png}"']
lines += [f'   SurfaceSkin 0 {i} "{png}"' for i in range(nsurf)]
lines += ["   Scale 1.0 1.0 1.0", "   NOINTERPOLATION", ""]
for spr in SPRITES:
    lines += [f"   FrameIndex {spr} {L} 0 0" for L in LETTERS]
lines += ["}"]
with open(os.path.join(OUT, f"modeldef.{GUN}.txt"), "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"{GUN}: modeldef written")
