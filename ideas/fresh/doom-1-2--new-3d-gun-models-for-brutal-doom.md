# New 3D gun models for Brutal Doom

Order: 10000
From: the ideas repo, `games/doom-1-2.md` (<https://github.com/TefMeister/mod-ideas/blob/main/games/doom-1-2.md>), copied 2026-10-19

`[considered]` · `[looks doable]` — *the size of the job is settled now: it is the bigger of the two*

> "make new gun models for doom 1 and 2 brutal doom mod, latest version of brutal doom"

> "3d guns that catch light, the ones available are for an older version of brutal doom and are
> outdated" — 2026-09-14, answering the question that used to sit below

Replace the weapons you see and hold in **Brutal Doom** — the current version of it — with our own.

Verbatim record: [`inbox/2026-09-11c-doom-new-gun-models-for-brutal-doom.md`](../inbox/2026-09-11c-doom-new-gun-models-for-brutal-doom.md)

**⭐ This is the first idea in the repo that builds on somebody else's mod**, and that is genuinely
good news rather than a complication. Brutal Doom already does the hard part — the recoil, the
timings, the feel — so nothing has to be invented for the guns to *work*. We are changing what they
look like, and the thing that carries the change is art, not code.

It also means the base can move underneath us: Brutal Doom keeps being updated, so "latest version"
is a moving target. Not a problem, just something to pin down at the start rather than discover
later.

**✅ Answered 2026-09-14: real 3D guns, not drawn art.** (Answered, not `[settled]` — you have said
*which* it should be, not that we are building it.) Guns that are built and lit and catch the
light as you move — not flat hand-drawn pictures in the style Brutal Doom uses today. This is the
more expensive of the two options and it was chosen knowingly.

**What it'd take:** every gun has to be modelled and lit before it can appear at all, and it will
look different *in kind* from everything else on screen — which is either the appeal or the
problem, and you have said it is the appeal. Once a gun exists, re-posing it for every animation
frame is far less work than drawing each frame by hand, so the cost is front-loaded rather than
spread out. Still an **art** project with a small amount of plumbing: no reverse engineering, no
debugger, no programming worth the name. That remains the reason this one could actually be
finished.

**⭐ The other half of the answer changes the target, and it is the more useful half.** Your words:
*"the ones available are for an older version of brutal doom and are outdated."* So 3D weapon packs
for Brutal Doom **already exist** — they are just built against a version we don't play. That makes
the first job a look rather than a build:

- **Find out what the outdated packs actually break on.** A pack failing on a newer Brutal Doom is
  sometimes a small fix (renamed states, changed weapon classes) and sometimes a rewrite. Nobody
  here has checked which, and the gap between those two answers is the whole size of the project.
- **Then decide** whether this is *making* guns or *bringing existing ones forward* — a genuinely
  different project, and possibly a far shorter one.

⚠️ **Not checked.** The above is reasoning about how GZDoom mods usually break, not a look at any
real pack. It is a cheap thing to find out and it should happen before anyone models anything.

⚠️ **Worth thirty minutes anyway:** weapon replacement packs for Brutal Doom are one of the most
common things in the entire Doom community. Not a reason to stop — our version being *ours* is the
point — but seeing what already exists is free and tells you what you like.

---
