# Brutal Doom weapons: the numbers

Read from the mod's own weapon files by `tools/weapon_sheet.py`, playing each one forward at 35 tics a second on the plain path (a normal, not Tactical, player class; nobody pressing anything). All of it is `[inferred-static]` until timed in the game. Damage is bullets x damage per bullet as written; Brutal Doom's bullet puffs can add more on hit. Every frame and sound with its exact tic is in `weapons.json`.

## AmmoDroper  ($TAGBD_AMMODROPPER)

- Ammo: - (carry up to None); no magazine
- Sprites: ADRO

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 1 | 0.03 | - | Plasma/BeepQuiet @0 | ready (ready) |
| Reload from empty | 5 | 0.14 | - | Plasma/BeepQuiet @0 | ready (ready) |
| Reload with one round used | 5 | 0.14 | - | Plasma/BeepQuiet @0 | ready (ready) |
| Raise (select) | 6 | 0.17 | - | Plasma/Beep @6 | ready (ready) |
| Lower (deselect) | 11 | 0.31 | - | - | rests here for good |
| Alt fire / aim | 5 | 0.14 | - | Plasma/Beep @0 | ready (ready) |

Sound files: `Plasma/Beep` sounds\COMBAT\WEAPONS\Plasmagun\BEP.ogg, `Plasma/BeepQuiet` sounds\COMBAT\WEAPONS\Plasmagun\BEPquiet.ogg

## ArtilleryTankGun  (Artillery tank)

- Ammo: heavymachinegunammo (carry up to 2000); helicopterrocketammo holds 100
- Sprites: TNHD, TNLH

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 2505 | 71.57 | AutoCannonProjectile; AutoCannonProjectile; AutoCannonProjectile; AutoCannonProjectile | ACANO1 @1, FARCAN1 @1, ACANO1 @3, FARCAN1 @3, ACANO1 @5, FARCAN1 @5, ACANO1 @7, FARCAN1 @7 | cut short |
| Raise (select) | 2 | 0.06 | - | - | ready (ready) |
| Lower (deselect) | 6667 | 190.49 | - | - | cut short |
| Alt fire / aim | 2529 | 72.26 | TankMissile | MISFAR @0 | cut short |

Sound files: `ACANO1` sounds\VEHICLES\ACANO1.ogg, `FARCAN1` sounds\COMBAT\WEAPONS\DISTANTSOUNDS\FARCAN1.ogg, `MISFAR` MISFAR

## AssaultShotgun  ($TAGBD_ASG)

- Ammo: ammoshell (carry up to 50); assaultshotgunammo holds 20
- Sprites: 2SAR, USAR, USAS

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 6 | 0.17 | 9 x 11 | ASG/Fire @0 | ready (ready) |
| Reload from empty | 87 | 2.49 | - | ASG/Reload1 @12, ASG/Reload2 @35, asg/bolt1 @59, asg/bolt2 @70 | ready (ready3) |
| Reload with one round used | 56 | 1.6 | - | ASG/Reload1 @12, ASG/Reload2 @35, USASPUL1 @54 | ready (ready3) |
| Raise (select) | 5 | 0.14 | - | ASG/Draw @1 | ready (ready) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |
| Alt fire / aim | 8 | 0.23 | - | ads/in @0 | ready (ready2) |

Sound files: `ASG/Draw` sounds\COMBAT\WEAPONS\AssaultShotgun\AA12R1.ogg, `ASG/Fire` sounds\COMBAT\WEAPONS\AssaultShotgun\AA12F.ogg, `ASG/Reload1` sounds\COMBAT\WEAPONS\AssaultShotgun\usasout.ogg, `ASG/Reload2` sounds\COMBAT\WEAPONS\AssaultShotgun\USASIN.ogg, `USASPUL1` ?, `ads/in` sounds\COMBAT\WEAPONS\ADSIN.ogg, `asg/bolt1` sounds\COMBAT\WEAPONS\AssaultShotgun\ASGBOLT1.ogg, `asg/bolt2` sounds\COMBAT\WEAPONS\AssaultShotgun\ASGBOLT2.ogg

## attackhelicopterGun  (Attack Helicopter)

- Ammo: heavymachinegunammo (carry up to 2000); helicopterrocketammo holds 100
- Sprites: HELH

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 1 | 0.03 | - | - | ready (ready2) |
| Raise (select) | 9 | 0.26 | - | - | ready (ready2) |
| Lower (deselect) | 10000 | 285.71 | - | - | cut short |

Sound files: -

## BFG10k  ($TAGBD_BFG10K)

- Ammo: - (carry up to None); no magazine
- Sprites: BG2G

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 67 | 1.91 | GreenFlareSpawn; BFG10K_Ball | BFG10K/Charge @0, BFG10K/Fire @26, BFG10K/Stop @34 | ready (ready) |
| Raise (select) | 5 | 0.14 | - | BFG/Draw @1 | ready (ready) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |

Sound files: `BFG/Draw` sounds\COMBAT\WEAPONS\BFG\BFGREADY.ogg, `BFG10K/Charge` sounds\COMBAT\WEAPONS\BFG10K\10KSTART.ogg, `BFG10K/Fire` sounds\COMBAT\WEAPONS\BFG10K\10KFIRE.ogg, `BFG10K/Stop` sounds\COMBAT\WEAPONS\BFG10K\10KSTOP.ogg

## BIG_FUCKING_GUN  ($TAGBD_BFG9000)

- Ammo: - (carry up to None); no magazine
- Sprites: BFGA, BFGN, BFGS

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 43 | 1.23 | GreenFlareSpawn; GreenFlareSpawn; GreenFlareSpawn; GreenFlareSpawn; Alerter; BFGBall | BFG/Charge @0, BFG/Fire @30 | ready (ready3) |
| Raise (select) | 5 | 0.14 | - | BFG/Draw @1 | ready (ready3) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |

Sound files: `BFG/Charge` sounds\COMBAT\WEAPONS\BFG\BFGCHARG.ogg, `BFG/Draw` sounds\COMBAT\WEAPONS\BFG\BFGREADY.ogg, `BFG/Fire` sounds\COMBAT\WEAPONS\BFG\BFGFIRE.ogg

## BikeHUD  (Bike)

- Ammo: - (carry up to None); shell holds None
- Sprites: BKHL, BKHU

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 1 | 0.03 | - | - | ready (ready) |
| Raise (select) | 1 | 0.03 | - | - | ready (ready) |
| Lower (deselect) | 5000 | 142.86 | - | - | cut short |

Sound files: -

## BrutalAxe  ($TAGBD_AXE)

- Ammo: - (carry up to None); no magazine
- Sprites: AXEA, AXEG

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 25 | 0.71 | saw "", "", 3, "AxePuffs", 0, 44, 0, 0; AxeAttackNoDecal; AxeAttack | Axe/Swing @6 | ready (ready) |
| Reload from empty | 4 | 0.11 | - | - | ready (ready) |
| Reload with one round used | 4 | 0.11 | - | - | ready (ready) |
| Raise (select) | 5 | 0.14 | - | Axe/Draw @1 | ready (ready3) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |
| Alt fire / aim | 28 | 0.8 | saw "", "", 3, "AxePuffs", 0, 44, 0, 0; AltAxeAttack; AltAxeAttackNoDecal; AltAxeAttackNoDecal | Axe/AltSwing @7 | ready (ready) |

