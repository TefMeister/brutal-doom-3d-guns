# Doomguy's gloves posed on the Brutal Doom shotgun, in the gun's cube space. No Blender here.
# Gun space: x rear -> muzzle, y + = the gun's LEFT, z up (as bd_gun.py).
# The poses and placements are the Ashes shotgun hands' (ashes-2063-weapons, vs_hands.py, 2026-09-24): same finger
# bends, thumb paths, turns and leans. Their cube-by-cube fixes fitted only the Ashes gun and are not carried over;
# cubes that land inside this gun are dropped. The right hand is refitted to the stock together at the home PC.
from bd_glove import right_glove, left_glove
from bd_glove_settings import RIGHT_POSE, LEFT_POSE


def _right_axes(xh, yh, zh):
    """Fingers forward, thumb side up, back of the hand to the gun's right (the Ashes pistol-grip hand)."""
    P = RIGHT_POSE
    x, y, z = yh + P['x0'], -zh + P['y0'], -xh + P['z0']
    return x - round(max(0, P['grip_top'] - z) * P['rake']), y, z         # following the grip's lean


def _left_axes(xh, yh, zh):
    """Palm up under the pump, fingers round its right side, thumb forward along its left: a half turn about x."""
    P = LEFT_POSE
    x, y, z = xh + P['x0'], -yh + P['y0'], -zh + P['z0']
    return x, y, z - round(max(0, y - P['left_edge']) * P['wrist_drop'])   # the wrist angles down and away


def _place(cells, axes, shift, blocked):
    out = {}
    for c, colour in cells.items():
        x, y, z = axes(*c)
        x, y, z = x + shift[0], y + shift[1], z + shift[2]
        if (x, y, z) not in blocked:
            out[(x, y, z)] = colour
    return out


def gloves(blocked):
    """{'right': cells, 'left': cells} in gun space, never inside `blocked` (the gun's own cubes)."""
    R, L = RIGHT_POSE, LEFT_POSE
    right = right_glove(curls=R['curls'], thumb=R['thumb'])
    left = left_glove(curls=L['curls'], thumb=L['thumb'], thumb_base=L['thumb_base'], thumb_size=L['thumb_size'],
                      back_top=False)
    return {'right': _place(right, _right_axes, R['shift'], blocked),
            'left': _place(left, _left_axes, L['shift'], blocked)}
