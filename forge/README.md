# Brutal Doom weapons, forge cube set (first pass, 2026-10-19)

The rest of Brutal Doom's weapons, built in mixed cube sizes with `blender-cubekit`'s forge (`docs/FORGE.md`
there). Free designs: Tefa asked for them to be *"as creative and bold as you want"*, so they keep the house look of
the three guns already shaped together (dark gun metal, worn dark-red paint, white UAC marks, green sights) and push
it further with hazard stripes, skulls, glowing parts and heavy armour.

The shotgun, pistol and machine gun built with Tefa in `shotgun/`, `pistol/` and `machinegun/` are not touched.

The `.blend` files are in the MEGA transfer folder, `Game Files/brutal-doom-3d-guns/3D blender/forge-2026-10-19/`
(not on GitHub). One preview sheet per weapon is in `renders/`.

| File | Weapon |
| --- | --- |
| `axe.py` | Axe |
| `chainsaw.py` | Chainsaw |
| `revolver.py` | Revolver |
| `smg.py` | SMG |
| `super_shotgun.py` | Super Shotgun |
| `assault_shotgun.py` | Assault Shotgun |
| `assault_rifle.py` | Rifle |
| `mp40.py` | MP40 |
| `mg42.py` | MG42 |
| `minigun.py` | Minigun |
| `sniper_rifle.py` | Sniper rifle |
| `grenade_launcher.py` | Grenade launcher |
| `hand_grenade.py` | Hand grenade |
| `rocket_launcher.py` | Rocket launcher |
| `incendiary_launcher.py` | Incendiary launcher (M202) |
| `revenant_launcher.py` | Hellish missile launcher |
| `plasma_rifle.py` | Plasma rifle |
| `railgun.py` | Railgun |
| `flamethrower.py` | Flamethrower |
| `flame_cannon.py` | Flame cannon |
| `bfg9000.py` | BFG 9000 |
| `bfg10k.py` | BFG 10K |
| `unmaker.py` | Unmaker |
| `devastator.py` | Devastator |
| `nuke_launcher.py` | Nuke launcher |
| `dragonslayer.py` | Dragonslayer |

The list is every hand-held weapon in `sheet/WEAPONS.md` (Brutal Doom v22 test 6), leaving out vehicles, monster
morphs, shields and the two-gun versions (they reuse the single gun).

**Rebuild** one or all (Blender 5.2, no window):

```
python ../../blender-cubekit/forge_make.py "<blend folder>" renders axe.py bfg9000.py
```

**Still to do:** Doomguy's gloves on each gun, animations, the light and glow work, and the game export (the
exporter cannot read forge models yet).
