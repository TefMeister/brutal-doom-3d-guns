# Notes

Newest first. Claims carry a tag for how well they are known; untagged means `[hypothesis]`.

## 2026-10-29 - the exporters can leave the hands out (`--no-hands`)

**Why** (Tefa): "now that the hand can actually dock on the weapon we need to re-do weapons without hands on them".
The Ashes body rig places the arms and hands from the controllers, so a glove baked into a gun model is a second hand.

**What changed** (dev PC, /pd): `tools/gz_forge_export.py`, `tools/gz_vr_export.py` and `tools/forge_jobs.py` take a
`--no-hands` switch (for forge jobs also `"no_hands": true` per job). With it, every object named `*_glove_*` (and, in
`gz_vr_export.py`, everything under the GLOVES list) is left out of the model. The grip point is still measured from
the right glove first, so a gun with and without hands sits in exactly the same spot in the hand.

**Checked** on the forge revolver with two stand-in box gloves (scratch build, not kept): with hands 122522 triangles,
without 122498 (the 24 glove triangles); same grip both ways (0.0, -0.05, -0.04); comparing every corner of the two
models, 72 corners exist only in the with-hands model and none only in the no-hands one, so the gun itself did not
move or change `[verified-numerically 2026-10-29, n=1 gun]`. `gz_vr_export.py`'s switch (shotgun, pistol, machine
gun) is `[compile-verified 2026-10-29]` only: those blends live in MEGA on the home PC. Whether their gloves are
separate objects there (so the switch is enough) or joined into the gun mesh is not known `[hypothesis]`.

**Next** (home PC, where the blends are): re-export every forge gun with `forge_jobs.py doom|ashes <jobs> --no-hands`
and the three hand-built guns with `gz_vr_export.py <gun> <out> --no-hands`, then look at one in Blender.

## 2026-10-18 - project started

**Asked for** (Tefa): 3D guns for Brutal Doom in Doom 1 and 2, a project like the Ashes 2063 weapons. Extract
the weapons' data (fire rates, damage, reload times, sounds); then the shotgun, with its hands placed the way
the Ashes 2063 shotgun's are, looking like the Brutal Doom shotgun, with Doomguy's armoured gloves (Tefa sent a
reference picture: dark steel plates over a brown under-glove); then the pistol, as a beefed-up Beretta 92F.

**What is here now**
- Brutal Doom **v22 test 6** is the version we follow.
- Doom and Doom II: the Steam *Ultimate Doom* install, which carries both the original WADs and the 2024
  re-release ones. `[measured 2026-10-18]`
- The engine: our modified GZDoomVR from the Ashes 2063 project. `[measured 2026-10-18]` on the dev PC.
- **Brutal Doom ships no 3D gun models**: its `models/` folder holds blood, decals, vehicles and decorations
  only, so every gun is built from scratch. The weapons themselves are sprites. `[measured 2026-10-18]`

**The weapon numbers** are in `sheet/WEAPONS.md` (55 weapons). They come from playing each weapon's state list
forward on the plain path: a normal player class (not Tactical), nobody pressing anything, ammo as the row
says. `[inferred-static]` until timed in the game. The two we start with:

| | Shotgun | Pistol |
| --- | --- | --- |
| Shot to ready again | 27 tics = 0.77 s, pump sounds at tic 13 and 20 | 11 tics = 0.31 s |
| Damage per shot | 4 x 13 + 5 x 13 (9 pellets of 13) | 1 accurate bullet of 14 |
| Magazine | 9 (8 + 1 in the chamber), shells loaded one at a time | 16 |
| Reload | from empty 105 tics = 3.0 s; one shell 25 tics = 0.71 s | from empty 36 tics = 1.03 s |
| Raise / lower | 5 / 5 tics | 5 / 4 tics |

- Brutal Doom's **Tactical** class pumps the shotgun more slowly and fires a third pellet volley; the normal
  classes skip both. `[inferred-static]`
- Brutal Doom's pump animation **turns the shotgun on its side** while the left hand works the pump (frames
  SHTN B to Q). Worth deciding whether our 3D shotgun does the same, or pumps straight like the Ashes one.

**Kept off GitHub:** Brutal Doom's sprites, sounds and the picture sheets made from them, and Tefa's glove
reference picture. They live in a local reference folder on the dev PC.

**Next:** the shotgun, in Blender, together, one step at a time: first bring in the Ashes 2063 shotgun with
hands to see how the hands sit, then block out the Brutal Doom shotgun's shape beside it.

## 2026-10-24 - every forge gun in the game; relaxed free left hand (home PC)
- 25 forge guns in Brutal Doom as still models held in the right hand, gloves on (`tools/gz_forge_export.py`,
  `tools/forge_jobs.py`, `tools/weapon_sprites.py`; forge/README.md). Flat check: all 25 drawn as 3D models when
  selected, no errors `[verified-live 2026-10-24, n=1, flat]`. Not yet worn: placement (the right glove's middle at
  the revolver's tuned spot) and size per gun are untested in the headset.
- Two crashes on the way, both found and fixed: a MODELDEF frame `#` (the BFG 10K uses it in its states; GZDoom only
  takes A to Z, [, \ and ]) `[verified-live 2026-10-24]`; and a test-only helper's long `user` string setting
  ("User info descriptor too big"), now a `server` setting. The helper was never part of the mod.
- Free left hand rebuilt the Ashes way (ashes-2063-weapons NOTES.md, 2026-10-24: the game swaps the off hand):
  Doomguy's left glove relaxed, palm in, thumb on top, stored flipped top to bottom. Not worn.