Sound files: `Axe/AltSwing` sounds\COMBAT\WEAPONS\Axe\AXSWING2.ogg, `Axe/Draw` sounds\COMBAT\WEAPONS\Axe\AXEDRAW.ogg, `Axe/Swing` sounds\COMBAT\WEAPONS\Axe\AXSWING1.ogg

## BrutalPistol  ($TAGBD_PISTOL)

- Ammo: clip1 (carry up to 100); bdpistolammo holds 16
- Sprites: 2ISR, PISR, PISS, PIST

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 11 | 0.31 | -1 x 14 | FARSHT @0, Pistol/Fire @0 | ready (ready) |
| Reload from empty | 36 | 1.03 | - | Pistol/Reload1 @0, Pistol/Reload2 @19, pistol/slide2 @24 | ready (ready) |
| Reload with one round used | 32 | 0.91 | - | Pistol/Reload1 @0, Pistol/Reload2 @19 | ready (ready) |
| Raise (select) | 5 | 0.14 | - | Pistol/Draw @2 | ready (ready) |
| Lower (deselect) | 4 | 0.11 | - | - | wait |
| Alt fire / aim | 2 | 0.06 | - | Weapon/Empty @0 | ready (ready3) |

Sound files: `FARSHT` sounds\COMBAT\WEAPONS\DISTANTSOUNDS\FARSHT.ogg, `Pistol/Draw` sounds\COMBAT\WEAPONS\PISTOL\PISTUP.ogg, `Pistol/Fire` sounds\COMBAT\WEAPONS\PISTOL\PFIRE.ogg, `Pistol/Reload1` sounds\COMBAT\WEAPONS\PISTOL\MG_OUT.ogg, `Pistol/Reload2` sounds\COMBAT\WEAPONS\PISTOL\PISR.ogg, `Weapon/Empty` sounds\COMBAT\WEAPONS\DRYFIRE.ogg, `pistol/slide2` sounds\COMBAT\WEAPONS\PISTOL\PISSL.ogg

## BrutalSMG  ($TAGBD_SMG)

- Ammo: clip1 (carry up to 100); bdsmgammo holds 41
- Sprites: SMGF, SMGR, SMGS, SMGZ

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 3 | 0.09 | 1 x 12 | FARSHT @0, SMG/Fire @0 | ready (ready3) |
| Reload from empty | 42 | 1.2 | - | SMG/Reload1 @10, SMG/Reload2 @30 | ready (ready) |
| Reload with one round used | 42 | 1.2 | - | SMG/Reload1 @10, SMG/Reload2 @30 | ready (ready) |
| Raise (select) | 5 | 0.14 | - | Rifle/Select @1 | ready (ready3) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |
| Alt fire / aim | 8 | 0.23 | - | ads/in @0 | ready (ready2) |

Sound files: `FARSHT` sounds\COMBAT\WEAPONS\DISTANTSOUNDS\FARSHT.ogg, `Rifle/Select` sounds\COMBAT\WEAPONS\Rifle\CLIPIN.ogg, `SMG/Fire` sounds\COMBAT\WEAPONS\SMG\SMGFIRE.ogg, `SMG/Reload1` sounds\COMBAT\WEAPONS\SMG\SMGREL1.ogg, `SMG/Reload2` sounds\COMBAT\WEAPONS\SMG\SMGREL2.ogg, `ads/in` sounds\COMBAT\WEAPONS\ADSIN.ogg

## BrutalWeapon  ($TAGBD_DEFAULT)

- Ammo: - (carry up to None); no magazine
- Sprites: -

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |

Sound files: -

## CguyShield  (CguyShield.dec)

- Ammo: bdpistolammo (carry up to 16); meatammo holds 100
- Sprites: GRZ4, PI3F, PI3G, THRW

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 4 | 0.11 | YellowFlareSpawn | Pistol/Fire @1 | ready (ready) |
| Raise (select) | 2 | 0.06 | - | - | ready (ready) |
| Lower (deselect) | 2 | 0.06 | - | - | ready (ready) |
| Alt fire / aim | 27 | 0.77 | ThrowedChaingunguy | skeleton/swing @12 | ready (ready) |

Sound files: `Pistol/Fire` sounds\COMBAT\WEAPONS\PISTOL\PFIRE.ogg, `skeleton/swing` ?

## Chain_saw  ($TAGBD_SAW)

- Ammo: - (carry up to None); no magazine
- Sprites: SAWF, SAWG, SAWS

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 25 | 0.71 | saw "", "", 1, "SSawPuff2", 0, 120, 28, 0; saw "", "", 1, "SSawPuff2", 0, 120, 28, 0; saw "", "", 1, "SSawPuff2", 0, 120, 28, 0; SawDamageHorizontal2; SawDamageHorizontal; SawDamageHorizontal2; SawDamageHorizontal2 | Chainsaw/Draw @7 | ready (ready) |
| Reload from empty | 22 | 0.63 | - | Chainsaw/Zip @5, Chainsaw/Draw @16 | ready (ready) |
| Reload with one round used | 22 | 0.63 | - | Chainsaw/Zip @5, Chainsaw/Draw @16 | ready (ready) |
| Raise (select) | 22 | 0.63 | - | Chainsaw/Zip @5, Chainsaw/Draw @16 | ready (ready) |
| Lower (deselect) | 4 | 0.11 | - | - | wait |
| Alt fire / aim | 13 | 0.37 | custompunch 7, true, 0, "SSawPuff3"; custompunch 7, true, 0, "SSawPuff3"; custompunch 7, true, 0, "SSawPuff3"; custompunch 7, true, 0, "SSawPuff3" | - | ready (ready) |

Sound files: `Chainsaw/Draw` sounds\COMBAT\WEAPONS\Chainsaw\CSAWDRAW.ogg, `Chainsaw/Zip` sounds\COMBAT\WEAPONS\Chainsaw\DSSAWZIP.ogg

## D4BaronHUD  (Baron morph)

- Ammo: - (carry up to None); no magazine
- Sprites: HBRF, HBRN, HBRS

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 17 | 0.49 | GreenPlasmaBallPlayerTransformed | - | ready (ready) |
| Raise (select) | 4 | 0.11 | - | baron/sight @1 | ready (ready) |
| Lower (deselect) | 14418 | 411.94 | - | - | cut short |
| Alt fire / aim | 19 | 0.54 | BaronAttackOnBarrel; BaronAttackOnBarrel; BaronAttack; BaronAttack | Melee/SwingStrong @7 | ready (ready) |

Sound files: `Melee/SwingStrong` sounds\COMBAT\WEAPONS\MELEE\DSSWING.ogg, `baron/sight` ?

## D4RevenantHUD  (Revenant morph)

- Ammo: - (carry up to None); no magazine
- Sprites: RVCG

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 7 | 0.2 | Alerter; revenantseekermissiles2 | Incendiary/Fire @0 | ready (ready) |
| Alt fire / aim | 7 | 0.2 | Alerter; revenantseekermissiles2 | Incendiary/Fire @0 | ready (ready) |

Sound files: `Incendiary/Fire` sounds\COMBAT\WEAPONS\RocketLauncher\RLANSHOT.ogg

## Devastator  ($TAGBD_DEVASTATOR)

