# Stop-motion gun movement that does not look doubled

Order: 10002
From: the ideas repo, `games/doom-1-2.md` (<https://github.com/TefMeister/mod-ideas/blob/main/games/doom-1-2.md>), copied 2026-10-19

`[raw]` · `[looks doable]` — *not checked in the headset yet*

> "is there a way to keep the gun always on the screen, but add the frameyness to it by only changing the way it is
> pointing every like 20 or 10 frames per second ... having the gun only jump around 10 fps is making it look doubled
> ... if we can get it to work, have the gun move in less frames so it looks natural, it would be an epic feature"

The gun in your hand moves in little stop-motion steps, like the animations do, without the doubled, jittery look an
earlier try had. Also for Ashes 2063: same engine.

Verbatim record: [`inbox/2026-10-18-doom-stepped-aim-without-doubling.md`](../inbox/2026-10-18-doom-stepped-aim-without-doubling.md)

**Why the earlier try looked doubled:** when your eyes follow something that jumps, they see it in two places at once,
and the bigger each jump, the wider the gap. At 10 steps a second a normal swing of the arm is a jump of several
degrees each time. So the fix is to keep every jump small, not to step less often.

**What it'd take:** the gun's place always follows the hand exactly (no more teleporting). Only its pointing is held,
and it snaps on as soon as the hand has turned past a small angle, a degree or so. Slow, careful aiming then looks
stop-motion; a fast swing becomes many tiny steps that read as smooth, so it never looks doubled. The step size and
how long a pose is held become two named settings to tune in the headset. A small piece of game code in the weapon,
the same kind as the swinging-strap idea.

⚠️ **Not checked.** Whether a held pointing feels right in the hand, or feels like lag, only the headset can say.

---

_Other categories appear as they arrive — gameplay, visuals, audio, VR, level design, UI, controls, enemies, performance. Nothing is missing; none of them have been needed yet._

**To add one:** `[doom] your idea` — anywhere, any time.

Chosen by Tefa: 2026-10-29
