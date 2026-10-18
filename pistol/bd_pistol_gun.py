# The Brutal Doom cube pistol's shape, split into parts: {part: {(x, y, z): colour name}}. No Blender here.
# The DOOM (2016) pistol's shape (Tefa, 2026-10-18), without its glow and without a hammer, then made a hand cannon
# with a compensator and silver grip plates.
# Parts: 'frame' (frame, grip, guard, ring module, tang - never moves), 'slide' (slide and sights - runs back on a
# shot), 'barrel', 'trigger', 'mag', 'cover' (the ejection port's cover - swings open on its hinge).
import math

from bd_pistol_settings import (ROUND_SLACK, GRIP, GRIP_TEXTURE, GRIP_PLATE, MAG_BASE, TANG, FRAME, GUARD, TRIGGER,
                                MODULE, RING, RAIL, SLIDE, DECK, REAR_SLOPE, DIAMONDS, PORT, CASE, COVER, SERRATIONS,
                                REAR_SIGHT, FRONT_SIGHT, BARREL, COMP, MUZZLE)
from parts import Parts


def bulge(z, size):
    """How far the grip bulges at height z: nothing at the ends, `size` cubes in the middle."""
    t = (z - GRIP['z0']) / float(GRIP['z1'] - GRIP['z0'])
    return round(size * math.sin(math.pi * t))


def grip_front(z):
    return round(GRIP['front'] - (GRIP['z1'] - z) * GRIP['rake']) + bulge(z, GRIP['belly'])


def grip_back(z):
    return round(GRIP['back'] - (GRIP['z1'] - z) * GRIP['rake']) - bulge(z, GRIP['swell'])


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


