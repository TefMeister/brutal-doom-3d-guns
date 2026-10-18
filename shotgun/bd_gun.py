# The Brutal Doom cube shotgun's shape, split into parts: {part: {(x, y, z): colour name}}. No Blender here.
# Built one part at a time with Tefa (2026-10-18 on): the stock first, then the metal; the metal then remodelled on the
# DOOM (2016) combat shotgun, round the same dark oak stock and pump.
# Tefa then had the stock taken off (2026-10-18): a dark oak pistol grip and the picture's short metal rear instead.
# Parts: 'body' (grip, receiver, barrel, magazine - never moves), 'pump' (fore-end and action bars - slides back to
# pump), 'trigger'.
import math

from bd_settings import (ROUND_SLACK, GRIP, GRAIN_STEP, GRAIN_WAVE, REAR_STUB, RECEIVER, REAR_STEP, NOSE_CHAMFER, SIDE_PLATE, SPINE, REAR_SIGHT, TOP_BLOCK, PORT, SHELL,
                         LOADING_PORT, TRIGGER_PLATE, LOWER_BLOCK, GUARD, TRIGGER, BARREL, BARREL_SHINE, BARREL_RING,
                         JACKET, RODS, HOUSING, MAGTUBE, PUMP, ACTION_BARS, FRONT_MODULE, SHROUD, SHROUD_LOW, SHROUD_PANEL,
                         MUZZLE, MAG_MUZZLE, FRONT_SIGHT)
from parts import Parts


def along(points, x):
    """The edge's height at x, on the straight line between the two points either side of it."""
    for (x0, z0), (x1, z1) in zip(points, points[1:]):
        if x0 <= x <= x1:
            return z0 + (z1 - z0) * (x - x0) / (x1 - x0) if x1 != x0 else z0
    return points[-1][1]


def grip(g):
    """Dark oak pistol grip, raked back, rounded long edges, a metal base plate."""
    G = GRIP
    for z in range(G['z0'], G['z1'] + 1):
        shift = round((G['z1'] - z) * G['rake'])
        f, b = G['front'] - shift, G['back'] - shift
        for x in range(b, f + 1):
            for y in range(-G['y'], G['y'] + 1):
                if x in (b, f) and abs(y) == G['y']:
                    continue                                   # rounded long edges
                if z < G['z0'] + G['cap']:
                    g.put('body', x, y, z, 'metal')
                    continue
                wave = GRAIN_WAVE[0] * math.sin(x / GRAIN_WAVE[1])
                c = 'wood'
                if x == f and abs(y) < G['y']:
                    c = 'wood_hi'                              # the front edge, worn by the fingers
                elif round(z + wave) % GRAIN_STEP == 0:
                    c = 'wood_grain'
                elif x == b:
                    c = 'wood_dark'
                g.put('body', x, y, z, c)


def rear_stub(g):
    """The short metal end behind the grip, its bottom dropping to a tall end plate."""
    S = REAR_STUB
    for x in range(S['x0'], S['x1'] + 1):
        top, bot = round(along(S['top'], x)), round(along(S['bottom'], x))
        c = 'metal_dark' if x < S['x0'] + S['plate'] else 'metal'
        box(g, 'body', x, x, S['y'], bot, top, c, 1)


def box(g, part, x0, x1, y, z0, z1, c, bevel=0):
    """A square bar along x, its four long edges cut back by `bevel` cubes (0 = sharp corners)."""
    for x in range(x0, x1 + 1):
        for yy in range(-y, y + 1):
            for z in range(z0, z1 + 1):
                if bevel and (y - abs(yy)) + min(z - z0, z1 - z) < bevel:
                    continue
                g.put(part, x, yy, z, c)


