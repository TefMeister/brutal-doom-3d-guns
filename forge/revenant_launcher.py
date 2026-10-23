# Brutal Doom: the hellish missile launcher (the Revenant's shoulder launchers torn off and made into a gun), forge
# cube version. Free design, bold: two bone-white and rusted launch pods on a ribcage of curved bones, sinew and red
# flesh binding them to a steel grip, glowing hell-orange inside each pod, spikes and a skull at the back.
import math

from _common import (Model, fp, METAL, METAL_HI, BONE, FLESH, HELL, DARK, SCREW, SKULL, mul, mix, hash01)

RUST = (120, 66, 34)
SINEW = (150, 60, 56)
Z_AXIS = 18.0


def bone(x, y, z):
    return mix(BONE, mul(BONE, 0.7), hash01(int(x // 2), int(z // 2), int(y), 2001) * 0.6)


def build():
    m = Model("bd_revenant_launcher")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (40, 0, 0)
    m.part = 'pods'
    # the two pods, side by side: rusted tubes with bone shells
    for y in (-8, 8):
        m.cyl(30, 130, y, Z_AXIS, 6.5, fp.rusty(mul(BONE, 0.8), RUST, 0.45, seed=2002), edge=0.5)
        m.cyl(126, 132, y, Z_AXIS, 7.2, bone, edge=0.25)
        m.cyl(128, 133, y, Z_AXIS, 4.2, None, edge=0.25, carve=True)
        m.cyl(126, 128, y, Z_AXIS, 4.2, HELL, size=0.25, edge=0.25)
        for x in range(40, 124, 14):
            m.cyl(x, x + 3, y, Z_AXIS, 7.0, fp.metal(METAL), edge=0.25)
    m.part = 'ribcage'
    # the ribcage: curved bones arching over both pods
    for x in range(44, 120, 10):
        for i in range(30):
            a = i / 29 * math.pi
            m.ball(x, math.cos(a) * 17, Z_AXIS + math.sin(a) * 10, 1.3, bone, edge=0.25)
    m.cyl(36, 124, 0, Z_AXIS + 10, 2.0, bone, edge=0.25)                                     # the spine
    for x in range(40, 124, 6):
        m.ball(x, 0, Z_AXIS + 12.5, 1.5, bone, edge=0.25)
    m.part = 'flesh'
    # flesh and sinew binding it to the grip below
    m.cbox(30, 90, 18.0, Z_AXIS - 12, Z_AXIS - 5, lambda x, y, z: mix(FLESH, SINEW, hash01(int(x), int(y), 2003)),
           bevel=3.0, edge=0.5)
    for x in range(34, 90, 6):
        for side in ('+y', '-y'):
            m.groove([(x, Z_AXIS - 11), (x + 3, Z_AXIS - 6)], side, depth=1, col=(70, 16, 14))
    m.part = 'grip'
    m.cprism([(50, Z_AXIS - 12), (42, Z_AXIS - 14), (36, -14), (46, -16), (52, -4), (58, Z_AXIS - 12)], 9.0,
             fp.metal(METAL), bevel=2.0, edge=0.5)
    m.part = 'guard'
    fp.guard(m, 56, 70, -2, Z_AXIS - 12, fp.metal(METAL))
    fp.trigger(m, 62, Z_AXIS - 12, fp.metal(METAL_HI), length=6)
    m.part = 'spikes'
    # spikes along the sides, a skull at the back
    for x in range(40, 128, 12):
        for s in (-1, 1):
            m.cyl(x, x + 7, s * 15, Z_AXIS - 4, 1.4, bone, r1=0.25, edge=0.25)
    m.part = 'skull'
    m.ball(22, 0, Z_AXIS, 10.0, bone, rz=11.0, edge=0.5)
    for y in (-4, 4):
        m.ball(14, y, Z_AXIS + 2, 3.0, DARK, edge=0.25, carve=False)
        m.ball(13.5, y, Z_AXIS + 2, 1.2, HELL, edge=0.25)
    m.cbox(12, 18, 6.0, Z_AXIS - 8, Z_AXIS - 4, DARK, size=0.5)
    for i in range(5):
        m.box(13, 15, -5 + i * 2.25, -4 + i * 2.25, Z_AXIS - 9, Z_AXIS - 6, bone, size=0.5)
    m.scratches('+y', (30, 130, Z_AXIS - 6, Z_AXIS + 6), 14, 2004)
    m.scratches('-y', (30, 130, Z_AXIS - 6, Z_AXIS + 6), 14, 2005)
    m.crack(22, Z_AXIS + 6, '+y', 10, 2006)
    m.crack(80, Z_AXIS + 2, '-y', 14, 2007)
    m.grime(0.3, 2008, col=(50, 20, 14))
    return m
