# Brutal Doom: 3D weapons (work in progress)

New 3D gun models, with Doomguy's armoured gloves, for **Brutal Doom** (v22 test 6) in **Doom** and
**Doom II**, built in Blender from scratch and lit so they catch the light. The long-term aim is to hold
them in **VR** (GZDoom VR), the way our [Ashes 2063 weapons](https://github.com/TefMeister/ashes-2063-weapons)
already are.

> ⚠️ **Disclaimer.** This is an unofficial, non-commercial fan project. It is **not** made by or affiliated
> with id Software, Bethesda, or Sergeant_Mark_IV and the Brutal Doom team, and it is **not** a playable mod
> yet. **No original game files, sprites, sounds or other assets are included.** Every model here is made
> from scratch, using the games only as a visual reference. You need your own copy of Doom or Doom II, and
> Brutal Doom from its official page.
>
> ⚠️ **Caution.** Once this is used in VR it will be unfinished work and **may cause severe motion sickness
> and discomfort**. Take breaks and stop if you feel unwell.

## What's here

| Folder | What it holds |
| --- | --- |
| [`sheet/`](sheet/) | [`WEAPONS.md`](sheet/WEAPONS.md): every Brutal Doom weapon's numbers (how fast it fires, damage, magazine, reload, raise and lower times, and when each sound plays), read from the mod's own files. `weapons.json` has every frame and sound with its exact time, for timing our animations. |
| [`tools/`](tools/) | the scripts that read those numbers (`weapon_sheet.py`, `doom_states.py`) and lay out picture sheets to model from (`ref_sheets.py`) |
| [`NOTES.md`](NOTES.md) | the plan, decisions and open questions |

## The first two guns

- **Shotgun:** the Brutal Doom pump shotgun, hands placed the way the Ashes 2063 shotgun's are, wearing
  Doomguy's gloves.
- **Pistol:** in the look of a beefed-up Beretta 92F.

## Credits

- **Sergeant_Mark_IV** and the Brutal Doom team, for Brutal Doom, whose weapon timings this follows.
- **id Software**, for Doom and Doom II.
- **hh79**, for GZDoomVR, and the **GZDoom** team (Graf Zahl and contributors).

If you should be credited here and are not, or you hold the rights to anything used and want it changed or
removed, please open an issue and we will fix it as soon as possible.
