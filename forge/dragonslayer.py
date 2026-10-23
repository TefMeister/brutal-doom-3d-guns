# Brutal Doom: the Dragonslayer, forge cube version. Free design, bold: a sword far too big to be a sword: a slab of
# raw iron taller than a man, thick and blunt-tipped, its flat pitted and cut with nicks, a heavy square guard, a
# long grip bound in leather straps, a pommel ring, and old blood dried into the edges.
from _common import (Model, fp, METAL, METAL_HI, METAL_MID, RED_DK, DARK, SCREW, mix, mul, hash01)

IRON = (88, 86, 84)
IRON_DK = (54, 52, 50)
LEATHER = (80, 48, 28)
LENGTH = 520                           # the blade, cubes (1.77 m)


def iron(x, y, z):
    return mix(IRON, IRON_DK, hash01(int(x // 3), int(z // 3), int(y), 2801) * 0.7)


def build():
    m = Model("bd_dragonslayer")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (40, 0, 0)
    m.part = 'blade'
    # the blade: a thick slab, bevelled to blunt edges, its tip cut square with the corners knocked off
    blade = [(64, -16), (LENGTH - 16, -16), (LENGTH, -8), (LENGTH, 8), (LENGTH - 16, 16), (64, 16)]
    m.cprism(blade, 7.0, iron, bevel=3.0, edge=0.5)
    m.groove([(70, 0), (LENGTH - 30, 0)], '+y', depth=2, width=4, dark=0.6)                   # the fuller
    m.groove([(70, 0), (LENGTH - 30, 0)], '-y', depth=2, width=4, dark=0.6)
    for i in range(26):                                                                    # nicks in both edges
        x = 80 + i * 17 + hash01(i, 1, 2802) * 8
        z = 15.5 if i % 2 else -16.5
        m.box(x, x + 1.5 + hash01(i, 2, 2802) * 3, -4, 4, z, z + 1.0, None, size=0.25, carve=True)
    for side in ('+y', '-y'):
        for i in range(10):
            m.crack(90 + i * 40, -6 + (i % 3) * 6, side, 8, 2810 + i + (20 if side == '-y' else 0), dark=0.5)
        m.scratches(side, (70, LENGTH - 20, -14, 14), 40, 2840 if side == '+y' else 2841, length=(4, 14))
    m.recolour(lambda x, y, z: abs(z) > 13 and hash01(int(x // 2), int(z), 2803) > 0.55,
               lambda x, y, z: mix((70, 14, 10), (36, 8, 6), hash01(int(x), int(z), 2804)))
    m.part = 'guard'
    # the guard, the grip, the pommel ring
    m.cbox(56, 66, 10.0, -24, 24, fp.metal(METAL_MID), bevel=2.0, edge=0.5)
    for side in ('+y', '-y'):
        m.bolt(61, -18, side, SCREW)
        m.bolt(61, 18, side, SCREW)
    m.part = 'grip'
    m.cyl(-30, 56, 0, 0, 4.2, fp.wood(LEATHER, mul(LEATHER, 0.6)), edge=0.5)
    for x in range(-28, 54, 6):
        m.cyl(x, x + 1.5, 0, 0, 4.6, (40, 24, 14), edge=0.25)
    m.part = 'pommel'
    m.cyl(-36, -30, 0, 0, 6.0, fp.metal(METAL_HI), edge=0.25)
    m.cyl(-4, 4, -42, 0, 6.0, fp.metal(METAL_HI), axis='y', hollow=3.5, edge=0.25)
    m.wear_edges(0.4, (170, 168, 164))
    m.grime(0.25, 2805)
    return m