- Ammo: - (carry up to None); no magazine
- Sprites: DEVA

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 9 | 0.26 | DEvastatorMissile; DEvastatorMissile | Devastator/fire @0 | ready (ready) |
| Raise (select) | 5 | 0.14 | - | Devastator/select @1 | ready (ready) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |
| Alt fire / aim | 9 | 0.26 | DEvastatorMissile; DEvastatorMissile | Devastator/fire @0 | ready (ready) |

Sound files: `Devastator/fire` sounds\COMBAT\WEAPONS\Devastator\DEVAFIRE.ogg, `Devastator/select` sounds\COMBAT\WEAPONS\Devastator\DEVASEL.ogg

## DSweap  (Dragonslayer)

- Ammo: - (carry up to None); no magazine
- Sprites: DSLA, DSLC

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 37 | 1.06 | DSAttack; DSAttack2; DSAttack2; DSAttack2; DSAttack; DSAttack; DSAttack; DSAttack; DSAttack; DSAttack | Melee/SwingStrong @5 | ready (ready) |
| Raise (select) | 7 | 0.2 | - | - | ready (ready) |
| Lower (deselect) | 20000 | 571.43 | - | - | cut short |

Sound files: `Melee/SwingStrong` sounds\COMBAT\WEAPONS\MELEE\DSSWING.ogg

## DualFlameCannon  ($TAGBD_DUALFLAMECANNON)

- Ammo: - (carry up to None); no magazine
- Sprites: DUFL

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 0 | 0.0 | - | - | goto noammo (not followed) |
| Reload from empty | 1 | 0.03 | - | - | ready (ready3) |
| Reload with one round used | 1 | 0.03 | - | - | ready (ready3) |
| Raise (select) | 5 | 0.14 | - | Flamer/select @1 | ready (ready) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |
| Alt fire / aim | 0 | 0.0 | - | - | goto noammo (not followed) |

Sound files: `Flamer/select` sounds\COMBAT\WEAPONS\Flamethrower\Flamer5.ogg

## DualMP40  ($TAGBD_DUALMP40)

- Ammo: mauser9mm (carry up to 160); dualmp40ammo holds 64
- Sprites: 2P4R, 3P4R, 4P4R, 5P4R, MP42

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 4 | 0.11 | -1 x 18 | weapons/lowammo @0, FARSHT @0, MP40/Fire @0 | ready (ready3) |
| Reload from empty | 137 | 3.91 | - | Weapon/Empty @14, MP40/Reload1 @25, MP40/Reload2 @48, Weapon/Empty @78, MP40/Reload1 @89, MP40/Reload2 @111 | ready (ready) |
| Reload with one round used | 137 | 3.91 | - | Weapon/Empty @14, MP40/Reload1 @25, MP40/Reload2 @48, Weapon/Empty @78, MP40/Reload1 @89, MP40/Reload2 @111 | ready (ready) |
| Raise (select) | 5 | 0.14 | - | MP40/Draw @1 | ready (ready3) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |

Sound files: `FARSHT` sounds\COMBAT\WEAPONS\DISTANTSOUNDS\FARSHT.ogg, `MP40/Draw` sounds\COMBAT\WEAPONS\MP40\MP40DRAW.ogg, `MP40/Fire` sounds\COMBAT\WEAPONS\MP40\GMP40.ogg, `MP40/Reload1` sounds\COMBAT\WEAPONS\MP40\MP401.ogg, `MP40/Reload2` sounds\COMBAT\WEAPONS\MP40\MP402.ogg, `Weapon/Empty` sounds\COMBAT\WEAPONS\DRYFIRE.ogg, `weapons/lowammo` sounds\COMBAT\MagClick.ogg

## DualPistols  ($TAGBD_DUALPISTOLS)

- Ammo: clip1 (carry up to 100); bddualpistolammo holds 32
- Sprites: 2I2R, 3ISR, 4ISR, 5ISR, PI2F, PI2G, PI2R

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 6 | 0.17 | YellowFlareSpawn; -1 x 14 | FARSHT @0, Pistol/Fire @0 | ready (ready) |
| Reload from empty | 84 | 2.4 | - | Pistol/Reload1 @6, Pistol/Reload2 @25, Pistol/Reload1 @37, Pistol/Reload2 @56, pistol/slide2 @73, pistol/slide2 @76 | ready (ready) |
| Reload with one round used | 71 | 2.03 | - | Pistol/Reload1 @6, Pistol/Reload2 @25, Pistol/Reload1 @37, Pistol/Reload2 @56 | ready (ready) |
| Raise (select) | 5 | 0.14 | - | Pistol/Draw @1 | ready (ready) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |
| Alt fire / aim | 2 | 0.06 | - | Weapon/Empty @0 | ready (ready3) |

Sound files: `FARSHT` sounds\COMBAT\WEAPONS\DISTANTSOUNDS\FARSHT.ogg, `Pistol/Draw` sounds\COMBAT\WEAPONS\PISTOL\PISTUP.ogg, `Pistol/Fire` sounds\COMBAT\WEAPONS\PISTOL\PFIRE.ogg, `Pistol/Reload1` sounds\COMBAT\WEAPONS\PISTOL\MG_OUT.ogg, `Pistol/Reload2` sounds\COMBAT\WEAPONS\PISTOL\PISR.ogg, `Weapon/Empty` sounds\COMBAT\WEAPONS\DRYFIRE.ogg, `pistol/slide2` sounds\COMBAT\WEAPONS\PISTOL\PISSL.ogg

## DualPlasmaRifles  ($TAGBD_DUALPLASMA)

- Ammo: ammocell (carry up to 300); doubleplasmaammo holds 100
- Sprites: 3UPR, DUPR, PRR1, PRR2, PRSR

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 1667 | 47.63 | PlasmaFlareSpawn; Plasma_Ball | Plasma/Fire @0 | cut short |
| Reload from empty | 120 | 3.43 | - | Plasma/Reload1 @12, Plasma/Reload2 @37, Plasma/Reload1 @64, Plasma/Reload2 @89 | ready (ready) |
| Reload with one round used | 120 | 3.43 | - | Plasma/Reload1 @12, Plasma/Reload2 @37, Plasma/Reload1 @64, Plasma/Reload2 @89 | ready (ready) |
| Raise (select) | 5 | 0.14 | - | PRSDRAW @1 | ready (ready) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |

Sound files: `PRSDRAW` ?, `Plasma/Fire` sounds\COMBAT\WEAPONS\Plasmagun\plsm9.ogg, `Plasma/Reload1` sounds\COMBAT\WEAPONS\Plasmagun\PLSREL1.ogg, `Plasma/Reload2` sounds\COMBAT\WEAPONS\Plasmagun\PLSREL2.ogg

## DualRifles  ($TAGBD_DUALRIFLES)

- Ammo: clip2 (carry up to 200); doublerifleammo holds 62
- Sprites: 3IFR, 4IFR, DURI, DURR, RIFR

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 3 | 0.09 | -1 x 20 | FARRIF @0, Rifle/Fire @0 | ready (ready3) |
| Reload from empty | 106 | 3.03 | - | Rifle/Reload1 @9, Rifle/Reload2 @28, Rifle/Reload1 @58, Rifle/Reload2 @77 | ready (ready) |
| Reload with one round used | 106 | 3.03 | - | Rifle/Reload1 @9, Rifle/Reload2 @28, Rifle/Reload1 @58, Rifle/Reload2 @77 | ready (ready) |
| Raise (select) | 5 | 0.14 | - | Rifle/Select @1 | ready (ready3) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |

