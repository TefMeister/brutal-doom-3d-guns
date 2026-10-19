# Brutal Doom: the axe, forge cube version. Free design, bold: a long dark hardwood haft bound in black grip tape
# and steel collars, a huge bearded head with a bright ground edge chipped and nicked, a spike on the back, a skull
# punched through the blade, rivets holding it on, old blood dried into the edge.
from _common import (Model, fp, METAL, METAL_HI, METAL_MID, RED_DK, WHITE, DARK, SCREW, SKULL, finish, mul, mix,
                     hash01)

HAFT = (96, 58, 32)
HAFT_DK = (52, 30, 14)
TAPE = (26, 26, 28)
EDGE = (200, 204, 210)
HEAD = (70, 72, 78)
LENGTH = 230


def build():
    m = Model("bd_axe")
    m.pivot = (60, 0, 0)
    # the haft along x, slightly oval
    m.cyl(0, LENGTH, 0, 0, 3.4, fp.wood(HAFT, HAFT_DK), edge=0.5)
    m.ball(-1, 0, 0, 4.2, fp.metal(METAL_HI), edge=0.25)                                   # pommel
    m.cyl(0, 3, 0, 0, 4.0, fp.metal(METAL), edge=0.25)
    for x0, x1 in ((8, 70),):                                                             # taped grip
        m.cyl(x0, x1, 0, 0, 3.7, TAPE, edge=0.25)
        for x in range(x0, x1, 3):
            m.cyl(x, x + 0.5, 0, 0, 3.9, (44, 44, 46), size=0.25, edge=0.25)
    for x in (72, 140, LENGTH - 30):
        m.cyl(x, x + 3, 0, 0, 4.0, fp.metal(METAL_HI), edge=0.25)
    # the head: a bearded blade below the haft's end, a spike above; both 3 cubes thick, tapering to the edge
    hx = LENGTH - 26
    blade = [(hx, 4), (hx + 22, 4), (hx + 22, -6), (hx + 30, -26), (hx + 32, -40), (hx + 24, -44), (hx + 10, -38),
             (hx + 2, -20), (hx, -6)]
    m.cprism(blade, 4.0, fp.metal(HEAD), bevel=1.0, edge=0.25)
    # the ground edge: a strip of bright steel along the curved front
    m.recolour(lambda x, y, z: z < -18 and x > hx + 22 - (z + 18) * 0.25 or (z < -36 and x > hx + 8),
               lambda x, y, z: mul(EDGE, 0.95 + 0.1 * hash01(int(x), int(z), 3)))
    m.cprism([(hx + 4, 4), (hx + 18, 4), (hx + 14, 22), (hx + 10, 26), (hx + 8, 22)], 3.0, fp.metal(HEAD),
             bevel=0.75, edge=0.25)                                                        # the back spike
    m.cyl(hx - 2, hx + 24, 0, 0, 5.0, fp.metal(METAL_MID), edge=0.25)                      # the eye socket
    for x in (hx + 4, hx + 18):
        for side in ('+y', '-y'):
            m.screw(x, 0, side, SCREW, kind='rivet')
    # nicks in the edge, a skull punched through, dried blood
    for i in range(7):
        z = -24 - i * 2.6
        x = hx + 30 - (z + 24) * -0.1
        m.box(x - 1.5, x + 3, -2.5, 2.5, z, z + 1.0 + (i % 2) * 0.5, None, size=0.25, carve=True)
    m.decal(SKULL, hx + 8, -12, '+y', None, dot=1, mode='carve')
    m.decal(SKULL, hx + 8, -12, '-y', None, dot=1, mode='carve')
    m.recolour(lambda x, y, z: hash01(int(x), int(z), 7) > 0.7 and z < -10 and x > hx + 14,
               lambda x, y, z: mix((70, 12, 10), (40, 8, 6), hash01(int(x), int(z), 8)))
    m.wear_edges(0.35, (190, 190, 196))
    for side in ('+y', '-y'):
        m.scratches(side, (hx, hx + 30, -40, 0), 12, 501 if side == '+y' else 502, length=(2, 6))
        m.crack(hx + 12, -30, side, 8, 503 if side == '+y' else 504, heading=0.6)
    m.scratches('+y', (75, 200, -3, 3), 10, 505, length=(3, 10))
    m.grime(0.2, 506)
    return m
