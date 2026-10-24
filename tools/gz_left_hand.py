# Doomguy's free LEFT hand for GZDoom VR, drawn on the left controller while a one-handed weapon is out.
#   blender.exe -b --factory-startup --python tools/gz_left_hand.py -- <out folder>
#
# ⭐ The game draws everything at the off hand (FollowOffhand, our GZDoomVR build; ashes-2063-weapons engine/README.md)
# with left and right swapped `[verified-live 2026-10-24, n=1, Ashes]`, which is why the 2026-10-19 hand here (the
# pistol's right glove mirrored into a left one) showed "a glove with the thumb still on the wrong side" (Tefa). Seen in
# the Ashes hand worn three times on 2026-10-24, the swap acts on the file's up and down: a hand facing palm-in, thumb up
# in the file showed palm-out; so the file holds the hand flipped top to bottom, and the game turns it back.
# Tefa, 2026-10-24: "then please do the same with doom loose left hand": the same as the Ashes hand they approved, a
# relaxed hand (not the trigger pose), palm towards the weapon, thumb on top, 3.5 cm lower and 4 cm further back than
# the middle of the palm.
# Built here as Doomguy's true LEFT glove (left_glove: the mirror of the approved right one, with the Slayer's mark on
# its back plate), with all its fine detail and scratches, then flipped top to bottom on the way out; the game's swap
# makes it the left glove again, so the mark reads the right way.
# Hand space (bd_glove_settings): x across (+x to the right of a right hand laid palm down), y wrist -> fingertips,
# z = back of the hand. Gun space: x forward, y the gun's LEFT, z up.
import bpy, sys, os, struct, zlib, importlib
from mathutils import Vector

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for sub in ("gloves", "shotgun", os.path.join("..", "blender-cubekit")):
    sys.path.insert(0, os.path.abspath(os.path.join(REPO, sub)))
import bd_glove_fine, bd_wear, bl, edit                       # noqa: E402
from bd_glove import left_glove                               # noqa: E402
from bd_glove_settings import VOXEL_M, COL, SHADE, NOISE, WEAR, SCRATCH_LIGHTEN, PALM_L, sc   # noqa: E402

OUT = os.path.abspath(sys.argv[sys.argv.index("--") + 1])
KIT = os.path.join(os.path.dirname(REPO), "ashes-2063-weapons", "kit")
exec(open(os.path.join(KIT, "gz_md3.py")).read())
MAX_SURFACE_VERTS = 60000          # GZDoom takes at most 32 surfaces; it indexes them in 32 bit (gz_vr_export.py)
UNITS_PER_M = 34                    # vr_vunits_per_meter in doom-vr.ini: world actors, not the weapon's hand space
NAME = "bd_left_hand"
OBJ = "BD_glove_free_left"
MODEL_PATH = "models/bd3dguns/lefthand"
# the Ashes hand's relaxed pose (ashes-2063-weapons tools/gz_left_hand.py), thumb lengths at this glove's size
RELAXED_CURLS = {"index": (18, 30, 18), "middle": (22, 36, 22), "ring": (26, 40, 24), "pinky": (30, 44, 26)}
RELAXED_THUMB = [(sc(14), 38, 14), (sc(12), 20, 30)]
HAND_DOWN_CM = 3.5
HAND_BACK_CM = 4.0


def axes(xh, yh, zh):
    """A left hand, fingers forward, back of the hand to the left (out), thumb (+x on a left hand) on top."""
    return (yh, zh, xh)


hand = left_glove(curls=RELAXED_CURLS, thumb=RELAXED_THUMB, back_top=False)   # poses are given as for the right hand
cells = {axes(*c): n for c, n in hand.items()}
palm = [axes(*c) for c in hand if 0 <= c[1] < PALM_L]
O = [(min(c[i] for c in palm) + max(c[i] for c in palm) + 1) / 2.0 for i in range(3)]


def solid(self, P):
    """bd_glove_fine.Hand.solid for this pose: hand space (quarter cubes) -> the glove object's small-cube grid."""
    F = bd_glove_fine.F
    cell = tuple(p // F for p in P)
    sub = tuple(p % F for p in P)
    x, y, z = axes(*cell)
    gs = axes(*sub)
    return self.g.at(F * x + gs[0], F * y + gs[1], F * z + gs[2])


bd_glove_fine.Hand.solid = solid
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o)
root = bpy.data.objects.new("BD_free_left_root", None)
bpy.context.scene.collection.objects.link(root)
os.makedirs(OUT, exist_ok=True)
objs = bl.make_objects([(OBJ, {c: COL[n] for c, n in cells.items()}, (0, 0, 0))], root,
                       os.path.join(OUT, "bd_free_left_atlas.png"), bl.Space(VOXEL_M, (0, 0, 0)), SHADE, NOISE)
