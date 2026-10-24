# A forge cube gun (blender-cubekit forge, 2026-10-19) into GZDoom VR as a still model held in the right hand: one MD3,
# one palette PNG and a MODELDEF block for every weapon class it stands in for. For Brutal Doom and Ashes 2063 alike.
#   blender.exe -b <gun.blend> --python tools/gz_forge_export.py -- <jobs.json> <gun> <out folder>
#
# Tefa, 2026-10-24: "please add all the weapons you have made so far into both brutal doom and ashes 2063 games, so i can
# test them out in 3d one after another and we can do blender work after that". No animation: every frame the weapon
# shows in the hand points at the one pose. The jobs file (tools/forge_jobs.py writes it) names, per gun, the classes
# and their (sprite, letter) frames; pickups on the floor keep their sprites (weapon_sprites.py).
#
# Colours: the forge parts carry theirs in a small palette texture through their UVs, the Ashes gloves in an atlas the
# same way, Doomguy's gloves on the faces (`cubekit_view`). Every face is one flat colour, so each triangle takes the
# texel under the middle of its UVs (or its face colour), and the colours go into one palette PNG as in
# gz_vr_export.py. Texture pixels are read as stored (sRGB), face colours are linear and converted.
# Placement: as the guns already in both games (the Ashes revolver as Tefa tuned it, 2026-09-17; gz_vr_export.py): 100
# units a metre, the middle of the right glove 0.20 m ahead of and 0.16 m above the model's origin.
import bpy, sys, os, json
import numpy as np
from mathutils import Vector

args = sys.argv[sys.argv.index("--") + 1:]
JOBS, GUN, OUT = args[0], args[1], os.path.abspath(args[2])
job = json.load(open(JOBS))[GUN]
KIT = os.path.join(os.path.expanduser("~"), "github-backups", "ashes-2063-weapons", "kit")
exec(open(os.path.join(KIT, "gz_md3.py")).read())
UNITS_PER_M = 100
GRIP_FROM_ORIGIN = Vector((0.0, 0.20, -0.16))
MAX_SURFACES = 32                  # GZDoom refuses an MD3 with more ("Invalid MD3 Surface 32", 2026-10-19)
NAME = job["name"]
MODEL_PATH = job["model_path"]

sc = bpy.context.scene
roots = [o for o in sc.objects if o.type == 'EMPTY' and o.name.endswith("_root")]
assert len(roots) == 1, f"{GUN}: expected one *_root empty, found {[o.name for o in roots]}"
root = roots[0]
inv = root.matrix_world.inverted()
meshes = sorted((o for o in sc.objects if o.type == 'MESH' and not o.hide_render), key=lambda o: o.name)

glove = [o for o in meshes if o.name.endswith("glove_right")]
grip_objs = glove or meshes        # no hand on it (the pipe bomb): the middle of the whole thing
pts = [inv @ (o.matrix_world @ Vector(c)) for o in grip_objs for c in o.bound_box]
lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
grip = (lo + hi) / 2
origin = grip - GRIP_FROM_ORIGIN
print(f"{GUN}: {len(meshes)} parts, grip from {'the right glove' if glove else 'the whole model'} "
      f"{tuple(round(v, 3) for v in grip)}")

images = {}


def texels(img):
    if img.name not in images:
        w, h = img.size
        a = np.empty(w * h * 4, dtype=np.float32)
        img.pixels.foreach_get(a)
        images[img.name] = a.reshape(h, w, 4)
    return images[img.name]


def srgb(c):
    c = np.clip(c, 0.0, 1.0)
    return np.where(c <= 0.0031308, 12.92 * c, 1.055 * np.power(c, 1 / 2.4) - 0.055)