Sound files: `FARRIF` sounds\COMBAT\WEAPONS\DISTANTSOUNDS\FARRIF.ogg, `Rifle/Fire` sounds\COMBAT\WEAPONS\Rifle\DSRIFLE.ogg, `Rifle/Reload1` sounds\COMBAT\WEAPONS\Rifle\RIFLER1.ogg, `Rifle/Reload2` sounds\COMBAT\WEAPONS\Rifle\RIFLER2.ogg, `Rifle/Select` sounds\COMBAT\WEAPONS\Rifle\CLIPIN.ogg

## DualSMG  ($TAGBD_DUALSMG)

- Ammo: clip1 (carry up to 100); bddualsmgammo holds 82
- Sprites: 3MGR, 4MGR, SM2F, SM2S, SMGR

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 3 | 0.09 | -1 x 12 | weapons/lowammo @0, FARSHT @0, SMG/Fire @0 | ready (ready3) |
| Reload from empty | 107 | 3.06 | - | SMG/Reload1 @19, SMG/Reload2 @39, SMG/Reload1 @66, SMG/Reload2 @86 | ready (ready) |
| Reload with one round used | 107 | 3.06 | - | SMG/Reload1 @19, SMG/Reload2 @39, SMG/Reload1 @66, SMG/Reload2 @86 | ready (ready) |
| Raise (select) | 5 | 0.14 | - | Rifle/Select @1 | ready (ready) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |

Sound files: `FARSHT` sounds\COMBAT\WEAPONS\DISTANTSOUNDS\FARSHT.ogg, `Rifle/Select` sounds\COMBAT\WEAPONS\Rifle\CLIPIN.ogg, `SMG/Fire` sounds\COMBAT\WEAPONS\SMG\SMGFIRE.ogg, `SMG/Reload1` sounds\COMBAT\WEAPONS\SMG\SMGREL1.ogg, `SMG/Reload2` sounds\COMBAT\WEAPONS\SMG\SMGREL2.ogg, `weapons/lowammo` sounds\COMBAT\MagClick.ogg

## EvilMarineShield  (EvilMarineShield.dec)

- Ammo: bdpistolammo (carry up to 16); meatammo holds 100
- Sprites: GRZ5, PI3F, PI3G, THRW

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 4 | 0.11 | YellowFlareSpawn | Pistol/Fire @1 | ready (ready) |
| Raise (select) | 2 | 0.06 | - | - | ready (ready) |
| Lower (deselect) | 2 | 0.06 | - | - | ready (ready) |
| Alt fire / aim | 27 | 0.77 | ThrowedEvilMarine | skeleton/swing @12 | ready (ready) |

Sound files: `Pistol/Fire` sounds\COMBAT\WEAPONS\PISTOL\PFIRE.ogg, `skeleton/swing` ?

## ExecutionWeapon  (ExecutionsWeap.dec)

- Ammo: - (carry up to None); no magazine
- Sprites: -

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 20000 | 571.43 | - | - | cut short |
| Raise (select) | 1 | 0.03 | - | - | wait |
| Lower (deselect) | 1 | 0.03 | - | - | wait |

Sound files: -

## FlameCannon  ($TAGBD_FLAMECANNON)

- Ammo: - (carry up to None); no magazine
- Sprites: FLMG

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 0 | 0.0 | - | - | goto noammo (not followed) |
| Reload from empty | 1 | 0.03 | - | - | ready (ready3) |
| Reload with one round used | 1 | 0.03 | - | - | ready (ready3) |
| Raise (select) | 5 | 0.14 | - | Flamer/select @1 | ready (ready) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |
| Alt fire / aim | 0 | 0.0 | - | - | goto noammo (not followed) |

Sound files: `Flamer/select` sounds\COMBAT\WEAPONS\Flamethrower\Flamer5.ogg

## Flamethrower2  ($TAGBD_FLAMETHROWER)

- Ammo: - (carry up to None); no magazine
- Sprites: FLMT

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 13 | 0.37 | FlamethrowerProjectileNew; FlamethrowerProjectileNew2; FlamethrowerProjectileNew3; FlamethrowerProjectileNew; FlamethrowerProjectileNew2; FlamethrowerProjectileNew3; FlamethrowerProjectileNew; FlamethrowerProjectileNew2; FlamethrowerProjectileNew3; FlamethrowerProjectileNew; FlamethrowerProjectileNew2; FlamethrowerProjectileNew3 | Flamer/loop @1, Flamer/idle @13, Flamer/stop @13 | ready (ready) |
| Reload from empty | 2500 | 71.43 | - | - | cut short |
| Reload with one round used | 2500 | 71.43 | - | - | cut short |
| Raise (select) | 5 | 0.14 | - | Flamer/select @1 | ready (ready) |
| Lower (deselect) | 1820 | 52.0 | - | - | cut short |

Sound files: `Flamer/idle` sounds\COMBAT\WEAPONS\Flamethrower\flamer4.ogg, `Flamer/loop` sounds\COMBAT\WEAPONS\Flamethrower\Flamer2.ogg, `Flamer/select` sounds\COMBAT\WEAPONS\Flamethrower\Flamer5.ogg, `Flamer/stop` sounds\COMBAT\WEAPONS\Flamethrower\Flamer1.ogg

## GrenadeLauncher  ($TAGBD_GL)

- Ammo: ammorocket (carry up to 50); glammo holds 1
- Sprites: GRL2, GRLN

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 55 | 1.57 | ShortGrenade2; RedFlareSpawn; GrenadeMissileBreaksGlass | GrenadeLauncher/Fire @0, GrenadeLauncher/Open @13, GrenadeLauncher/Load @28, GrenadeLauncher/Close @38 | ready (ready) |
| Reload from empty | 47 | 1.34 | - | GrenadeLauncher/Open @5, GrenadeLauncher/Load @20, GrenadeLauncher/Close @30 | ready (ready) |
| Reload with one round used | 47 | 1.34 | - | GrenadeLauncher/Open @5, GrenadeLauncher/Load @20, GrenadeLauncher/Close @30 | ready (ready) |
| Raise (select) | 9 | 0.26 | - | GrenadeLauncher/Close @3 | ready (ready) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |
| Alt fire / aim | 55 | 1.57 | GrenadeMissile; RedFlareSpawn; GrenadeMissileBreaksGlass | GrenadeLauncher/Fire @0, GrenadeLauncher/Open @13, GrenadeLauncher/Load @28, GrenadeLauncher/Close @38 | ready (ready) |

Sound files: `GrenadeLauncher/Close` sounds\COMBAT\WEAPONS\GrenadeLauncher\DSGRCLOS.ogg, `GrenadeLauncher/Fire` sounds\COMBAT\WEAPONS\GrenadeLauncher\DSGRFIRE.ogg, `GrenadeLauncher/Load` sounds\COMBAT\WEAPONS\GrenadeLauncher\DSGRLOAD.ogg, `GrenadeLauncher/Open` sounds\COMBAT\WEAPONS\GrenadeLauncher\DSGROPEN.ogg

## HandGrenades  ($TAGBD_GRENADE)

