# Where Doomguy's gloves go on a gun, worked out from the gun's own cubes (2026-10-19). No Blender here.
#
# Tefa, 2026-10-19: "can you do gloves on all the other weapons now?", done alone as a first pass and looked at together
# afterwards. The rule comes from the three guns whose gloves were fitted with Tefa (shotgun, pistol, machine gun):
#   right glove: shift = (the grip's front x at its top - 17, 0, the grip's top z - 2), leaning with the grip
#                (shotgun front 13 / top -7 -> (-4, 0, -9); pistol 20 / 28 -> (3, 0, 26); machine gun 78 / -1 -> (61, 0, -3))
#   left glove:  palm up under the gun at the support point: x0 + shift = that point (LEFT_POSE x0 is 116), the palm's
#                face one cube under the gun's bottom there, the knuckle line 10 cubes out from the gun's half width
#                (shotgun pump 9 -> 19, machine gun 6 -> 16), the wrist dropping past half width + 1.
# Gun space: x rear -> muzzle, y + = the gun's LEFT, z up; the pivot is the top of the pistol grip.
from bd_glove_settings import PALM_T

ONE_HANDED = {"revolver", "hand_grenade"}      # the right glove only
FORE_REACH = 120                                # cubes from the grip to the left hand (shotgun 129, machine gun 119)


def _front_at(cells, px, z):
    """The grip's front at height z: walking forward from the pivot's x through touching cubes near the middle."""
    if not any((px, y, z) in cells for y in range(-3, 4)):
        return None
    x = px
    while any((x + 1, y, z) in cells for y in range(-3, 4)):
        x += 1
    return x


def _grip_x(cells, px, reach=24):
    """The middle of the upright grip nearest px: a run of x columns hanging 10+ cubes below z -2 near the middle."""
    deep = {}
    for x, y, z in cells:
        if abs(y) <= 4 and z <= -2 and abs(x - px) <= reach:
            deep.setdefault(x, set()).add(z)
    cols = sorted(x for x in deep if len(deep[x]) >= 10)
    if not cols:
        return None
    runs, cur = [], [cols[0]]
    for x in cols[1:]:
        if x == cur[-1] + 1:
            cur.append(x)
        else:
            runs.append(cur)
            cur = [x]
    runs.append(cur)
    best = min(runs, key=lambda r: min(abs(x - px) for x in r))
    return (best[0] + best[-1]) // 2


def grip(cells, pivot):
    """(front x at the top, top z, rake) of the pistol grip under (or nearest) the pivot, or None if there is none."""
    px = int(round(pivot[0]))
    if not any((px, y, z) in cells for y in range(-3, 4) for z in range(int(round(pivot[2])) - 16, int(round(pivot[2])) - 12)):
        px = _grip_x(cells, px) or px
    z1 = int(round(pivot[2])) - 1
    while z1 > pivot[2] - 6 and not any((px, y, z1) in cells for y in range(-3, 4)):
        z1 -= 1
    lo, hi = _front_at(cells, px, z1 - 9), _front_at(cells, px, z1 - 17)
    if lo is None:
        return None
    rake = max(0.0, min(0.6, (lo - hi) / 8.0)) if hi is not None else 0.3
    return lo + round(9 * rake), z1, rake


def foregrip(cells, front):
    """An upright front grip ahead of the pistol grip (body cubes hanging 10+ below the body's bottom), as
    (front x at its top, top z, rake) like grip(), or None. The left hand then holds it like the right hand holds
    the pistol grip, mirrored (forge_gloves_run.py)."""
    x_end = max(c[0] for c in cells)
    deep = {}
    for x, y, z in cells:
        if abs(y) <= 4 and z <= -8 and front + 15 < x < x_end - 10:
            deep.setdefault(x, set()).add(z)
    run = [x for x in sorted(deep) if len(deep[x]) >= 10]
    if not run:
        return None
    best, cur = [], [run[0]]
    for x in run[1:]:
        cur = cur + [x] if x == cur[-1] + 1 else [x]
        best = cur if len(cur) > len(best) else best
    best = best or cur
    return grip(cells, ((best[0] + best[-1]) / 2.0, 0, 0))


def support(cells, front, fore_reach=FORE_REACH):
    """(x, bottom z, half width) under the gun where the left hand holds it, or None for a short gun."""
    xs = [c[0] for c in cells]
    x_end = max(xs)
    x = min(front + fore_reach, front + round(0.55 * (x_end - front)), x_end - 12)   # mid fore-end, not the muzzle
    if x < front + 40:
        return None
    near = [c for c in cells if abs(c[0] - x) <= 6]
    # the barrel / handguard body near the middle line: ignore what hangs far below (magazines, bipods)
    zs = sorted(c[2] for c in near if abs(c[1]) <= 12)
    if not zs:
        return None
    bottom = zs[len(zs) // 10]                     # the lowest tenth is often a hanging part
    half = max(abs(c[1]) for c in near if c[2] <= bottom + 6)
    return x, bottom, half


def poses(name, cells, pivot):
    """(right overrides, left overrides or None, sides, what was found). `cells` are the body's cubes only (no
    magazines). The left overrides carry upright=True when the left hand holds an upright front grip: they are then a
    RIGHT-hand pose (shift, rake) to be mirrored, not a palm-up one."""
    g = grip(cells, pivot)
    if g is None:
        front, top, rake = int(round(pivot[0])) + 7, int(round(pivot[2])) - 1, 0.3
        found = "no grip found under the pivot: placed as if one sat there"
    else:
        front, top, rake = g
        found = f"grip front {front} top {top} rake {rake:.2f}"
    right = dict(shift=(front - 17, 0, top - 2), rake=rake)
    if name in ONE_HANDED:
        return right, None, ('right',), found + "; one-handed"
    fg = foregrip(cells, front)
    if fg is not None:
        f2, t2, r2 = fg
        return (right, dict(shift=(f2 - 17, 0, t2 - 2), rake=r2, upright=True), ('right', 'left'),
                found + f"; left hand on the upright front grip, front {f2} top {t2}")
    s = support(cells, front)
    if s is None:
        return right, None, ('right',), found + "; too short for a second hand"
    x, bottom, half = s
    left = dict(shift=(x - 116, 0, 0), z0=bottom - 1 - PALM_T // 2, y0=half + 10, left_edge=half + 1)
    return right, left, ('right', 'left'), found + f"; left hand at x {x}, under z {bottom}, half width {half}"
