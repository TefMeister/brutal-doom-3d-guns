"""ref_sheets.py - picture sheets to model from: one weapon's animation (fire, reload ...) laid out frame by frame
in the order and length the game plays it, made from the mod's own sprites, plus a copy of its sounds.

    python ref_sheets.py <unpacked pk3> <weapons.json> <out folder> <weapon name> [<weapon name> ...]

The sheets and sounds are Brutal Doom's own art: they stay in the local reference folder and are NEVER committed.
"""
import json
import os
import shutil
import sys

from PIL import Image, ImageDraw

CELL = 160              # each frame is drawn in a square this many pixels wide
PER_ROW = 8
LABEL_H = 18
TITLE_H = 24            # room for the title line at the top
BACKGROUND = (40, 40, 44)


def sprite_index(root):
    idx = {}
    for dp, _, fns in os.walk(os.path.join(root, "sprites")):
        for fn in fns:
            stem, ext = os.path.splitext(fn)
            if ext.lower() == ".png" and len(stem) >= 6:
                idx.setdefault(stem[:5].upper(), os.path.join(dp, fn))
    return idx


def draw_run(run, idx, title, path):
    frames = [f for f in run["frames"] if f["sprite"].upper() in idx]
    if not frames:
        return False
    rows = (len(frames) + PER_ROW - 1) // PER_ROW
    sheet = Image.new("RGB", (PER_ROW * CELL, rows * (CELL + LABEL_H) + TITLE_H), BACKGROUND)
    d = ImageDraw.Draw(sheet)
    d.text((6, 4), f"{title}: {run['tics']:g} tics = {run['seconds']} s", fill=(230, 230, 230))
    for n, f in enumerate(frames):
        img = Image.open(idx[f["sprite"].upper()]).convert("RGBA")
        img.thumbnail((CELL - 8, CELL - 8))
        x, y = (n % PER_ROW) * CELL, TITLE_H + (n // PER_ROW) * (CELL + LABEL_H)
        sheet.paste(img, (x + (CELL - img.width) // 2, y + (CELL - img.height) // 2), img)
        d.text((x + 4, y + CELL), f"{f['sprite']}  @{f['tic']:g}  x{f['tics']:g}", fill=(200, 200, 120))
    sheet.save(path)
    return True


def main(argv):
    if len(argv) < 4:
        print(__doc__)
        return 2
    root, sheet_json, out, names = argv[0], argv[1], argv[2], argv[3:]
    weapons = {w["name"].lower(): w for w in json.load(open(sheet_json, encoding="utf-8"))}
    idx = sprite_index(root)
    for name in names:
        w = weapons.get(name.lower())
        if not w:
            print(f"{name}: not in the sheet")
            continue
        folder = os.path.join(out, w["name"])
        os.makedirs(os.path.join(folder, "sounds"), exist_ok=True)
        made = []
        for row, run in w["runs"].items():
            fn = row.split(" (")[0].lower().replace(" ", "-").replace("/", "") + ".png"
            if draw_run(run, idx, f"{w['name']} - {row}", os.path.join(folder, fn)):
                made.append(fn)
        for logical, rel in w["sounds"].items():
            src = os.path.join(root, rel) if rel else ""
            if src and os.path.isfile(src):
                shutil.copy2(src, os.path.join(folder, "sounds", os.path.basename(src)))
        for spr in w["sprites"]:
            for key, p in idx.items():
                if key.startswith(spr.upper()):
                    os.makedirs(os.path.join(folder, "sprites"), exist_ok=True)
                    shutil.copy2(p, os.path.join(folder, "sprites", os.path.basename(p)))
        print(f"{w['name']}: {', '.join(made) or 'no sheets'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
