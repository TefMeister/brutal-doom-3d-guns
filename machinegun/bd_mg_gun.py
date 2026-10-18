# The Brutal Doom cube machine gun's shape, split into parts: {part: {(x, y, z): colour name}}. No Blender here.
# A mash of two pictures Tefa chose (2026-10-18), with dried blood all over it (bd_mg_settings.py says which part
# came from which).
# Parts: 'body' (never moves), 'mag', 'trigger', 'charge' (the charging handle - runs back on a reload).
import math
import random

from bd_mg_settings import (ROUND_SLACK, RECEIVER, RAIL, STOCK, STOCK_WINDOW, BUTT, GRIP, GUARD, TRIGGER, MAG,
                            MAG_STRAP, BOX_SIGHT, AMMO_WINDOW, CHARGE, HANDGUARD, SHROUD, SIDE_TUBE, FRONT_BLOCK,
                            BARREL, BRAKE, FRONT_SIGHT, BLOOD, BLOOD_SKIP)
from parts import Parts


def box(g, part, x0, x1, y, z0, z1, c, bevel=0):
    """A square bar along x, its four long edges cut back by `bevel` cubes (0 = sharp corners)."""
    for x in range(x0, x1 + 1):
        for yy in range(-y, y + 1):
            for z in range(z0, z1 + 1):
                if bevel and (y - abs(yy)) + min(z - z0, z1 - z) < bevel:
                    continue
                g.put(part, x, yy, z, c)


def recolour(g, x0, x1, y0, y1, z0, z1, c):
    """Repaint the cubes already there, adding none."""
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            for z in range(z0, z1 + 1):
                for part in g.p.values():
                    if (x, y, z) in part:
                        part[(x, y, z)] = c


def along(points, x):
    """The height of a line through `points` [(x, z)] at x."""
    for (x0, z0), (x1, z1) in zip(points, points[1:]):
        if x0 <= x <= x1:
            return round(z0 + (z1 - z0) * (x - x0) / max(1, x1 - x0))
    return points[-1][1]


def receiver(g):
    R = RECEIVER
    box(g, 'body', R['x0'], R['x1'], R['y'], R['z0'], R['z1'], 'metal', R['bevel'])
    for y in (-R['y'], R['y']):                                          # the narrower upper part
        g.cut(R['x0'], R['x1'], y, y, R['upper_z'], R['z1'])
    recolour(g, R['x0'], R['x1'], -R['y'], R['y'], R['z0'], R['upper_z'] - 1, 'panel')   # the grey lower band
    L = RAIL
    g.fill('body', L['x0'], L['x1'], -L['y'], L['y'], L['z0'], L['z1'], 'metal_mid')
    for x in range(L['x0'] + 1, L['x1'], L['slot_step']):
        g.cut(x, x + 1, -L['y'], L['y'], L['z1'], L['z1'])
    S = BOX_SIGHT                                                        # the box sight and its tunnel
    box(g, 'body', S['x0'], S['x1'], S['y'], S['z0'], S['z1'], 'metal', 1)
    g.cut(S['x0'], S['x1'], -S['tunnel_y'], S['tunnel_y'], S['tunnel_z'][0], S['tunnel_z'][1])
    recolour(g, S['x0'], S['x1'], -S['tunnel_y'] - 1, S['tunnel_y'] + 1, S['tunnel_z'][0] - 1,
             S['tunnel_z'][1] + 1, 'metal_dark')
    W = AMMO_WINDOW                                                      # right side: brass rounds behind a frame
    recolour(g, W['x0'] - 1, W['x1'] + 1, -R['y'], -R['y'], W['z0'] - 1, W['z1'] + 1, 'caution')
    g.cut(W['x0'], W['x1'], -R['y'], W['y_in'], W['z0'], W['z1'])
    recolour(g, W['x0'], W['x1'], W['y_in'] + 1, W['y_in'] + 1, W['z0'], W['z1'], 'port')
    for x in W['rounds']:
        g.fill('body', x, x + W['round_w'] - 1, W['y_in'], W['y_in'], W['round_z'][0], W['round_z'][1] - 1, 'brass')
        g.fill('body', x, x + W['round_w'] - 1, W['y_in'], W['y_in'], W['round_z'][1], W['round_z'][1], 'brass_hi')
    C = CHARGE
    g.fill('charge', C['x0'], C['x1'], C['y0'], C['y1'], C['z0'], C['z1'], 'metal_hi')