- Ammo: - (carry up to None); no magazine
- Sprites: GRTH

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 24 | 0.69 | - | Grenade/Pin @7, Grenade/Toss @15 | ready (ready) |
| Raise (select) | 1 | 0.03 | - | - | ready (ready) |
| Lower (deselect) | 1 | 0.03 | - | - | wait |
| Alt fire / aim | 24 | 0.69 | - | Grenade/Pin @7, Grenade/Toss @15 | ready (ready) |

Sound files: `Grenade/Pin` sounds\COMBAT\WEAPONS\Grenade\GRNPIN.ogg, `Grenade/Toss` sounds\COMBAT\WEAPONS\Grenade\GRNTOSS.ogg

## HeavyMachinegunHUD  (Heavy MG Turret)

- Ammo: - (carry up to None); no magazine
- Sprites: HMGH

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 3 | 0.09 | - | - | ready (ready) |
| Raise (select) | 9 | 0.26 | - | - | ready (ready) |
| Lower (deselect) | 20000 | 571.43 | - | - | cut short |

Sound files: -

## HellishMissileLauncher  ($TAGBD_REVMISSILE)

- Ammo: - (carry up to None); no magazine
- Sprites: RVCG

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 7 | 0.2 | Alerter; revenantseekermissiles2 | Incendiary/Fire @0 | ready (ready) |
| Raise (select) | 5 | 0.14 | - | RevLaunch/Draw @1 | ready (ready) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |
| Alt fire / aim | 7 | 0.2 | Alerter; revenantseekermissiles2 | Incendiary/Fire @0 | ready (ready) |

Sound files: `Incendiary/Fire` sounds\COMBAT\WEAPONS\RocketLauncher\RLANSHOT.ogg, `RevLaunch/Draw` sounds\COMBAT\WEAPONS\REVUP.ogg

## ImpShield  (ImpShield.dec)

- Ammo: bdpistolammo (carry up to 16); meatammo holds 100
- Sprites: GRZ3, PI3F, PI3G, THRW

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 4 | 0.11 | YellowFlareSpawn | Pistol/Fire @1 | ready (ready) |
| Raise (select) | 2 | 0.06 | - | - | ready (ready) |
| Lower (deselect) | 2 | 0.06 | - | - | ready (ready) |
| Alt fire / aim | 27 | 0.77 | ThrowedImp | skeleton/swing @12 | ready (ready) |

Sound files: `Pistol/Fire` sounds\COMBAT\WEAPONS\PISTOL\PFIRE.ogg, `skeleton/swing` ?

## IncendiaryLauncher  ($TAGBD_M202)

- Ammo: - (carry up to None); no magazine
- Sprites: M202

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 4 | 0.11 | IncendiaryRocket | Incendiary/Fire @0 | ready (ready3) |
| Raise (select) | 9 | 0.26 | - | - | ready (ready3) |
| Lower (deselect) | 4 | 0.11 | - | - | wait |

Sound files: `Incendiary/Fire` sounds\COMBAT\WEAPONS\RocketLauncher\RLANSHOT.ogg

## LedgeGrab  (LedgeGrab.dec)

- Ammo: - (carry up to None); no magazine
- Sprites: -

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 20000 | 571.43 | - | - | cut short |
| Raise (select) | 1 | 0.03 | - | - | wait |
| Lower (deselect) | 1 | 0.03 | - | - | wait |

Sound files: -

## MechGun  (Mech)

- Ammo: - (carry up to None); no magazine
- Sprites: MEKH

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 1 | 0.03 | - | - | ready (ready) |
| Raise (select) | 2 | 0.06 | - | - | ready (ready) |
| Lower (deselect) | 2500 | 71.43 | - | - | cut short |
| Alt fire / aim | 0 | 0.0 | - | - | ready (ready) |

Sound files: -

## Melee_Attacks  ($TAGBD_FIST)

- Ammo: - (carry up to None); no magazine
- Sprites: PONG, PUNG, PUNS

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 14 | 0.4 | MeleeStrikeNormal | Melee/Swing @3 | ready (ready3) |
| Reload from empty | 18 | 0.51 | - | Melee/Reload @7 | ready (ready3) |
| Reload with one round used | 18 | 0.51 | - | Melee/Reload @7 | ready (ready3) |
| Raise (select) | 4 | 0.11 | - | - | ready (ready) |
| Lower (deselect) | 1739 | 49.69 | - | - | cut short |
| Alt fire / aim | 21 | 0.6 | MeleeStrike2 | Melee/SwingDeep @2, *grunt @2 | ready (ready) |

Sound files: `*grunt` ?, `Melee/Reload` sounds\COMBAT\WEAPONS\MELEE\KNUCKLED.ogg, `Melee/Swing` ?, `Melee/SwingDeep` ?

## MG42  ($TAGBD_MG42)

- Ammo: - (carry up to None); no magazine
- Sprites: HBUS

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 3 | 0.09 | 1 x 24; ShakeYourAss; YellowFlareSpawn; 1 x 24; YellowFlareSpawn | Chaingun/Fire @0, Chaingun/Fire @1 | ready (ready) |
| Raise (select) | 5 | 0.14 | - | MG42/Draw @1 | ready (ready) |
| Lower (deselect) | 4 | 0.11 | - | - | wait |

Sound files: `Chaingun/Fire` sounds\COMBAT\WEAPONS\MP40\MP40.ogg, `MG42/Draw` sounds\COMBAT\WEAPONS\MP40\MG42UP.ogg

## MiniGun  ($TAGBD_CHAINGUN)

- Ammo: - (carry up to None); no magazine
- Sprites: CHAF, CHAG

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 66 | 1.89 | Alerter; -1 x 20; -1 x 20; -1 x 20 | Chaingun/Start @0, Chaingun/Fire @4, FARMGN @4, Chaingun/Fire @7, FARMGN @7, Chaingun/Fire @10, FARMGN @10, Chaingun/Stop @13 | ready (ready) |
| Raise (select) | 5 | 0.14 | - | CHGNPKUP @1 | ready (ready) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |
| Alt fire / aim | 6 | 0.17 | - | Chaingun/Start @0 | ready (ready2) |

Sound files: `CHGNPKUP` sounds\ITEMS\CHGNPKUP.ogg, `Chaingun/Fire` sounds\COMBAT\WEAPONS\MP40\MP40.ogg, `Chaingun/Start` sounds\COMBAT\WEAPONS\Minigun\CHAINSTA.ogg, `Chaingun/Stop` sounds\COMBAT\WEAPONS\Minigun\CHAINSTO.ogg, `FARMGN` sounds\COMBAT\WEAPONS\DISTANTSOUNDS\FARMGN.ogg

## MP40  ($TAGBD_MP40)

- Ammo: mauser9mm (carry up to 160); mp40ammo holds 32
- Sprites: 2P4R, 3P4R, MP40, MP4R

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 4 | 0.11 | -1 x 18 | MP40/Fire @0, FARSHT @0 | ready (ready3) |
| Reload from empty | 97 | 2.77 | - | MP40/Bolt1 @11, Weapon/Empty @27, MP40/Reload1 @37, MP40/Reload2 @60, MP40/Bolt2 @83 | ready (ready3) |
| Reload with one round used | 60 | 1.71 | - | Weapon/Empty @8, MP40/Reload1 @19, MP40/Reload2 @42 | ready (ready3) |
| Raise (select) | 5 | 0.14 | - | MP40/Draw @1 | ready (ready) |
| Lower (deselect) | 4 | 0.11 | - | - | wait |
| Alt fire / aim | 6 | 0.17 | - | ads/in @0 | ready (ready2) |