def grip(g):
    G, T = GRIP, GRIP_TEXTURE
    for z in range(G['z0'], G['z1'] + 1):
        f, b = grip_front(z), grip_back(z)
        for x in range(b, f + 1):
            for y in range(-G['y'], G['y'] + 1):
                if x in (b, f) and abs(y) == G['y']:
                    continue                                             # rounded corners
                c = 'grip'
                if abs(y) == G['y'] and b + T['inset'] <= x <= f - T['inset'] and T['z0'] <= z <= T['z1']:
                    c = 'grip_check' if (x // 1 + z) % 2 == 0 and z % 2 == 0 else 'grip'   # stippled rubber
                g.put('frame', x, y, z, c)
    P = GRIP_PLATE                                                       # a silver plate on each side
    for z in range(P['z0'], P['z1'] + 1):
        x0, x1 = grip_back(z) + P['inset'], grip_front(z) - P['inset']
        for x in range(x0, x1 + 1):
            cx, cz = min(x - x0, x1 - x), min(z - P['z0'], P['z1'] - z)
            if cx + cz < P['corner']:
                continue                                                 # cut corners
            edge = cx + cz == P['corner'] or cx == 0 or cz == 0
            for sign in (-1, 1):
                g.put('frame', x, sign * (G['y'] + 1), z, 'silver_dark' if edge else 'silver')
    M = MAG_BASE                                                         # flared base plate
    for z in range(M['z0'], M['z1'] + 1):
        g.fill('mag', grip_back(G['z0']) - M['over'], grip_front(G['z0']) + M['over'], -M['y'], M['y'], z, z,
               'metal_dark' if z < M['z1'] else 'metal')
    T = TANG                                                             # the tang over the web of the hand
    for x in range(T['x0'], grip_back(G['z1']) + 1):
        droop = round((grip_back(G['z1']) - x) * T['droop'])
        g.fill('frame', x, x, -T['y'], T['y'], T['z0'] - droop, T['z1'] - droop, 'metal')


def frame(g):
    F = FRAME
    box(g, 'frame', F['x0'], F['x1'], F['y'], F['z0'], F['z1'], 'metal', 1)
    G = GUARD
    top = F['z0'] - 1
    front = grip_front(G['z_bottom'] + 1)
    g.fill('frame', front, G['x1'], -G['y'], G['y'], G['z_bottom'], G['z_bottom'] + 1, 'metal')     # bottom bar
    for z in range(G['z_bottom'], top + 1):                                                         # front post
        x = G['x1'] - round((top - z) * G['lean'] / (top - G['z_bottom']))
        g.fill('frame', x - 1, x, -G['y'], G['y'], z, z, 'metal')
    for x, z in TRIGGER:
        g.fill('trigger', x, x, -1, 1, z, z, 'metal_hi')
    M = MODULE                                                           # the box under the front
    for z in range(M['z0'], M['z1'] + 1):
        back = round((M['z1'] - z) * M['lean'] / max(1, M['z1'] - M['z0']))
        for x in range(M['x0'], M['x1'] - back + 1):
            for y in range(-M['y'], M['y'] + 1):
                if (M['y'] - abs(y)) + min(z - M['z0'], x - M['x0']) < M['bevel']:
                    continue
                g.put('frame', x, y, z, 'metal')
    R = RING                                                             # the coil on each side, plain metal
    for x in range(math.floor(R['x'] - R['r_out']), math.ceil(R['x'] + R['r_out']) + 1):
        for z in range(math.floor(R['z'] - R['r_out']), math.ceil(R['z'] + R['r_out']) + 1):
            d2 = (x - R['x']) ** 2 + (z - R['z']) ** 2
            for sign in (-1, 1):
                if d2 <= R['r_out'] ** 2 and d2 >= R['r_in'] ** 2:
                    g.put('frame', x, sign * R['y'], z, 'metal_hi')
                elif d2 < R['r_in'] ** 2:
                    g.cut(x, x, sign * M['y'], sign * M['y'], z, z)
                    g.put('frame', x, sign * (M['y'] - 1), z, 'port')     # dark inside: where it glowed
    L = RAIL
    for x in L['slots']:
        g.cut(x, x + 1, -2, 2, L['z'], L['z'])


def slide(g):
    S, D = SLIDE, DECK
    box(g, 'slide', S['x0'], S['x1'], S['y'], S['z0'], S['z1'], 'metal', S['bevel'])
    for y in (-S['y'], S['y']):                                          # the narrower upper deck
        g.cut(S['x0'], D['x1'], y, y, D['z0'], S['z1'])
    recolour(g, S['x0'], D['x1'], -D['y'], D['y'], D['z0'], S['z1'], 'metal_mid')
    R = REAR_SLOPE                                                       # the back end sloping down
    for x in range(S['x0'], R['x1'] + 1):
        drop = round((R['x1'] - x) * R['drop'] / max(1, R['x1'] - S['x0']))
        if drop:
            g.cut(x, x, -S['y'], S['y'], S['z1'] - drop + 1, S['z1'])
    V = DIAMONDS                                                         # diamond holes, LEFT side, onto the barrel
    for cx in V['x']:
        for x in range(cx - V['half'], cx + V['half'] + 1):
            for z in range(V['z'] - V['half'], V['z'] + V['half'] + 1):
                if abs(x - cx) + abs(z - V['z']) <= V['half']:
                    g.cut(x, x, V['y_in'], S['y'], z, z)
                    recolour(g, x, x, V['y_in'] - 1, V['y_in'] - 1, z, z, 'port')
    P = PORT                                                             # ejection port, RIGHT side
    g.cut(P['x0'], P['x1'], -S['y'], P['y_in'], P['z0'], P['z1'])
    recolour(g, P['x0'], P['x1'], P['y_in'] + 1, P['y_in'] + 1, P['z0'], P['z1'], 'port')        # back wall
    recolour(g, P['x0'], P['x1'], -S['y'] + 1, P['y_in'], P['z0'] - 1, P['z0'] - 1, 'port')      # floor, the outer
    recolour(g, P['x0'], P['x1'], -D['y'] + 1, P['y_in'], P['z1'] + 1, P['z1'] + 1, 'port')      # face left metal (the roof is in the deck)
    C = COMP                                                             # the compensator on the nose, wrapping
    nose = Parts()                                                       # around the frame where it reaches back
    box(nose, 'slide', C['x0'], C['x1'], C['y'], C['z0'], C['z1'], 'metal', C['bevel'])
    for (x, y, z), c in nose.p['slide'].items():
        if (x, y, z) not in g.p['frame']:
            g.put('slide', x, y, z, c)
    for px in C['top_ports']:
        g.cut(px, px + C['port_w'] - 1, -2, 2, C['z1'] - C['port_depth'] + 1, C['z1'])
        recolour(g, px, px + C['port_w'] - 1, -2, 2, C['z1'] - C['port_depth'], C['z1'] - C['port_depth'], 'port')
    E = SERRATIONS
    for x in range(E['x0'], E['x1'] + 1, E['step']):
        g.cut(x, x, -S['y'], -S['y'], E['z0'], E['z1'])
        g.cut(x, x, S['y'], S['y'], E['z0'], E['z1'])
    R = REAR_SIGHT
    g.fill('slide', R['x0'], R['x1'], -R['y'], R['y'], S['z1'] - REAR_SLOPE['drop'] + 1, R['z1'], 'metal')
    g.cut(R['x0'], R['x1'], -R['notch'], R['notch'], R['z1'] - R['notch_depth'] + 1, R['z1'])
    for y in (-R['y'] + 1, R['y'] - 1):                                  # dots on the face toward the eye
        g.put('slide', R['x0'], y, R['dot_z'], 'sight_dot')
    F = FRONT_SIGHT
    g.fill('slide', F['x0'], F['x1'], -F['y'], F['y'], C['z1'] + 1, F['z1'], 'metal')
    g.put('slide', F['x0'], 0, F['dot_z'], 'sight_dot')
    B = BARREL                                                           # copper, seen through the holes and the port
    g.tube('barrel', B['x0'], B['x1'], B['zc'], B['r'], 'copper')
    K = CASE                                                             # a brass case in the port
    g.tube('barrel', K['x0'] + K['head'], K['x1'], K['zc'], K['r'], 'brass', yc=K['y'])
    g.tube('barrel', K['x0'], K['x0'] + K['head'] - 1, K['zc'], K['r'] + 0.4, 'brass_hi', yc=K['y'])
    M = MUZZLE                                                           # the bore into the compensator's front
    back = C['x1'] - M['depth']
    ri = math.ceil(M['bore']) + 2
    for y in range(-ri, ri + 1):
        for z in range(math.floor(B['zc'] - ri), math.ceil(B['zc'] + ri) + 1):
            d2 = y * y + (z - B['zc']) ** 2
            if d2 <= M['bore'] ** 2 + ROUND_SLACK:
                g.cut(back + 1, C['x1'], y, y, z, z)
                g.put('slide', back, y, z, 'bore')
            elif d2 <= (M['bore'] + 1) ** 2 + ROUND_SLACK:                # the bore's walls dark, a bright crown
                recolour(g, back + 1, C['x1'] - 1, y, y, z, z, 'port')
                recolour(g, C['x1'], C['x1'], y, y, z, z, 'metal_hi')


def cover(g):
    """The ejection port's cover, closed, its own part so it can swing open on its hinge later."""
    V = COVER
    for z in range(V['z0'], V['z1'] + 1):                                # one cube proud of the slide: the
        y = V['y'] + (1 if z >= DECK['z0'] else 0)                       # upper half steps in with the deck
        g.fill('cover', V['x0'], V['x1'], y, y, z, z, 'metal_mid')
        if V['z0'] < z < V['z1']:
            for x in V['ridges']:                                        # raised grip ridges on it
                g.put('cover', x, y - 1, z, 'metal_hi')
    for x in range(V['x0'], V['x1'] + 1):                                # the hinge along its bottom edge
        g.put('cover', x, V['y'], V['hinge_z'], 'metal_hi' if x % 4 < 2 else 'metal')


def build():
    g = Parts()
    grip(g)
    frame(g)
    slide(g)
    cover(g)
    return g
