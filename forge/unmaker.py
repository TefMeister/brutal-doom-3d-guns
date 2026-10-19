# Brutal Doom: the Unmaker, forge cube version. Free design, bold: a demon-forged weapon: a body of black bone and
# hell iron shaped like a stretched skull with a mouth that is the muzzle, red eyes glowing in its sockets, three
# curved horns sweeping back, ribs of bone along the sides, veins of hell-red light, a grip of wrapped sinew.
import math

from _common import (Model, fp, METAL, BONE, FLESH, HELL, DARK, SCREW, mix, mul, hash01)

BLACK_BONE = (44, 38, 36)
HELL_RED = (255, 40, 20)
Z_AXIS = 20.0


def black_bone(x, y, z):
    return mix(BLACK_BONE, (80, 70, 62), hash01(int(x // 2), int(y // 2), int(z // 2), 2501) * 0.5)


def build():
    m = Model("bd_unmaker")
    m.pivot = (40, 0, 0)
    # the long skull body, its jaw opening at the front
    m.ball(80, 0, Z_AXIS, 70.0, black_bone, ry=13.0, rz=13.0, edge=0.5)
    m.ball(150, 0, Z_AXIS - 2, 14.0, black_bone, ry=15.0, rz=13.0, edge=0.5)                 # the skull's head
    m.cyl(150, 168, 0, Z_AXIS - 4, 7.0, None, r1=9.0, edge=0.25, carve=True)                 # the mouth
    m.cyl(148, 151, 0, Z_AXIS - 4, 7.0, HELL_RED, size=0.25, edge=0.25)
    for k in range(9):                                                                      # teeth round it
        a = math.pi + k * math.pi / 8
        m.cyl(160, 166, math.cos(a) * 8, Z_AXIS - 4 + math.sin(a) * 8, 1.2, BONE, r1=0.3, edge=0.25)
        m.cyl(160, 166, math.cos(a) * 8, Z_AXIS - 4 - math.sin(a) * 8, 1.2, BONE, r1=0.3, edge=0.25)
    for y in (-6, 6):                                                                       # glowing eyes
        m.ball(158, y, Z_AXIS + 5, 3.0, None, edge=0.25, carve=True)
        m.ball(156.5, y, Z_AXIS + 5, 2.0, HELL_RED, edge=0.25)
    # three horns sweeping back from the head
    for side, (y0, z0) in ((0, (0, Z_AXIS + 12)), (1, (11, Z_AXIS + 6)), (-1, (-11, Z_AXIS + 6))):
        for i in range(40):
            t = i / 39
            x = 146 - t * 60
            y = y0 + side * t * 6
            z = z0 + math.sin(t * math.pi * 0.8) * 10 + t * 4
            m.ball(x, y, z, 3.0 * (1 - t) + 0.6, BONE, edge=0.25)
    # bone ribs along the sides, red veins between them
    for x in range(40, 132, 9):
        for i in range(24):
            a = -math.pi / 2 + i / 23 * math.pi
            for s in (-1, 1):
                m.ball(x, s * (12.5 + math.cos(a) * 1.5), Z_AXIS + math.sin(a) * 11, 1.2, BONE, edge=0.25)
    for side in ('+y', '-y'):
        for i in range(6):
            m.groove([(45 + i * 15, Z_AXIS - 4), (50 + i * 15, Z_AXIS + 5), (54 + i * 15, Z_AXIS - 2)], side,
                     depth=1, col=HELL_RED)
    # grip of wrapped sinew, a bone trigger
    m.cprism([(60, Z_AXIS - 10), (52, Z_AXIS - 12), (46, -12), (56, -14), (62, -2), (68, Z_AXIS - 10)], 10.0,
             lambda x, y, z: mix(FLESH, (90, 30, 28), (int(z) % 3) / 3), bevel=2.0, edge=0.5)
    fp.trigger(m, 72, Z_AXIS - 10, BONE, length=7)
    m.ball(10, 0, Z_AXIS, 12.0, black_bone, edge=0.5)
    m.ball(2, 0, Z_AXIS, 5.0, HELL_RED, edge=0.25)
    m.wear_edges(0.25, (140, 120, 110))
    m.scratches('+y', (20, 140, Z_AXIS - 10, Z_AXIS + 10), 14, 2520)
    m.scratches('-y', (20, 140, Z_AXIS - 10, Z_AXIS + 10), 14, 2521)
    return m