Sound files: `FARSHT` sounds\COMBAT\WEAPONS\DISTANTSOUNDS\FARSHT.ogg, `MP40/Bolt1` sounds\BOLTBACK.ogg, `MP40/Bolt2` sounds\COMBAT\WEAPONS\MP40\BOLTRELE.ogg, `MP40/Draw` sounds\COMBAT\WEAPONS\MP40\MP40DRAW.ogg, `MP40/Fire` sounds\COMBAT\WEAPONS\MP40\GMP40.ogg, `MP40/Reload1` sounds\COMBAT\WEAPONS\MP40\MP401.ogg, `MP40/Reload2` sounds\COMBAT\WEAPONS\MP40\MP402.ogg, `Weapon/Empty` sounds\COMBAT\WEAPONS\DRYFIRE.ogg, `ads/in` sounds\COMBAT\WEAPONS\ADSIN.ogg

## NaziShield  (NaziShield.dec)

- Ammo: bdpistolammo (carry up to 16); meatammo holds 100
- Sprites: GRZ6, PI3F, PI3G, THRW

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 4 | 0.11 | YellowFlareSpawn | Pistol/Fire @1 | ready (ready) |
| Raise (select) | 2 | 0.06 | - | - | ready (ready) |
| Lower (deselect) | 2 | 0.06 | - | - | ready (ready) |
| Alt fire / aim | 27 | 0.77 | ThrowedNazi | skeleton/swing @12 | ready (ready) |

Sound files: `Pistol/Fire` sounds\COMBAT\WEAPONS\PISTOL\PFIRE.ogg, `skeleton/swing` ?

## NukeLauncher  ($TAGBD_NUKE)

- Ammo: - (carry up to None); no magazine
- Sprites: NKLS

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 0 | 0.0 | - | - | ready (ready3) |
| Raise (select) | 5 | 0.14 | - | BFG/Draw @1 | ready (ready) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |

Sound files: `BFG/Draw` sounds\COMBAT\WEAPONS\BFG\BFGREADY.ogg

## Plasma_Gun  ($TAGBD_Plasma)

- Ammo: ammocell (carry up to 300); plasmaammo holds 50
- Sprites: PRSA, PRSG, PRSR

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 4 | 0.11 | Plasma_Ball | Plasma/Fire @0 | ready (ready) |
| Reload from empty | 55 | 1.57 | - | Plasma/Reload1 @0, Plasma/Reload2 @28 | ready (ready) |
| Reload with one round used | 55 | 1.57 | - | Plasma/Reload1 @0, Plasma/Reload2 @28 | ready (ready) |
| Raise (select) | 5 | 0.14 | - | Plasma/Draw @1, Plasma/Beep @5 | ready (ready) |
| Lower (deselect) | 5 | 0.14 | - | Plasma/BeepLow @0 | wait |
| Alt fire / aim | 84 | 2.4 | PlasmaFlareSpawn; PlasmaFlareSpawn; PlasmaFlareSpawn; PlasmaFlareSpawn; PlasmaFlareSpawn; PlasmaFlareSpawn; PlasmaFlareSpawn; PlasmaFlareSpawn; PlasmaFlareSpawn; PlasmaFlareSpawn; PlasmaFlareSpawn; PlasmaFlareSpawn; PlasmaFlareSpawn; PlasmaFlareSpawn; PlasmaFlareSpawn; PlasmaFlareSpawn; PlasmaFlareSpawn; PlasmaFlareSpawn; PlasmaFlareSpawn; PlasmaFlareSpawn; PlasmaBall75; PlasmaBall75; PlasmaBall75; PlasmaBall75; PlasmaBall75; PlasmaBall75; PlasmaBall75; PlasmaBall75; PlasmaBall75; PlasmaBall75; PlasmaFlareSpawn | Plasma/Charge @0, Plasma/FullyCharged @40, Plasma/BeepLow @40, Plasma/AltFire @44, Plasma/BeepBeep @84 | ready (ready) |

Sound files: `Plasma/AltFire` sounds\COMBAT\WEAPONS\Plasmagun\PLSALTFR.ogg, `Plasma/Beep` sounds\COMBAT\WEAPONS\Plasmagun\BEP.ogg, `Plasma/BeepBeep` sounds\COMBAT\WEAPONS\Plasmagun\BEPBEP.ogg, `Plasma/BeepLow` sounds\COMBAT\WEAPONS\Plasmagun\BEPlow.ogg, `Plasma/Charge` sounds\COMBAT\WEAPONS\Plasmagun\PLSCHARG.ogg, `Plasma/Draw` sounds\COMBAT\WEAPONS\Plasmagun\PLSDRAW.ogg, `Plasma/Fire` sounds\COMBAT\WEAPONS\Plasmagun\plsm9.ogg, `Plasma/FullyCharged` sounds\COMBAT\WEAPONS\Plasmagun\PLSFULL.ogg, `Plasma/Reload1` sounds\COMBAT\WEAPONS\Plasmagun\PLSREL1.ogg, `Plasma/Reload2` sounds\COMBAT\WEAPONS\Plasmagun\PLSREL2.ogg

## RailGun  ($TAGBD_RAILGUN)

- Ammo: ammocell (carry up to 300); railgunammo holds 5
- Sprites: RAIF, RAIL, RAIR, RAIZ, RAR2

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 43 | 1.23 | RailgunTrailEffectMissile; RailgunProjectile; railattack 400, 0, 0, "none", "none", RGF_FULLBRIGHT, 1, "RailgunPuff2" | Railgun/Fire @0, Railgun/Recharge @20, Plasma/BeepBeep @43 | ready (ready3) |
| Reload from empty | 71 | 2.03 | - | Railgun/Reload1 @0, Railgun/Reload2 @25, Plasma/Beep @55, Railgun/Recharge @59 | ready (ready) |
| Reload with one round used | 71 | 2.03 | - | Railgun/Reload1 @0, Railgun/Reload2 @25, Plasma/Beep @55, Railgun/Recharge @59 | ready (ready) |
| Raise (select) | 5 | 0.14 | - | Railgun/Recharge @5 | ready (ready) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |
| Alt fire / aim | 8 | 0.23 | - | ads/in @0 | ready (ready2) |

Sound files: `Plasma/Beep` sounds\COMBAT\WEAPONS\Plasmagun\BEP.ogg, `Plasma/BeepBeep` sounds\COMBAT\WEAPONS\Plasmagun\BEPBEP.ogg, `Railgun/Fire` sounds\COMBAT\WEAPONS\Railgun\RAILF1.ogg, `Railgun/Recharge` sounds\COMBAT\WEAPONS\Railgun\RAILR1.ogg, `Railgun/Reload1` sounds\COMBAT\WEAPONS\Railgun\RGREL1.ogg, `Railgun/Reload2` sounds\COMBAT\WEAPONS\Railgun\RGREL2.ogg, `ads/in` sounds\COMBAT\WEAPONS\ADSIN.ogg

## RepairTool  ($TAG_CHAINSAW)