def stock(g):
    S, W = STOCK, STOCK_WINDOW
    for x in range(S['x0'], S['x1'] + 1):
        bottom = along(S['bottom'], x)
        for y in range(-S['y'], S['y'] + 1):
            for z in range(bottom, S['top'] + 1):
                if (S['y'] - abs(y)) + min(z - bottom, S['top'] - z) < S['bevel']:
                    continue
                g.put('body', x, y, z, 'panel' if abs(y) == S['y'] and W['z1'] < z < S['top'] - 1 else 'metal')
    g.cut(W['x0'], W['x1'], -S['y'], S['y'], W['z0'], W['z1'])          # the skeleton window
    for zc in W['rods']:                                                 # two rods across it
        g.tube('body', W['x0'], W['x1'], zc, W['rod_r'], 'metal_hi')
    B = BUTT
    for z in range(along(S['bottom'], S['x0']) - 1, S['top'] + 1):
        g.fill('body', S['x0'] - B['x1'] - 1, S['x0'] - 1, -B['y'], B['y'], z, z, 'rubber')


def grip_front(z):
    return round(GRIP['front'] - (GRIP['z1'] - z) * GRIP['rake'])


def grip_back(z):
    return round(GRIP['back'] - (GRIP['z1'] - z) * GRIP['rake'])


def grip(g):
    G = GRIP
    for z in range(G['z0'], G['z1'] + 1):
        f, b = grip_front(z), grip_back(z)
        for x in range(b, f + 1):
            for y in range(-G['y'], G['y'] + 1):
                if x in (b, f) and abs(y) == G['y']:
                    continue
                ridge = (abs(y) == G['y'] and b + G['ridge_inset'] <= x <= f - G['ridge_inset']
                         and z % G['ridge_step'] == 0)
                g.put('body', x, y, z, 'grip_ridge' if ridge else 'grip')
    U = GUARD
    front = grip_front(U['z_bottom'] + 1)
    g.fill('body', front, U['x1'], -U['y'], U['y'], U['z_bottom'], U['z_bottom'] + 1, 'metal')
    for z in range(U['z_bottom'], RECEIVER['z0']):
        x = U['x1'] - round((RECEIVER['z0'] - 1 - z) * U['lean'] / (RECEIVER['z0'] - 1 - U['z_bottom']))
        g.fill('body', x - 1, x, -U['y'], U['y'], z, z, 'metal')
    for x, z in TRIGGER:
        g.fill('trigger', x, x, -1, 1, z, z, 'metal_hi')


def mag(g):
    M, S = MAG, MAG_STRAP
    for z in range(M['z0'], M['z1'] + 1):
        lean = round((z - M['z0']) * M['lean'] / (M['z1'] - M['z0']))   # the box leans back at the bottom
        for x in range(M['x0'] - M['lean'] + lean, M['x1'] - M['lean'] + lean + 1):
            for y in range(-M['y'], M['y'] + 1):
                if (M['y'] - abs(y)) + min(z - M['z0'], M['z1'] - z) < M['bevel']:
                    continue
                g.put('mag', x, y, z, 'metal')
    for sign in (-1, 1):                                                 # the carry strap, a raised loop
        y = sign * S['y']
        g.fill('mag', S['x0'], S['x1'], y, y, S['z0'], S['z0'] + 1, 'panel')
        g.fill('mag', S['x0'], S['x1'], y, y, S['z1'] - 1, S['z1'], 'panel')
        g.fill('mag', S['x0'], S['x0'] + 1, y, y, S['z0'], S['z1'], 'panel')
        g.fill('mag', S['x1'] - 1, S['x1'], y, y, S['z0'], S['z1'], 'panel')


