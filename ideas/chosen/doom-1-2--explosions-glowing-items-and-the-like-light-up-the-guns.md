# Explosions, glowing items and the like light up the guns

Order: 10001
From: the ideas repo, `games/doom-1-2.md` (<https://github.com/TefMeister/mod-ideas/blob/main/games/doom-1-2.md>), copied 2026-10-19

`[raw]` · `[looks doable]` — *not checked yet*

> "the light is actually showing up on the guns! we now need to get other parts of the game to emit light, like
> explosions, glowing health bottles and so on"

The 3D guns already catch the light in the headset (first look, 2026-10-19). Next: explosions, fireballs, muzzle
flashes, glowing health and armour bonuses, lamps and so on give off light too, so it plays across the guns and the
gloves as you walk past or fight.

Verbatim record: [`inbox/2026-10-19-doom-lights-from-explosions-and-items.md`](../inbox/2026-10-19-doom-lights-from-explosions-and-items.md)

**What it'd take:** GZDoom already has these lights ("dynamic lights", defined per thing in GLDEFS). Its own
`lights.pk3` (and `brightmaps.pk3` for glowing pixels) sit in our engine folder but the first test launcher does not
load them; adding them is the first step, then filling the gaps for Brutal Doom's own effects with our own GLDEFS.

⚠️ **Not checked.** Whether the engine's lights land on the guns the way the room light does, and what it costs in
frame rate in VR, only a run can say.

---

Chosen by Tefa: 2026-10-29
