# 2026-10-29 — a working GZDoom VR scope, from another modder's Brutal Doom pack

Tefa asked another modder working on Brutal Doom in VR how they got their scope working, and was sent their pack,
`BD22_VR-Reloaded_2.0.3h.pk3` (38 MB, 790 files). It was opened read-only (a pk3 is a zip) and nothing was run.

## What it is

Not a single scope or a single gun: the whole pack, **"BD22Q"**, an addon that loads after Brutal Doom v22
(`doom2.wad -> brutal22test6.pk3 -> BD_VoxelPack.pk3 -> this`) and adds VR hands, hand reloading for 23 guns, melee,
ballistics, brass, and **a working scope**. It targets stock **QuestZDoom 17.3** (the Quest standalone GZDoom), with no
engine changes. `[reported]` (its README).

## How the scope works (its own comments, `zscript/rsq/scope.zs`, `zscript/rsq/scope_real.zs`)

- **REAL mode (3x):** an invisible camera actor is parked at the scope's lens each tic, pointing down the bore;
  `TexMan.SetCameraToTexture` renders it into a camera texture (`ANIMDEFS.rsq`: `cameratexture RSQSCOPE 256 256`), and
  the scope GLASS surface's skin is swapped to that texture (`A_ChangeModel` with `CMDL_USESURFACESKIN`). So the glass
  must be its OWN surface in the MD3 (the Railgun's mesh already had one; they carved one into the Ruger/XM21).
- One extra mono scene render per frame while a scoped gun is held (a real scope is monocular anyway); the picture is
  one frame late. Alt fire switches it off to save the cost.
- **DOT mode (1x):** a collimated red dot, placed each rendered frame (in `ModifyBobLayer3D`, per frame not per tic)
  where the eye-to-dot ray runs parallel to the bore, so it does not slide off the target when the head moves.
- Per gun it needs four measured numbers in one table (`RSQ_ScopeTable`: lens, axis, up, radius, glass surface,
  magnification). It borrows the pack's own VR hand transform (`zscript/rsvr/vrhand.zs`).

## What it means for us `[not checked]`

- This is the method our scopes can use: a camera texture on a separate glass surface. Our guns are already built
  in separate parts (2026-10-23 rule), so the scope glass can be its own object/surface.
- NOT checked: whether it runs on the PC GZDoom VR build we use (it targets QuestZDoom); what licence covers the
  pack's own code (its README credits Ermac's hands as MIT and Dakka as WTFPL, but states no licence for the rest).
  Ask the author before lifting code; the idea itself is ours to use.
- Credits it names: Sergeant_Mark_IV (Brutal Doom), Ermac (hands, Force Unleashed pack, DoomXR), TeamBeef,
  Emawind (QuestZDoom), ijon (Dakka). The pack author's own handle is not in the README.
