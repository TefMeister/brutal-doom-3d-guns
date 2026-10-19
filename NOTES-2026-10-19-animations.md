# 2026-10-19: the first animations (shots, the shotgun pump, the first pick-up)

Tefa, 2026-10-19: *"doom games, please animate the shooting animations, pump after each shotgun shot, but not the
reloads, we'll not include reloading guns, only the initial weapon pick up animation we must animate too"*, then
*"please do all the animations without me and we'll look at them all together later and tweak what we have to then"*.
So this was built alone (the stated exception to doing Blender work together) as a first pass for review.

## What moves

| Gun | On each shot | First pick-up (Brutal Doom's FirstSelectAnimation / Tacticalselect) | Raise |
| --- | --- | --- | --- |
| Shotgun | kick back and muzzle up over 5 frames, then the pump goes back and forward with the left glove on it (Brutal Doom's own frames: Pump1 sound at the back, Pump2 at home) | raised from muzzle-down, then one slow pump | SHTA M L K J |
| Pistol | kick and the slide back, then home | raised, tipped up and turned in to look it over, the side, the front, racked, lowered | PISS A B C |
| Machine gun | a short kick per round (RIFF A B, D) | raised canted on its side, the charging handle pulled and let go, turned back level | RIFG I H G F |

Not animated, on purpose: reloads (the launcher sets Brutal Doom's own `bd_noreloading 1`), the magazine checks inside
Brutal Doom's first pick-up frames (left out because they are reload moves), zoomed fire (SHT8), dual wield, purist
sprites. The machine gun's left hand does not go to the charging handle yet (a hand pose, for together).

## How

- `tools/gz_anim.py`: the poses (back, up, pitch, roll, yaw about the grip; plus a moving part's travel along its
  axis) and which Brutal Doom sprite frame shows which pose, read from v22 test 6's DECORATE and sprite pictures.
  Every number is a first guess to tweak together.
- `tools/gz_vr_export.py`: now writes each gun as two MD3s drawn together, the body (frame, right glove, ...) and the
  moving part (pump + left glove / slide / charging handle), each with one frame per distinct pose it takes, and a
  MODELDEF with a FrameIndex per sprite frame per model. Stepped (NOINTERPOLATION), exactly on Brutal Doom's tics.
  Corner maths in numpy (the plain Python version took over 20 minutes for the shotgun).
- `tools/gz_anim_preview.py`: keys the same animations onto Blender's timeline (one Blender frame per tic, 35 fps,
  markers fire / first_pickup / raise) in a SEPARATE `<gun>_anim_preview.blend` next to the gun's blend in the MEGA
  folder, for looking at them together. The gun's own blend is never saved over.
- `tools/gz_anim_shots.py`: renders chosen frames of a preview from the side and from behind, to check poses without
  opening Blender.

## Where

- Builds (never in git): `D:/MEGA transfer/Game Files/brutal-doom-3d-guns/gzdoom/vr-test-anim/` (the static first
  test kept in `gzdoom/archive/2026-10-19-static-first-test/`).
- Launcher: `D:/Brutal Doom/Play Doom 1 - Brutal Doom VR (3D guns animated test).bat` (the static one is unchanged).