g = objs[OBJ]
if not bl.pick_mode_check(g, VOXEL_M):
    bl.split_to_cubes(g, VOXEL_M)
edit.convert(g, VOXEL_M)
bd_glove_fine.run({"left": cells}, {"left": OBJ})            # the Slayer's mark, studs, stitching, grooves
bd_wear.carve([OBJ], WEAR, lighten=SCRATCH_LIGHTEN)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "bd_free_left_hand.blend"))

# the palm's middle in Blender metres (bl.Space: Blender = (-gun y, gun x, gun z) * cube)
ox, oy, oz = O[1] * -VOXEL_M, O[0] * VOXEL_M, O[2] * VOXEL_M
print(f"{NAME}: {len(cells)} cubes, palm middle gun ({O[0]:.1f}, {O[1]:.1f}, {O[2]:.1f})")


def srgb(c):
    c = max(0.0, min(1.0, c))
    return int(round(255 * (12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055)))


dg = bpy.context.evaluated_depsgraph_get()
eo = g.evaluated_get(dg)
me = eo.to_mesh()
col = me.attributes.get("cubekit_view") or me.attributes.get("cubekit_base")
M = root.matrix_world.inverted() @ g.matrix_world
R = M.to_3x3()
faces = []
for poly in me.polygons:
    c = col.data[poly.loop_start].color
    key = (srgb(c[0]), srgb(c[1]), srgb(c[2]))
    n = (R @ poly.normal).normalized()
    nm = (n.y, n.x, -n.z)                       # the guns' MD3 axes (kit gz_export: y and x swap), then top <-> bottom
    loops = list(poly.loop_indices)
    for k in range(1, len(loops) - 1):
        tri = []
        # the axis swap and the top/bottom flip are two flips: they cancel, so the corner order stays as Blender has it
        for li in (loops[0], loops[k], loops[k + 1]):
            p = M @ me.vertices[me.loops[li].vertex_index].co
            tri.append((((p.y - oy) * UNITS_PER_M - HAND_BACK_CM / 100.0 * UNITS_PER_M,
                         (p.x - ox) * UNITS_PER_M,
                         -(p.z - oz) * UNITS_PER_M + HAND_DOWN_CM / 100.0 * UNITS_PER_M), nm))
        faces.append((tri, key))
eo.to_mesh_clear()

palette = sorted({k for _, k in faces})
side = 1
while side * side < len(palette):
    side *= 2
index = {k: i for i, k in enumerate(palette)}
rows = []
for y in range(side):
    row = bytearray(b"\x00")
    for x in range(side):
        i = y * side + x
        row += bytes(palette[i]) if i < len(palette) else b"\x00\x00\x00"
    rows.append(bytes(row))


def chunk(tag, data):
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


os.makedirs(OUT, exist_ok=True)
png = NAME + ".png"
with open(os.path.join(OUT, png), "wb") as f:
    f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", side, side, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(b"".join(rows), 9)) + chunk(b"IEND", b""))
verts, uvs = [], []
for tri, key in faces:
    i = index[key]
    uv = ((i % side + 0.5) / side, 1.0 - (i // side + 0.5) / side)
    for v in tri:
        verts.append(v)
        uvs.append(uv)
tris = [(j, j + 1, j + 2) for j in range(0, len(uvs), 3)]
nsurf, nv, nt = write_md3(os.path.join(OUT, NAME + ".md3"), NAME, [verts], (tris, uvs), f"{MODEL_PATH}/{png}")
print(f"{NAME}: {nt} triangles, {nsurf} surfaces, {len(palette)} colours")
with open(os.path.join(OUT, "modeldef." + NAME + ".txt"), "w") as f:
    f.write("\n".join([f"// Generated by brutal-doom-3d-guns/tools/gz_left_hand.py. Do not edit by hand.",
                       "Model BDLeftHand", "{", f'   Path "{MODEL_PATH}"', f'   Model 0 "{NAME}.md3"', f'   Skin 0 "{png}"']
                      + [f'   SurfaceSkin 0 {i} "{png}"' for i in range(nsurf)]
                      + ["   Scale 1.0 1.0 1.0", "   AngleOffset 0", "   NOINTERPOLATION", "   USEACTORPITCH",
                         "   USEACTORROLL", "   FrameIndex BDLH A 0 0", "}"]) + "\n")
print(f"{NAME}: written to {OUT}")
