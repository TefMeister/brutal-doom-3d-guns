# Brutal Doom: the flame cannon (the Mancubus's arm cannon, carried), forge cube version. Free design, bold: a fat
# demonic flesh-and-iron cannon: a ribbed iron barrel with a glowing orange throat, pipes of fuel running along it,
# raw red flesh wrapped round the back where it was torn off, bolted iron bands, a crude grip spiked through the flesh.
import math

from _common import (Model, fp, METAL, METAL_HI, METAL_MID, FLESH, HELL, ORANGE, DARK, SCREW, mix, mul, hash01)

IRON = (70, 64, 60)
FLESH_DK = (80, 26, 24)
Z_AXIS = 22.0


def flesh(x, y, z):
    return mix(FLESH, FLESH_DK, hash01(int(x // 2), int(y // 2), int(z // 2), 2301))


def build():
    m = Model("bd_flame_cannon")
    m.pivot = (50, 0, 0)
    m.ball(30, 0, Z_AXIS, 22.0, flesh, ry=18.0, rz=18.0, edge=0.5)                          # torn flesh at the back
    for i in range(30):
        a = hash01(i, 1, 2302) * math.tau
        m.crack(30 + math.cos(a) * 10, Z_AXIS + math.sin(a) * 10, '+y' if i % 2 else '-y', 6, 2303 + i, dark=0.5)
    m.cyl(36, 170, 0, Z_AXIS, 13.0, fp.rusty(IRON, (110, 56, 30), 0.35, seed=2304), edge=0.5)
    for x in range(46, 166, 10):
        m.cyl(x, x + 3, 0, Z_AXIS, 14.0, fp.metal(METAL), edge=0.25)
        for k in range(6):
            a = k * math.pi / 3
            m.ball(x + 1.5, math.cos(a) * 14, Z_AXIS + math.sin(a) * 14, 1.0, fp.metal(METAL_HI), edge=0.25)
    m.cyl(166, 182, 0, Z_AXIS, 15.0, fp.metal(METAL_MID), r1=17.0, edge=0.5)
    m.cyl(170, 183, 0, Z_AXIS, 9.0, None, r1=12.0, edge=0.5, carve=True)
    m.cyl(169, 170, 0, Z_AXIS, 9.0, HELL, size=0.25, edge=0.25)
    m.cyl(160, 169, 0, Z_AXIS, 6.0, ORANGE, edge=0.25)
    # fuel pipes along both sides into the flesh
    for y in (-15, 15):
        m.cyl(20, 160, y, Z_AXIS + 6, 2.0, fp.metal(METAL_HI), edge=0.25)
        for x in range(30, 160, 20):
            m.cyl(x, x + 2, y, Z_AXIS + 6, 2.6, fp.metal(METAL), edge=0.25)
    # the grip, iron, spiked through the flesh, and a lever trigger
    m.cprism([(56, Z_AXIS - 12), (48, Z_AXIS - 14), (42, -14), (52, -16), (58, -4), (64, Z_AXIS - 12)], 10.0,
             fp.metal(METAL), bevel=2.0, edge=0.5)
    fp.trigger(m, 68, Z_AXIS - 12, fp.metal(METAL_HI), length=8, curve=1.5)
    for y in (-5, 5):
        m.cyl(Z_AXIS - 22, Z_AXIS - 8, 50, y, 1.2, fp.metal(METAL_HI), axis='z', r1=0.4, edge=0.25)
    m.cprism([(100, Z_AXIS - 13), (96, 0), (104, -2), (110, Z_AXIS - 13)], 8.0, fp.metal(METAL), bevel=1.5,
             edge=0.5)
    m.scratches('+y', (40, 165, Z_AXIS - 10, Z_AXIS + 10), 16, 2310)
    m.scratches('-y', (40, 165, Z_AXIS - 10, Z_AXIS + 10), 16, 2311)
    m.wear_edges(0.3, (170, 150, 130))
    m.grime(0.3, 2312, col=(40, 18, 12))
    return m
