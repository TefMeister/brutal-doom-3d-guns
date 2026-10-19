# Shared start for every Brutal Doom forge gun: finds blender-cubekit (cloned beside this repo), the house colours
# the shotgun, pistol and machine gun settled with Tefa (dark gun metal, worn dark-red paint, white UAC marks, green
# sights), and a few bold pieces every Doom gun here is built from.
# Tefa, 2026-10-19: "be as creative and bold as you want to with doom weapons - use different cube sizes to really
# emphasize cracks and cuts but also little screws and corners".
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "blender-cubekit")))

from forge import Model, mix, mul, hash01          # noqa: E402,F401
import forge_parts as fp                            # noqa: E402,F401

METAL = (34, 35, 39)            # the guns' near-black gun metal
METAL_HI = (60, 62, 68)
METAL_MID = (46, 48, 53)
PANEL = (72, 74, 79)            # grey panels
PANEL_DK = (52, 54, 58)
RED = (110, 30, 28)             # worn dark red paint (the machine gun's)
RED_HI = (146, 52, 46)
RED_DK = (72, 20, 18)
CAUTION = (200, 152, 36)
WHITE = (204, 204, 198)
GREEN = (60, 235, 80)           # sights and status lights
CYAN = (60, 200, 235)           # plasma
ORANGE = (240, 120, 30)         # heat and fire
BRASS = (176, 134, 62)
DARK = (10, 10, 11)
SCREW = (84, 86, 92)
BONE = (200, 190, 160)
FLESH = (130, 50, 46)
HELL = (220, 60, 20)            # hell-forged glow

UAC = ["#.#..#..###", "#.#.#.#.#..", "#.#.###.#..", "#.#.#.#.#..", "###.#.#.###"]
SKULL = ["..#######..", ".#########.", "###########", "##...#...##", "##...#...##", "###########",
         "#####.#####", ".#########.", "..#.#.#.#..", "..#######.."]
ARROW = ["#....", "###..", "#####", "###..", "#...."]
HAZARD_TRI = ["....#....", "...###...", "..##.##..", ".##.#.##.", "####.####", "#########"]


def armour(m, x0, x1, w, z0, z1, col, bevel=2.0, panel=None, inset=1.5, part=None):
    """A chunky armoured block: bevelled edges in half cubes, and an inset side panel framed by a cut line."""
    m.cbox(x0, x1, w, z0, z1, col, bevel=bevel, bevel_x=bevel / 2, edge=0.5, part=part)
    if panel:
        for side in ('+y', '-y'):
            pts = [(x0 + inset, z0 + inset), (x1 - inset, z0 + inset), (x1 - inset, z1 - inset),
                   (x0 + inset, z1 - inset), (x0 + inset, z0 + inset)]
            m.groove(pts, side, depth=2, dark=0.35)
            m.recolour(lambda x, y, z, s=side: (x0 + inset + 0.5 < x < x1 - inset - 0.5 and
                                                z0 + inset + 0.5 < z < z1 - inset - 0.5 and
                                                (y > w / 2 - 1.5 if s == '+y' else y < -w / 2 + 1.5)), panel)


def corner_screws(m, x0, x1, z0, z1, inset=2.0, kind='hex', col=SCREW, sides=('+y', '-y')):
    for side in sides:
        for x in (x0 + inset, x1 - inset):
            for z in (z0 + inset, z1 - inset):
                m.screw(x, z, side, col, kind=kind)


def vents(m, x0, x1, z0, z1, step=3.0, sides=('+y', '-y'), slant=0.0, glow=None):
    """Slots cut through a side, two cubes deep; glow paints their floors (heat, plasma)."""
    x = x0
    while x < x1:
        for side in sides:
            m.groove([(x, z0), (x + slant, z1)], side, depth=3, width=2, col=glow, dark=0.15)
        x += step


def hazard(m, x0, x1, y0, y1, z0, z1, step=2.0, a=CAUTION, b=DARK):
    m.recolour(lambda x, y, z: x0 <= x < x1 and y0 <= y < y1 and z0 <= z < z1,
               lambda x, y, z: a if int((x + z) / step) % 2 else b)


def worn_paint(rgb, hi, amount=0.25, seed=5):
    """Paint chipped back to its lighter worn colour in patches."""
    def f(x, y, z):
        n = hash01(int(x // 2), int(y // 2), int(z // 2), seed)
        return mix(rgb, hi, 0.8) if n > 1.0 - amount else mul(rgb, 0.95 + 0.1 * hash01(int(x), int(z), seed + 1))
    return f


def finish(m, seed, area, grime=0.2, scratches=14, cracks=2):
    """The standard weathering pass: worn edges, scratches on both sides, a few cracks, grime."""
    x0, x1, z0, z1 = area
    m.wear_edges(0.4, (150, 150, 156))
    m.scratches('+y', area, scratches, seed)
    m.scratches('-y', area, scratches, seed + 1)
    for i in range(cracks):
        side = '+y' if i % 2 == 0 else '-y'
        m.crack(x0 + (x1 - x0) * hash01(seed, i, 1), z0 + (z1 - z0) * hash01(seed, i, 2), side, 10, seed + 10 + i)
    m.grime(grime, seed + 20)