def front(g):
    H = HANDGUARD
    box(g, 'body', H['x0'], H['x1'], H['y'], H['z0'], H['z1'], 'panel', H['bevel'])
    for x in H['slots']:
        g.cut(x, x + H['slot_len'] - 1, -H['y'], -H['y'] + 1, H['slot_z'][0], H['slot_z'][1])
        g.cut(x, x + H['slot_len'] - 1, H['y'] - 1, H['y'], H['slot_z'][0], H['slot_z'][1])
        for y in (-H['y'] + 2, H['y'] - 2):
            recolour(g, x, x + H['slot_len'] - 1, y, y, H['slot_z'][0], H['slot_z'][1], 'port')
    S = SHROUD
    box(g, 'body', S['x0'], S['x1'], S['y'], S['z0'], S['z1'], 'metal', S['bevel'])
    for x in S['top_slots']:
        g.cut(x, x + S['top_slot_len'] - 1, -S['top_slot_y'], S['top_slot_y'], S['z1'] - 1, S['z1'])
        recolour(g, x, x + S['top_slot_len'] - 1, -S['top_slot_y'], S['top_slot_y'], S['z1'] - 2, S['z1'] - 2,
                 'port')
    T = SIDE_TUBE
    for sign in (-1, 1):
        g.tube('body', T['x0'], T['x1'], T['zc'], T['r'], 'metal_hi', yc=sign * T['y'])
    F = FRONT_BLOCK
    for z in range(F['z0'], F['z1'] + 1):
        lean = round((F['z1'] - z) * F['lean'] / (F['z1'] - F['z0']))    # its underside tucks back
        for x in range(F['x0'] + lean, F['x1'] + 1):
            for y in range(-F['y'], F['y'] + 1):
                if (F['y'] - abs(y)) + min(z - F['z0'], F['z1'] - z) < F['bevel']:
                    continue
                g.put('body', x, y, z, 'panel')
    for x in F['slashes']:                                               # the red gun's three slots, slanted
        for z in range(F['slash_z'][0], F['slash_z'][1] + 1):
            xs = x + (z - F['slash_z'][0]) // 2
            g.cut(xs, xs + 1, -F['y'], -F['y'], z, z)
            g.cut(xs, xs + 1, F['y'], F['y'], z, z)
    B = BARREL
    g.tube('body', F['x1'] + 1, B['x1'], B['zc'], B['r'], 'metal_hi')
    K = BRAKE                                                            # the slotted muzzle brake
    box(g, 'body', K['x0'], K['x1'], K['y'], K['z0'], K['z1'], 'metal', K['bevel'])
    for x0, x1 in K['slots']:
        g.cut(x0, x1, -K['y'], K['y'], K['slot_z'][0], K['slot_z'][1])
    ri = math.ceil(K['bore']) + 1
    for y in range(-ri, ri + 1):
        for z in range(math.floor(B['zc'] - ri), math.ceil(B['zc'] + ri) + 1):
            if y * y + (z - B['zc']) ** 2 <= K['bore'] ** 2 + ROUND_SLACK:
                g.cut(K['x0'], K['x1'], y, y, z, z)
                g.put('body', K['x0'] - 1, y, z, 'bore')
    P = FRONT_SIGHT                                                      # the post, between protective ears
    g.fill('body', P['x0'], P['x1'], -P['y'], P['y'], F['z1'] + 1, P['z1'], 'metal')
    g.put('body', P['x0'], 0, P['z1'], 'sight_dot')
    for sign in (-1, 1):
        g.fill('body', P['ears_x'][0], P['ears_x'][1], sign * P['ears_y'], sign * P['ears_y'], F['z1'] + 1,
               P['ears_z1'], 'metal')