def hole(g, x0, x1, zc, r):
    """A round hole along x from x0 to x1, its far wall (x0 - 1) dark: a bore."""
    ri = math.ceil(r)
    for y in range(-ri, ri + 1):
        for z in range(math.floor(zc - r), math.ceil(zc + r) + 1):
            if y * y + (z - zc) ** 2 <= r * r + ROUND_SLACK:
                g.cut(x0, x1, y, y, z, z)
                if g.owned((x0 - 1, y, z)):
                    g.put('body', x0 - 1, y, z, 'bore')


def recolour(g, x0, x1, y0, y1, z0, z1, c):
    """Repaint the cubes already there, adding none."""
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            for z in range(z0, z1 + 1):
                for part in g.p.values():
                    if (x, y, z) in part:
                        part[(x, y, z)] = c


def receiver(g):
    R = RECEIVER
    box(g, 'body', R['x0'], R['x1'], R['y'], R['z0'], R['z1'], 'metal', R['bevel'])
    S = REAR_STEP                                                      # rear end down to the stock's wrist
    g.cut(R['x0'], S['x1'], -R['y'], R['y'], S['z1'] + 1, R['z1'])
    g.cut(R['x0'], S['x1'], -R['y'], R['y'], R['z0'], S['z0'] - 1)
    N = NOSE_CHAMFER                                                   # the underside rising towards the front
    for x in range(N['x0'], R['x1'] + 1):
        g.cut(x, x, -R['y'], R['y'], R['z0'], R['z0'] + (x - N['x0']) // N['rise'])
    P = SIDE_PLATE                                                     # the armour plates, both sides
    for z in range(P['z0'], P['z1'] + 1):
        lean = round((z - P['z0']) * P['slant'] / (P['z1'] - P['z0']))
        for yy in (-P['y'], P['y']):
            g.fill('body', P['x0'] + lean, P['x1'] - lean, yy, yy, z, z, 'metal_mid')
    S = SPINE
    g.fill('body', S['x0'], S['x1'], -S['y'], S['y'], S['z0'], S['z1'], 'metal')
    for x in range(S['x0'], S['x1'] + 1, S['notch_step']):
        g.cut(x, x, -S['y'], S['y'], S['z1'], S['z1'])
    V = REAR_SIGHT
    g.fill('body', V['x0'], V['x1'], -V['y'], V['y'], V['z0'], V['z1'], 'metal')
    g.cut(V['x0'], V['x1'], -V['hole_y'], V['hole_y'], V['hole_z'][0], V['hole_z'][1])
    T = TOP_BLOCK
    box(g, 'body', T['x0'], T['x1'], T['y'], T['z0'], T['z1'], 'metal_mid', 1)
    P = PORT                                                           # ejection port, right side only
    g.cut(P['x0'], P['x1'], -SIDE_PLATE['y'], P['y_in'], P['z0'], P['z1'])
    recolour(g, P['x0'], P['x1'], P['y_in'] + 1, P['y_in'] + 1, P['z0'], P['z1'], 'port')     # back wall
    recolour(g, P['x0'], P['x1'], -R['y'], P['y_in'], P['z0'] - 1, P['z0'] - 1, 'port')       # floor
    recolour(g, P['x0'], P['x1'], -R['y'], P['y_in'], P['z1'] + 1, P['z1'] + 1, 'port')       # roof
    recolour(g, P['x0'] - 1, P['x0'] - 1, -R['y'], P['y_in'], P['z0'], P['z1'], 'metal_hi')   # the bolt's face
    H = SHELL                                                          # a shell on its way out
    g.tube('body', H['x0'] + H['head'], H['x1'], H['zc'], H['r'], 'shell', yc=H['y'])
    g.tube('body', H['x0'], H['x0'] + H['head'] - 1, H['zc'], H['r'] + H['rim'], 'shell_brass', yc=H['y'])
    L = LOADING_PORT
    g.cut(L['x0'], L['x1'], -L['y'], L['y'], R['z0'], R['z0'] + L['depth'] - 1)
    recolour(g, L['x0'], L['x1'], -L['y'], L['y'], R['z0'] + L['depth'], R['z0'] + L['depth'], 'port')
    T = TRIGGER_PLATE
    box(g, 'body', T['x0'], T['x1'], T['y'], T['z0'], T['z1'], 'metal', 1)
    B = LOWER_BLOCK                                                    # angular block ahead of the guard
    for z in range(B['z0'], B['z1'] + 1):
        back = round((B['z1'] - z) * B['lean'] / max(1, B['z1'] - B['z0']))
        g.fill('body', B['x0'] + back, B['x1'] - back, -B['y'], B['y'], z, z, 'metal_mid')


def guard(g):
    G = GUARD
    top = TRIGGER_PLATE['z0'] - 1
    g.fill('body', G['x0'], G['x1'] - G['lean'], -G['y'], G['y'], G['z_bottom'], G['z_bottom'] + 1, 'metal')
    g.fill('body', G['x0'], G['x0'] + 1, -G['y'], G['y'], G['z_bottom'], top, 'metal')
    for z in range(G['z_bottom'], top + 1):                            # the front, leaning back going down
        x = G['x1'] - round((top - z) * G['lean'] / (top - G['z_bottom']))
        g.fill('body', x - 1, x, -G['y'], G['y'], z, z, 'metal')
    for x, z in TRIGGER:
        g.fill('trigger', x, x, -1, 1, z, z, 'metal_hi')


def jacket(g):
    """The thick hollow jacket round the bare barrel: solid ends, a dark inside, machined windows and top slots."""
    J, zc = JACKET, BARREL['zc']
    inner = J['r'] - J['wall']
    for x in range(J['x0'], J['x1'] + 1):
        end = min(x - J['x0'], J['x1'] - x)
        r = J['r'] - (1 if end == 0 else 0)                            # the ends chamfered by one cube
        solid = end < J['cap']
        for y in range(-r, r + 1):
            for z in range(math.floor(zc - r), math.ceil(zc + r) + 1):
                d2 = y * y + (z - zc) ** 2
                if d2 > r * r + ROUND_SLACK or (not solid and d2 < inner * inner):
                    continue
                g.put('body', x, y, z, 'port' if not solid and d2 < (inner + 1) ** 2 else 'polish')
    for y in range(-BARREL_SHINE, BARREL_SHINE + 1):                   # the shine along its top
        z = math.floor(zc + math.sqrt(J['r'] ** 2 + ROUND_SLACK - y * y))
        recolour(g, J['x0'] + 1, J['x1'] - 1, y, y, z, z, 'polish_hi')
    W, T = J['windows'], J['top_slot']
    for wx in W['x']:
        g.cut(wx, wx + W['length'] - 1, W['y_from'], J['r'] + 1, W['z0'], W['z1'])
        g.cut(wx, wx + W['length'] - 1, -J['r'] - 1, -W['y_from'], W['z0'], W['z1'])
        cx = wx + W['length'] // 2
        g.cut(cx - T['length'] // 2, cx + T['length'] // 2, -T['y'], T['y'], T['z_from'], zc + J['r'] + 1)


def barrel(g):
    B, K = BARREL, BARREL_RING
    jacket(g)
    g.tube('body', B['x0'], B['x1'], B['zc'], B['r'], 'polish')
    J = JACKET                                                         # inside the jacket the barrel is in shadow, so
    g.tube('body', J['x0'] + J['cap'], J['x1'] - J['cap'], B['zc'], B['r'], 'metal_dark')   # the windows read as holes
    g.tube('body', K['x0'], K['x1'], B['zc'], K['r'], 'brass')
    D = RODS
    for yy in (-D['y'], D['y']):
        g.fill('body', D['x0'], D['x1'], yy, yy, D['z'], D['z'], 'polish')
    T = MAGTUBE
    g.tube('body', T['x0'], T['x1'], T['zc'], T['r'], 'metal')
    H = HOUSING
    box(g, 'body', H['x0'], H['x1'], H['y'], H['z0'], H['z1'], 'metal', 1)
    for x in range(H['x0'] + H['holes'] // 2, H['x1'], H['holes']):
        for sign in (-1, 1):
            g.put('body', x, sign * H['y'], H['hole_z'], 'metal_dark')
    M = FRONT_MODULE
    box(g, 'body', M['x0'], M['x1'], M['y'], M['z0'], M['z1'], 'metal_mid', 1)
    for x in M['slots']:
        for sign in (-1, 1):
            g.cut(x, x, sign * M['y'], sign * M['y'], M['slot_z'][0], M['slot_z'][1])
            floor = sign * (M['y'] - 1)
            recolour(g, x, x, floor, floor, M['slot_z'][0], M['slot_z'][1], 'metal_dark')


def shroud(g):
    U, L = SHROUD, SHROUD_LOW
    box(g, 'body', U['x0'], U['x1'], U['y'], U['z0'], U['z1'], 'metal', U['bevel'])
    box(g, 'body', L['x0'], L['x1'], L['y'], L['z0'], L['z1'], 'metal', L['bevel'])
    P = SHROUD_PANEL
    for yy in (-U['y'], U['y']):
        g.cut(P['x0'], P['x1'], yy, yy, P['z0'], P['z1'])
    M, B = MUZZLE, BARREL
    g.tube('body', M['x0'], M['x1'], B['zc'], M['r'], 'metal_hi')
    hole(g, U['x1'] - 3, M['x1'], B['zc'], M['bore'])
    M, T = MAG_MUZZLE, MAGTUBE
    g.tube('body', M['x0'], M['x1'], T['zc'], M['r'], 'metal_hi')
    hole(g, L['x1'] - 3, M['x1'], T['zc'], M['bore'])
    F = FRONT_SIGHT
    g.fill('body', F['x0'], F['x1'], 0, 0, U['z1'] + 1, F['z1'], 'sight')
    for yy in (-F['ears'], F['ears']):
        g.fill('body', F['x0'], F['x1'], yy, yy, U['z1'] + 1, F['z0'] + 1, 'metal')


def pump(g):
    """Dark oak, boxed round the magazine tube, a rounded front-bottom corner, a recessed panel on each side."""
    P, I = PUMP, PUMP['inset']
    r = P['round_r']
    for x in range(P['x0'], P['x1'] + 1):
        end = min(x - P['x0'], P['x1'] - x)
        bev = max(0, P['end_bevel'] - end)
        for y in range(-P['y'] + bev, P['y'] - bev + 1):
            for z in range(P['z0'] + bev, P['z1'] - bev + 1):
                corner_x, corner_z = x - (P['x1'] - r), (P['z0'] + r) - z
                if corner_x > 0 and corner_z > 0 and corner_x ** 2 + corner_z ** 2 > r * r:
                    continue                                                 # rounded front-bottom corner
                if abs(y) == P['y'] and I['x0'] <= x <= I['x1'] and I['z0'] <= z <= I['z1']:
                    continue                                                 # the recessed side panel
                if g.owned((x, y, z)):
                    continue                                                 # the tube and rails run through it
                c = 'wood'
                if z == P['z1'] - bev:
                    c = 'wood_hi'
                elif z <= P['z0'] + bev + 1:
                    c = 'wood_dark'
                elif z % 3 == 0:
                    c = 'wood_grain'
                g.put('pump', x, y, z, c)
    A = ACTION_BARS
    for yy in (-A['y'], A['y']):
        g.fill('pump', A['x0'], P['x0'] - 1, yy, yy, A['z'], A['z'], 'metal_hi')


def build():
    g = Parts()
    rear_stub(g)
    receiver(g)
    grip(g)
    guard(g)
    barrel(g)
    shroud(g)
    pump(g)
    return g