dg = bpy.context.evaluated_depsgraph_get()
P_all, N_all, C_all = [], [], []
for o in meshes:
    eo = o.evaluated_get(dg)
    me = eo.to_mesh()
    me.calc_loop_triangles()
    nt = len(me.loop_triangles)
    if nt == 0:
        eo.to_mesh_clear()
        continue
    tl = np.empty(nt * 3, dtype=np.int32); me.loop_triangles.foreach_get("loops", tl)
    tp = np.empty(nt, dtype=np.int32); me.loop_triangles.foreach_get("polygon_index", tp)
    lv = np.empty(len(me.loops), dtype=np.int32); me.loops.foreach_get("vertex_index", lv)
    co = np.empty(len(me.vertices) * 3, dtype=np.float32); me.vertices.foreach_get("co", co)
    pn = np.empty(len(me.polygons) * 3, dtype=np.float32); me.polygons.foreach_get("normal", pn)
    pm = np.empty(len(me.polygons), dtype=np.int32); me.polygons.foreach_get("material_index", pm)
    M = np.array(inv @ eo.matrix_world)
    R = M[:3, :3]
    nrm = pn.reshape(-1, 3) @ R.T
    nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-12
    P = co.reshape(-1, 3)[lv[tl]] @ R.T + M[:3, 3]           # three corners per triangle, in the root's space
    col = me.attributes.get("cubekit_view") or me.attributes.get("cubekit_base")
    if col is not None and col.domain == 'CORNER':
        c = np.empty(len(me.loops) * 4, dtype=np.float32); col.data.foreach_get("color", c)
        rgb = np.round(255 * srgb(c.reshape(-1, 4)[tl[0::3], :3])).astype(np.int32)
        how = "face colours"
    else:
        uv = np.empty(len(me.loops) * 2, dtype=np.float32); me.uv_layers.active.data.foreach_get("uv", uv)
        uvm = uv.reshape(-1, 2)[tl].reshape(nt, 3, 2).mean(axis=1)
        rgb = np.zeros((nt, 3), dtype=np.int32)
        tri_mat = pm[tp]
        for mi, mat in enumerate(me.materials):
            img = next((n.image for n in mat.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image), None) \
                if mat and mat.use_nodes else None
            sel = tri_mat == mi
            if img is None or not sel.any():
                continue
            t = texels(img)
            h, w = t.shape[:2]
            px = np.clip((uvm[sel, 0] % 1.0 * w).astype(np.int32), 0, w - 1)
            py = np.clip((uvm[sel, 1] % 1.0 * h).astype(np.int32), 0, h - 1)
            rgb[sel] = np.round(255 * np.clip(t[py, px, :3], 0, 1)).astype(np.int32)
        how = "texture"
    P_all.append(P); N_all.append(np.repeat(nrm[tp], 3, axis=0)); C_all.append(rgb)
    print(f"  {o.name}: {nt} triangles ({how})")
    eo.to_mesh_clear()
P = np.concatenate(P_all); N = np.concatenate(N_all); C = np.concatenate(C_all)
ntri = len(C)

# the palette: one pixel per colour
keys, inverse = np.unique(C, axis=0, return_inverse=True)
inverse = inverse.reshape(-1)
side = 1
while side * side < len(keys):
    side *= 2
import struct, zlib
rows = []
for y in range(side):
    row = bytearray(b"\x00")
    for x in range(side):
        i = y * side + x
        row += bytes(int(v) for v in keys[i]) if i < len(keys) else b"\x00\x00\x00"
    rows.append(bytes(row))


def chunk(tag, data):
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


os.makedirs(OUT, exist_ok=True)
png = NAME + ".png"
with open(os.path.join(OUT, png), "wb") as f:
    f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", side, side, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(b"".join(rows), 9)) + chunk(b"IEND", b""))

# MD3 axes as every gun in both games: x forward, y right, z up (GZDoom draws MD3 +Y on the viewer's right), so
# Blender (x right, y forward) -> (y, x, z): a mirror, hence the corner order reversed (as gz_vr_export.py)
O = np.array(tuple(origin))
Q = (P - O) * UNITS_PER_M
Q = Q.reshape(ntri, 3, 3)[:, [0, 2, 1], :].reshape(-1, 3)[:, [1, 0, 2]]
Nm = N.reshape(ntri, 3, 3)[:, [0, 2, 1], :].reshape(-1, 3)[:, [1, 0, 2]]
u = (inverse % side + 0.5) / side
v = 1.0 - (inverse // side + 0.5) / side
uvs = list(zip(np.repeat(u, 3).tolist(), np.repeat(v, 3).tolist()))
verts = list(zip(map(tuple, Q.tolist()), map(tuple, Nm.tolist())))
tris = [(j, j + 1, j + 2) for j in range(0, len(uvs), 3)]
MAX_SURFACE_VERTS = max(60000, -(-len(uvs) // (MAX_SURFACES - 1) // 3) * 3)
nsurf, nv, nt = write_md3(os.path.join(OUT, NAME + ".md3"), NAME, [verts], (tris, uvs), f"{MODEL_PATH}/{png}")
assert nsurf <= MAX_SURFACES, f"{GUN}: {nsurf} surfaces"
print(f"{GUN}: {nt} triangles, {nsurf} surfaces, {len(keys)} colours, "
      f"{os.path.getsize(os.path.join(OUT, NAME + '.md3')) // 1048576} MB")

lines = [f"// Generated by brutal-doom-3d-guns/tools/gz_forge_export.py from the forge gun '{GUN}'. Do not edit by hand.",
         "// A still model: no animation yet; every frame the weapon shows in the hand points at it."]
for cls, frames in job["classes"].items():
    lines += [f"Model {cls}", "{", f'   Path "{MODEL_PATH}"', f'   Model 0 "{NAME}.md3"', f'   Skin 0 "{png}"']
    lines += [f'   SurfaceSkin 0 {i} "{png}"' for i in range(nsurf)]
    lines += ["   Scale 1.0 1.0 1.0", "   NOINTERPOLATION"]
    lines += [f"   FrameIndex {spr} {L} 0 0" for spr, L in frames]
    lines += ["}", ""]
with open(os.path.join(OUT, f"modeldef.{NAME}.txt"), "w") as f:
    f.write("\n".join(lines))
print(f"{GUN}: modeldef for {', '.join(job['classes'])}")
