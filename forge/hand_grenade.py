# Brutal Doom: the hand grenade, forge cube version. Free design, bold: a classic segmented frag body in olive drab,
# its squares cut deep with the smallest cubes, a steel fuse head with a spoon down the side, the pin's ring pulled
# out to the side, a yellow band and a stencilled mark.
import math

from _common import (Model, fp, METAL, METAL_HI, METAL_MID, CAUTION, WHITE, DARK, SCREW, mul, hash01)

OLIVE = (78, 88, 48)
OLIVE_DK = (48, 54, 28)


def build():
    m = Model("bd_hand_grenade")
    m.pivot = (0, 0, 0)
    m.ball(0, 0, 0, 10.0, fp.metal(OLIVE, 0.08), rz=12.0, edge=0.5)
    # the frag segments: grooves round it in both directions
    for k in range(8):
        a = k * math.pi / 8
        for side in ('+y', '-y'):
            pts = [(math.cos(a) * 11, -12), (math.cos(a) * 11, 12)]
            m.groove(pts, side, depth=2, dark=0.4)
    for z in (-7, -3.5, 0, 3.5, 7):
        for side in ('+y', '-y', '+x', '-x'):
            m.groove([(-12, z), (12, z)], side, depth=2, dark=0.4)
    m.recolour(lambda x, y, z: -1.5 < z < 1.5, CAUTION)
    # the fuse head, the spoon, the ring
    m.cyl(10, 15, 0, 0, 3.6, fp.metal(METAL_HI), axis='z', edge=0.25)
    m.cyl(15, 17, 0, 0, 2.6, fp.metal(METAL_MID), axis='z', edge=0.25)
    m.part = 'spoon'
    for i in range(40):
        t = i / 39
        x = 3.5 + t * 6 * (1 - t) * 2
        z = 15 - t * 22
        m.box(x, x + 1, -1.5, 1.5, z, z + 0.75, fp.metal(METAL_HI), size=0.25, keep=True)
    m.part = 'pin'
    for i in range(48):
        a = i / 48 * math.tau
        m.box(-0.25, 0.25, -6 + math.cos(a) * 4 - 0.25, -6 + math.cos(a) * 4 + 0.25, 13 + math.sin(a) * 4 - 0.25,
              13 + math.sin(a) * 4 + 0.25, fp.metal((190, 190, 196)), size=0.25)
    m.box(-0.5, 0.5, -3, 0, 12.75, 13.25, fp.metal((190, 190, 196)), size=0.25)
    m.part = 'body'
    m.decal(["#.#.###", "#.#.#..", "###.###", "#.#...#", "#.#.###"], -4, -4, '+y', WHITE, mode='paint')
    m.scratches('+y', (-9, 9, -10, 10), 8, 1801, length=(1, 4))
    m.scratches('-y', (-9, 9, -10, 10), 8, 1802, length=(1, 4))
    m.wear_edges(0.35, (160, 170, 120))
    m.grime(0.25, 1803)
    return m