- Ammo: - (carry up to None); no magazine
- Sprites: REPT

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 3 | 0.09 | RepairMissile | - | ready (ready) |
| Raise (select) | 20000 | 571.43 | - | - | cut short |
| Lower (deselect) | 20000 | 571.43 | - | - | cut short |

Sound files: -

## Revolver  ($TAGBD_REVOLVER)

- Ammo: ammoshell (carry up to 50); revolverammo holds 6
- Sprites: REVO, REVR, REVS

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 23 | 0.66 | 7 x 22; 2 x 22 | Revolver/Fire @0, Revolver/Hammer @16 | ready (ready3) |
| Reload from empty | 105 | 3.0 | - | Revolver/Open @7, Shotgun/Reload @25, Shotgun/Reload @36, Shotgun/Reload @47, Shotgun/Reload @58, Shotgun/Reload @69, Shotgun/Reload @80, Revolver/Close @97 | ready (ready) |
| Reload with one round used | 50 | 1.43 | - | Revolver/Open @7, Shotgun/Reload @25, Revolver/Close @42 | ready (ready) |
| Raise (select) | 5 | 0.14 | - | Revolver/Hammer @1 | ready (ready3) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |

Sound files: `Revolver/Close` sounds\COMBAT\WEAPONS\Revolver\revlose.ogg, `Revolver/Fire` sounds\COMBAT\WEAPONS\Revolver\REVOFIR.ogg, `Revolver/Hammer` sounds\COMBAT\WEAPONS\Revolver\REVOHAM.ogg, `Revolver/Open` sounds\COMBAT\WEAPONS\Revolver\revop.ogg, `Shotgun/Reload` ?

## Rifle  ($TAGBD_RIFLE)

- Ammo: clip2 (carry up to 200); rifleammo holds 31
- Sprites: 2IFR, RI2G, RIFF, RIFG, RIFR, RIFZ

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 4 | 0.11 | -1 x 20 | Rifle/Fire @0 | ready (ready) |
| Reload from empty | 59 | 1.69 | - | Rifle/Reload1 @0, Rifle/Reload2 @19, Rifle/Bolt1 @48, Rifle/Bolt2 @52 | ready (ready3) |
| Reload with one round used | 40 | 1.14 | - | Rifle/Reload1 @0, Rifle/Reload2 @19 | ready (ready3) |
| Raise (select) | 6 | 0.17 | - | Rifle/Select @1, Rifle/Select @2 | ready (ready3) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |
| Alt fire / aim | 8 | 0.23 | - | ads/in @0 | ready (ready2) |

Sound files: `Rifle/Bolt1` sounds\COMBAT\WEAPONS\Rifle\bolt1.ogg, `Rifle/Bolt2` sounds\COMBAT\WEAPONS\Rifle\bolt2.ogg, `Rifle/Fire` sounds\COMBAT\WEAPONS\Rifle\DSRIFLE.ogg, `Rifle/Reload1` sounds\COMBAT\WEAPONS\Rifle\RIFLER1.ogg, `Rifle/Reload2` sounds\COMBAT\WEAPONS\Rifle\RIFLER2.ogg, `Rifle/Select` sounds\COMBAT\WEAPONS\Rifle\CLIPIN.ogg, `ads/in` sounds\COMBAT\WEAPONS\ADSIN.ogg

## Rocket_Launcher  ($TAGBD_RL)

- Ammo: ammorocket (carry up to 50); rocketrounds holds 6
- Sprites: MIR2, MISF, MISG, MISR, MISS

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 18 | 0.51 | RedFlareSpawn; Alerter; Rocket2; RocketGlassBreaker | Rocket/Fire @0 | ready (ready) |
| Reload from empty | 46 | 1.31 | - | rocket/reload1 @0, rocket/reload2 @29 | ready (ready) |
| Reload with one round used | 46 | 1.31 | - | rocket/reload1 @0, rocket/reload2 @29 | ready (ready) |
| Raise (select) | 5 | 0.14 | - | Rocket/Draw @1 | ready (ready) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |
| Alt fire / aim | 8 | 0.23 | - | ads/in @0 | ready (ready2) |

Sound files: `Rocket/Draw` sounds\COMBAT\WEAPONS\RocketLauncher\RLANDRAW.ogg, `Rocket/Fire` sounds\COMBAT\WEAPONS\RocketLauncher\DSRFIRE.ogg, `ads/in` sounds\COMBAT\WEAPONS\ADSIN.ogg, `rocket/reload1` sounds\COMBAT\WEAPONS\RocketLauncher\RLREL1.ogg, `rocket/reload2` sounds\COMBAT\WEAPONS\RocketLauncher\RLREL2.ogg

## SguyShield  (SguyShield.dec)

- Ammo: bdpistolammo (carry up to 16); meatammo holds 100
- Sprites: GRZ2, PI3F, PI3G, THRW

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 4 | 0.11 | YellowFlareSpawn | Pistol/Fire @1 | ready (ready) |
| Raise (select) | 2 | 0.06 | - | - | ready (ready) |
| Lower (deselect) | 2 | 0.06 | - | - | ready (ready) |
| Alt fire / aim | 27 | 0.77 | ThrowedShotgunguy | skeleton/swing @12 | ready (ready) |

Sound files: `Pistol/Fire` sounds\COMBAT\WEAPONS\PISTOL\PFIRE.ogg, `skeleton/swing` ?

## Shot_Gun  ($TAGBD_SHOTGUN)

- Ammo: ammoshell (carry up to 50); shotgunammo holds 9
- Sprites: SHT8, SHTA, SHTN

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 27 | 0.77 | 4 x 13; 5 x 13 | Shotgun/Fire @0, Shotgun/Pump1 @13, Shotgun/Pump2 @20 | ready (readytofireagain) |
| Reload from empty | 105 | 3.0 | - | Shotgun/Reload @13, Shotgun/Reload @23, Shotgun/Reload @33, Shotgun/Reload @43, Shotgun/Reload @53, Shotgun/Reload @63, Shotgun/Reload @73, Shotgun/Reload @83 (+2) | ready (readytofireagain) |
| Reload with one round used | 25 | 0.71 | - | Shotgun/Reload @13 | ready (readytofireagain) |
| Raise (select) | 5 | 0.14 | - | Shotgun/Pump2 @1 | ready (ready3) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |
| Alt fire / aim | 7 | 0.2 | - | ads/in @0 | ready (ready2) |

Sound files: `Shotgun/Fire` sounds\COMBAT\WEAPONS\Shotgun\SGFIRE.ogg, `Shotgun/Pump1` sounds\COMBAT\WEAPONS\Shotgun\SHGUPUM1.ogg, `Shotgun/Pump2` sounds\COMBAT\WEAPONS\Shotgun\SHGUPUM2.ogg, `Shotgun/Reload` ?, `ads/in` sounds\COMBAT\WEAPONS\ADSIN.ogg

## Sniper  ($TAGBD_SNIPER)