def blood(g):
    """Dried blood all over: blotches with darker rims on the sides and tops, runs dripping down, and spatter.
    Each stain is recorded in g.stains for the fine pass's spatter: (side, x, z, r) - side +1/-1 for the left or
    right face, 0 for a top."""
    B = BLOOD
    rng = random.Random(B['seed'])
    owner = {}
    for name, cells in g.p.items():
        for c in cells:
            owner[c] = name
    outer = {1: {}, -1: {}}                                              # (x, z) -> the outermost y on each side
    top = {}                                                             # (x, y) -> the highest z
    for (x, y, z) in owner:
        for s in (1, -1):
            if (x, z) not in outer[s] or s * y > s * outer[s][(x, z)]:
                outer[s][(x, z)] = y
        if (x, y) not in top or z > top[(x, y)]:
            top[(x, y)] = z

    def paint(cell, colour):
        name = owner.get(cell)
        if name and g.p[name][cell] not in BLOOD_SKIP:
            g.p[name][cell] = colour

    def blot(r, u, v, cell_at, stretch=1.0):
        """One blotch centred on (u, v) in the face's own two directions; returns its lowest v at each u."""
        w1, w2 = rng.uniform(-1, 1) * B['wobble'][0], rng.uniform(-1, 1) * B['wobble'][1]
        p1, p2 = rng.uniform(0, 2 * math.pi), rng.uniform(0, 2 * math.pi)
        lowest = {}
        reach = int(math.ceil(r * (1 + abs(w1) + abs(w2)) * stretch)) + 1
        for i in range(-reach, reach + 1):
            for j in range(-reach, reach + 1):
                a = math.atan2(j, i / stretch)
                edge = r * (1 + w1 * math.sin(3 * a + p1) + w2 * math.sin(5 * a + p2))
                d = math.hypot(i / stretch, j)
                if d > edge:
                    continue
                cell = cell_at(u + i, v + j)
                if cell is None:
                    continue
                paint(cell, 'blood_dark' if d > edge * B['rim'] else rng.choice(('blood', 'blood', 'blood_mid')))
                lowest[u + i] = min(lowest.get(u + i, v + j), v + j)
        return lowest

    g.stains = []
    side_cols = {s: list(outer[s]) for s in (1, -1)}
    for _ in range(B['side_stains']):
        s = rng.choice((1, -1))
        x, z = rng.choice(side_cols[s])
        r = rng.uniform(*B['radius'])

        def on_side(xx, zz, s=s):
            y = outer[s].get((xx, zz))
            return None if y is None else (xx, y, zz)
        lowest = blot(r, x, z, on_side, stretch=rng.uniform(1.0, 1.8))
        g.stains.append((s, x, z, r))
        if rng.random() < B['drip_share'] and lowest:                   # runs dripping down the face
            for _ in range(rng.randint(*B['drips'])):
                dx = rng.choice(list(lowest))
                zz = lowest[dx] - 1
                y0 = outer[s].get((dx, zz + 1))
                for k in range(rng.randint(*B['drip_len'])):
                    y = outer[s].get((dx, zz - k))
                    if y is None or y0 is None or abs(y - y0) > 1:
                        break
                    paint((dx, y, zz - k), 'blood_mid')
                    y0 = y
                else:
                    paint((dx, y0, zz - k), 'blood_dark')                # a dried bead at its end
    top_cols = list(top)
    for _ in range(B['top_stains']):
        x, y = rng.choice(top_cols)
        r = rng.uniform(*B['radius'])

        def on_top(xx, yy):
            z = top.get((xx, yy))
            return None if z is None else (xx, yy, z)
        blot(r, x, y, on_top, stretch=rng.uniform(1.0, 2.0))
        g.stains.append((0, x, y, r))


def build():
    g = Parts()
    stock(g)
    receiver(g)
    grip(g)
    mag(g)
    front(g)
    blood(g)
    return g
