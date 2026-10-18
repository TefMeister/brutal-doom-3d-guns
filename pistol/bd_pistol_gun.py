# The Brutal Doom cube pistol's shape, split into parts: {part: {(x, y, z): colour name}}. No Blender here.
# Parts: 'frame' (frame, grip, guard - never moves), 'slide' (slide and its levers - runs back on a shot),
# 'barrel', 'trigger', 'hammer', 'mag'.
from bd_pistol_settings import (GRIP, GRIP_PANEL, MAG_BASE, FRAME, GUARD, TRIGGER, SLIDE_CATCH, TAKEDOWN, SLIDE,
                                OPEN_TOP, SERRATIONS, REAR_SIGHT, FRONT_SIGHT, SAFETY, BARREL, HAMMER)
from parts import Parts


def grip_front(z):
    return round(GRIP['front'] - (GRIP['z1'] - z) * GRIP['rake'])


def grip_back(z):
    return round(GRIP['back'] - (GRIP['z1'] - z) * GRIP['rake'])


def box(g, part, x0, x1, y, z0, z1, c, bevel=0):
    """A square bar along x, its four long edges cut back by `bevel` cubes (0 = sharp corners)."""
    for x in range(x0, x1 + 1):
        for yy in range(-y, y + 1):
            for z in range(z0, z1 + 1):
                if bevel and (y - abs(yy)) + min(z - z0, z1 - z) < bevel:
                    continue
                g.put(part, x, yy, z, c)


def grip(g):
    G, P = GRIP, GRIP_PANEL
    for z in range(G['z0'], G['z1'] + 1):
        f, b = grip_front(z), grip_back(z)
        for x in range(b, f + 1):
            for y in range(-G['y'], G['y'] + 1):
                edge_x = x in (b, f)
                if edge_x and abs(y) == G['y']:
                    continue                                             # rounded corners
                c = 'metal'
                in_panel = b + P['inset'] <= x <= f - P['inset'] and P['z0'] <= z <= P['z1']
                if abs(y) == G['y'] and in_panel:
                    c = 'grip_check' if (x + z) % P['check'] == 0 else 'grip'
                g.put('frame', x, y, z, c)
    M = MAG_BASE
    for z in range(M['z0'], M['z1'] + 1):
        g.fill('mag', grip_back(G['z0']) - M['over'], grip_front(G['z0']) + M['over'], -G['y'], G['y'], z, z,
               'metal_dark')


def frame(g):
    F = FRAME
    box(g, 'frame', F['x0'], F['x1'], F['y'], F['z0'], F['z1'], 'metal', 1)
    G = GUARD
    front = grip_front(G['z_bottom'] + 1)
    g.fill('frame', front, G['x1'], -G['y'], G['y'], G['z_bottom'], G['z_bottom'] + 1, 'metal')      # bottom bar
    g.fill('frame', G['x1'] - 1, G['x1'], -G['y'], G['y'], G['z_bottom'], F['z0'] - 1, 'metal')      # squared front
    g.fill('frame', G['x1'] + 1, G['x1'] + G['hook'], -G['y'], G['y'], G['z_bottom'], G['z_bottom'] + 1,
           'metal')                                                                                   # the hook
    for x, z in TRIGGER:
        g.fill('trigger', x, x, -1, 1, z, z, 'metal_hi')
    S, T = SLIDE_CATCH, TAKEDOWN
    g.fill('frame', S['x0'], S['x1'], F['y'] + 1, F['y'] + 1, S['z'], S['z'], 'metal_hi')
    g.fill('frame', T['x0'], T['x1'], F['y'] + 1, F['y'] + 1, T['z'], T['z'], 'metal_hi')


def slide(g):
    S, O = SLIDE, OPEN_TOP
    box(g, 'slide', S['x0'], S['x1'], S['y'], S['z0'], S['z1'], 'metal', S['bevel'])
    g.cut(O['x0'], O['x1'], -O['y'], O['y'], O['z0'], S['z1'])                       # the open top
    g.cut(O['dip_x0'], O['dip_x1'], -S['y'], S['y'], O['dip_z0'], S['z1'])           # its sides dipping lower
    R = SERRATIONS
    for x in range(R['x0'], R['x1'] + 1, R['step']):
        g.cut(x, x, -S['y'], -S['y'], R['z0'], R['z1'])
        g.cut(x, x, S['y'], S['y'], R['z0'], R['z1'])
    R = REAR_SIGHT
    g.fill('slide', R['x0'], R['x1'], -R['y'], R['y'], S['z1'] + 1, R['z1'], 'metal')
    g.cut(R['x0'], R['x1'], -R['notch'], R['notch'], R['z1'], R['z1'])               # the notch
    for y in (-R['y'] + 1, R['y'] - 1):
        g.put('slide', R['x1'], y, R['z1'] - 1, 'sight_dot')
    F = FRONT_SIGHT
    g.fill('slide', F['x0'], F['x1'], 0, 0, S['z1'] + 1, F['z1'], 'metal')
    g.put('slide', F['x0'], 0, F['z1'], 'sight_dot')
    A = SAFETY
    g.fill('slide', A['x0'], A['x1'], -S['y'] - 1, -S['y'] - 1, A['z0'], A['z1'], 'metal_hi')
    g.fill('slide', A['x0'], A['x1'], S['y'] + 1, S['y'] + 1, A['z0'], A['z1'], 'metal_hi')
    B = BARREL
    g.tube('barrel', B['x0'], B['x1'], B['zc'], B['r'], 'barrel')
    g.tube('barrel', B['x1'] - 1, B['x1'], B['zc'], B['bore'], 'bore')


def hammer(g):
    H = HAMMER
    g.fill('hammer', H['x0'], H['x1'], -H['y'], H['y'], H['z0'], H['z1'], 'metal_hi')
    g.cut(H['x0'], H['x0'], -H['y'], H['y'], H['z1'], H['z1'])                       # rounded spur


def build():
    g = Parts()
    grip(g)
    frame(g)
    slide(g)
    hammer(g)
    return g