- Ammo: sniperammo (carry up to 50); xm21ammo holds 11
- Sprites: SNIP, X21A, X21F, X21G, X21R, X21S, X22R

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 48 | 1.37 | -1 x 50; -1 x 50; -1 x 50; railattack 0, 0, 0, "none", "Gray", RGF_SILENT, 0, "None", 0, 0, 14000, 15, 1; railattack 30, 0, 0, "none", "None", RGF_SILENT, 0, "sniperpuff", 0, 0, 500, 15, 1 | Sniper/Fire @0, FARM14 @0 | ready (ready3) |
| Reload from empty | 80 | 2.29 | - | Sniper/MagOut @11, Sniper/MagIn @35, Sniper/BoltBack @67, Sniper/BoltForward @73 | ready (ready3) |
| Reload with one round used | 56 | 1.6 | - | Sniper/MagOut @11, Sniper/MagIn @35 | ready (ready3) |
| Raise (select) | 5 | 0.14 | - | Sniper/Draw @1 | ready (ready) |
| Lower (deselect) | 4 | 0.11 | - | - | wait |
| Alt fire / aim | 8 | 0.23 | - | ads/in @0 | ready (ready2) |

Sound files: `FARM14` sounds\COMBAT\WEAPONS\DISTANTSOUNDS\FARM14.ogg, `Sniper/BoltBack` sounds\COMBAT\WEAPONS\SniperRifle\X21BACK.ogg, `Sniper/BoltForward` sounds\COMBAT\WEAPONS\SniperRifle\X21FORW.ogg, `Sniper/Draw` sounds\COMBAT\WEAPONS\SniperRifle\X21DRAW.ogg, `Sniper/Fire` sounds\COMBAT\WEAPONS\SniperRifle\M14FIRE.ogg, `Sniper/MagIn` sounds\COMBAT\WEAPONS\SniperRifle\X21MGIN.ogg, `Sniper/MagOut` sounds\COMBAT\WEAPONS\SniperRifle\X21MGOUT.ogg, `ads/in` sounds\COMBAT\WEAPONS\ADSIN.ogg

## SSG  ($TAGBD_SSG)

- Ammo: ammoshell (carry up to 50); ssgammo holds 2
- Sprites: SHT2, SHTZ, SHZ2

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 61 | 1.74 | 1 x 40; 9 x 13; 9 x 13 | SSG/Fire @0, SSG/Lever2 @15, weapons/sshoto @27, weapons/sshotl @38, weapons/sshotc @47, SSG/Lever1 @57 | ready (ready) |
| Reload from empty | 49 | 1.4 | - | SSG/Lever2 @3, weapons/sshoto @15, weapons/sshotl @26, weapons/sshotc @35, SSG/Lever1 @45 | ready (ready) |
| Reload with one round used | 49 | 1.4 | - | SSG/Lever2 @3, weapons/sshoto @15, weapons/sshotl @26, weapons/sshotc @35, SSG/Lever1 @45 | ready (ready) |
| Raise (select) | 12 | 0.34 | - | weapons/sshotc @3, SSG/Lever1 @10 | ready (ready) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |
| Alt fire / aim | 6 | 0.17 | 9 x 13 | SSG/AltFire @0 | ready (ready) |

Sound files: `SSG/AltFire` sounds\COMBAT\WEAPONS\SuperShotgun\SSGALTFI.ogg, `SSG/Fire` sounds\COMBAT\WEAPONS\SuperShotgun\SSHFIRE.ogg, `SSG/Lever1` sounds\COMBAT\WEAPONS\SuperShotgun\SSGCLIP1.ogg, `SSG/Lever2` sounds\COMBAT\WEAPONS\SuperShotgun\SSGCLIP2.ogg, `weapons/sshotc` ?, `weapons/sshotl` ?, `weapons/sshoto` ?

## TankGun  (Main Battle Tank)

- Ammo: heavymachinegunammo (carry up to 2000); tankammo holds 100
- Sprites: TNHD

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 2500 | 71.43 | - | - | cut short |
| Raise (select) | 2 | 0.06 | - | - | ready (ready) |
| Lower (deselect) | 6667 | 190.49 | - | - | cut short |
| Alt fire / aim | 2503 | 71.51 | HeavyMachinegunProjectile | TANKMG @0 | cut short |

Sound files: `TANKMG` sounds\VEHICLES\TANK\TANKMG.ogg

## Unmaker  ($TAGBD_UNMAKER)

- Ammo: - (carry up to None); no magazine
- Sprites: UNHF, UNHS

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 12 | 0.34 | UnmakerLaser; railattack 1, 0, 0, "none", "red", RGF_NOPIERCING | RGF_SILENT | RGF_CENTERZ | RGF_FULLBRIGHT, 0, "hitpuff", 0, 0, 9999, 1; UnmakerLaser2; railattack 1, 0, 0, "none", "red", RGF_NOPIERCING | RGF_SILENT | RGF_CENTERZ | RGF_FULLBRIGHT, 0, "hitpuff", 0, 0, 9999, 1; UnmakerLaser; railattack 1, 0, 0, "none", "red", RGF_NOPIERCING | RGF_SILENT | RGF_CENTERZ | RGF_FULLBRIGHT, 0, "hitpuff", 0, 0, 9999, 1; UnmakerLaser2; railattack 1, 0, 0, "none", "red", RGF_NOPIERCING | RGF_SILENT | RGF_CENTERZ | RGF_FULLBRIGHT, 0, "hitpuff", 0, 0, 9999, 1 | Unmaker/Start @0, Unmaker/Loop @5, Unmaker/Stop @8 | ready (ready3) |
| Raise (select) | 5 | 0.14 | - | BFG/Draw @1 | ready (ready) |
| Lower (deselect) | 5 | 0.14 | - | - | wait |

Sound files: `BFG/Draw` sounds\COMBAT\WEAPONS\BFG\BFGREADY.ogg, `Unmaker/Loop` sounds\COMBAT\WEAPONS\Unmaker\UNMLOP.ogg, `Unmaker/Start` sounds\COMBAT\WEAPONS\Unmaker\UNMSTA.ogg, `Unmaker/Stop` sounds\COMBAT\WEAPONS\Unmaker\UNMSTO.ogg

## ZMANShield  (ZmanShield.dec)

- Ammo: bdpistolammo (carry up to 16); meatammo holds 100
- Sprites: GRZ1, PI3F, PI3G, THRW

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 4 | 0.11 | YellowFlareSpawn | Pistol/Fire @1 | ready (ready) |
| Raise (select) | 2 | 0.06 | - | - | ready (ready) |
| Lower (deselect) | 2 | 0.06 | - | - | ready (ready) |
| Alt fire / aim | 27 | 0.77 | ThrowedZman | skeleton/swing @12 | ready (ready) |

Sound files: `Pistol/Fire` sounds\COMBAT\WEAPONS\PISTOL\PFIRE.ogg, `skeleton/swing` ?

## ZombieCivilianShield  (ZombieCivilianShield.dec)

- Ammo: bdpistolammo (carry up to 16); meatammo holds 100
- Sprites: GRZ7, PI3F, PI3G, THRW

| What | Tics | Seconds | Shots (bullets x damage) | Sounds, at tic | Ends |
| --- | --- | --- | --- | --- | --- |
| Fire (one shot, back to ready) | 4 | 0.11 | YellowFlareSpawn | Pistol/Fire @1 | ready (ready) |
| Raise (select) | 2 | 0.06 | - | - | ready (ready) |
| Lower (deselect) | 2 | 0.06 | - | - | ready (ready) |
| Alt fire / aim | 27 | 0.77 | ThrowedZombieCivilian | skeleton/swing @12 | ready (ready) |

Sound files: `Pistol/Fire` sounds\COMBAT\WEAPONS\PISTOL\PFIRE.ogg, `skeleton/swing` ?
