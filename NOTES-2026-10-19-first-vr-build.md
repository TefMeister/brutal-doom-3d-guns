# 2026-10-19 — First VR test build: Doom 1 + Brutal Doom with our three guns

Tefa: *"can you see if you can get DOOM 1 working in VR with the brutal doom mod and our first 3 weapons in it?"*

## What was made (home PC)

- `tools/gz_vr_export.py` (new): exports one gun from its .blend in background Blender, gun + Doomguy's gloves, one
  static pose. Our cube models keep their colours on the faces (corner colour layer `cubekit_view`) with no UV map and
  empty atlas images, so the script writes its own palette PNG (one pixel per colour, every face pointing at the middle
  of its pixel). The MD3 writer is ashes-2063-weapons/kit/gz_md3.py; surfaces raised to 60,000 vertices because GZDoom
  takes at most 32 surfaces per model ("Invalid MD3 Surface 32 in Rifle" on the first launch). VR placement copies the
  Ashes revolver as Tefa tuned it: hand space, 100 units per metre, the grip (the middle of the right glove) 0.20 m
  ahead of and 0.16 m above the model origin.
- Mapping: pistol -> `BrutalPistol` (PIST, PISR, PISS, 2ISR), shotgun -> `Shot_Gun` (SHTA, SHTN, SHT8), machine gun ->
  `Rifle` (RIFG, RIFF, RIFR, RIFZ, RI2G, 2IFR); every letter A-Z of those sprites shows the gun (no animation yet).
- Sizes: pistol 114,650 triangles (6 surfaces), shotgun 244,030 (13), machine gun 203,928 (11).
- Output (never in git, all our own models): `D:/MEGA transfer/Game Files/brutal-doom-3d-guns/gzdoom/vr-test/`
  (`bd3dguns_vr_test.pk3` + the md3s, pngs and modeldefs).
- Launcher: `D:/Brutal Doom/Play Doom 1 - Brutal Doom VR (3D guns test).bat`: our GZDoomVR "Tefa engine" from Ashes
  (`C:/NonSteam/Ashes 2063 VR/gzdoomvr-tefa`, SteamVR, vr_mode 10), DOOM.WAD from Steam's Ultimate Doom,
  brutal22test6.pk3, our pk3, settings `D:/Brutal Doom/doom-vr.ini` (copied from the Ashes VR 3D test settings, music
  volume 0), E1M1, skill 3, the shotgun and rifle given.

## Checked

Flat launch (a throwaway copy of the settings, vr_mode 0): E1M1 loads with Brutal Doom v22 and the three models, no
model errors `[verified-live 2026-10-19, n=1, flat]`. The window capture showed the pistol in view. Not seen in the
headset yet: the placement in the hand, the size, Brutal Doom's 2D overlay layers (hands, flashes) floating beside the
models, how heavy the 244k-triangle shotgun is in VR.
