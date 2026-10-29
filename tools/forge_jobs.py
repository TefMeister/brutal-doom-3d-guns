# Which forge cube gun stands in for which weapon, in Brutal Doom and in Ashes 2063, and the frames each one shows in
# the hand: writes the jobs file tools/gz_forge_export.py reads. No Blender.
#   python tools/forge_jobs.py doom|ashes <out jobs.json>
#
# Tefa, 2026-10-24: "please add all the weapons you have made so far into both brutal doom and ashes 2063 games".
# Left out on purpose: guns already in the game as models Tefa shaped and wore (Doom: pistol, shotgun, machine gun =
# the forge assault rifle's class `Rifle`; Ashes: revolver, 9mm, pump shotgun), so those stay as they are; the
# two-gun versions (they need a gun in each hand); and the Afterglow and Hard Reset weapons (other episodes).
import glob
import json
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from weapon_sprites import hand_frames

MEGA = os.path.join("D:" + os.sep, "MEGA transfer", "Game Files")

DOOM_BLENDS = os.path.join(MEGA, "brutal-doom-3d-guns", "3D blender", "forge-2026-10-19")
DOOM_SOURCE = os.path.join("D:" + os.sep, "Brutal Doom", "brutal22test6-extracted")   # brutal22test6.pk3, unpacked
# forge file -> Brutal Doom v22 test 6 class (sheet/WEAPONS.md)
DOOM = {
    "axe": "BrutalAxe", "chainsaw": "Chain_saw", "revolver": "Revolver", "smg": "BrutalSMG", "super_shotgun": "SSG",
    "assault_shotgun": "AssaultShotgun", "mp40": "MP40", "mg42": "MG42", "minigun": "MiniGun", "sniper_rifle": "Sniper",
    "grenade_launcher": "GrenadeLauncher", "hand_grenade": "HandGrenades", "rocket_launcher": "Rocket_Launcher",
    "incendiary_launcher": "IncendiaryLauncher", "revenant_launcher": "HellishMissileLauncher",
    "plasma_rifle": "Plasma_Gun", "railgun": "RailGun", "flamethrower": "Flamethrower2", "flame_cannon": "FlameCannon",
    "bfg9000": "BIG_FUCKING_GUN", "bfg10k": "BFG10k", "unmaker": "Unmaker", "devastator": "Devastator",
    "nuke_launcher": "NukeLauncher", "dragonslayer": "DSweap",
}

ASHES_BLENDS = os.path.join(MEGA, "ashes-2063-weapons", "3D blender", "forge-2026-10-19")
# where Ashes is installed: the home PC first, then the dev PC
ASHES_SOURCE = next((p for p in (os.path.join(d, "Resources", "Ashes2063Enriched2_23.pk3") for d in (
    os.path.join("C:" + os.sep, "NonSteam", "Ashes 2063 VR"), os.path.join("D:" + os.sep, "ashes2063vr", "Ashes 2063 VR")))
    if os.path.isfile(p)), os.path.join("C:" + os.sep, "NonSteam", "Ashes 2063 VR", "Resources", "Ashes2063Enriched2_23.pk3"))
# forge file -> (weapon file in the pk3, classes); pumpaction2 is the shotgun's upgraded build, which had no model
ASHES = {
    "crowbar": ("Crowbar", ["Crowbar"]), "sawed_off": ("Sawedoff", ["SawedOff"]),
    "machine_pistol": ("Ingram", ["Ingram", "Ingram2", "Ingram3"]), "master_blaster": ("MBlaster", ["NapalmGun"]),
    "junker_musket": ("Musket", ["JunkerMusket"]), "pipe_bomb": ("pipebomb", ["pipebomb"]),
    "jackhammer": ("Hammer", ["JACKHAMMER"]), "battle_rifle": ("FAL", ["FAL"]),
    "pump_shotgun": ("Shotgun", ["pumpaction2"]),
}
# borrowed by Ashes weapons from elsewhere: the quick knife, Doom's own chaingun and shotgun frames used as blanks,
# the 9mm's and the Ingram's frames
ASHES_FOREIGN = {"KNIF", "CHGG", "SHTG", "NULL", "GLOK", "INGG"}
# guns with a live scope (2026-10-29): forge part holding the glass, and the surface the scope script swaps (scope/)
ASHES_SCOPES = {"battle_rifle": ("glass", 0)}


def doom_jobs():
    files = {os.path.basename(f).lower(): f for f in glob.glob(DOOM_SOURCE + "/**/*", recursive=True)
             if os.path.isfile(f)}
    sheet = json.load(open(os.path.join(os.path.dirname(HERE), "sheet", "weapons.json")))
    own = {w["name"]: set(w["sprites"]) for w in sheet}
    file_of = {w["name"]: w["file"] for w in sheet}
    jobs = {}
    for gun, cls in DOOM.items():
        src = open(files[os.path.basename(file_of[cls]).lower()], encoding="latin-1").read()
        foreign = set().union(*(v for k, v in own.items() if k != cls)) - own[cls]
        jobs[gun] = {"name": "bdf_" + gun, "blend": os.path.join(DOOM_BLENDS, gun + ".blend"),
                     "model_path": "models/bd3dguns/forge/" + gun, "classes": {cls: hand_frames(src, cls, foreign)}}
    return jobs


def ashes_jobs():
    z = zipfile.ZipFile(ASHES_SOURCE)
    jobs = {}
    for gun, (wfile, classes) in ASHES.items():
        src = z.read(f"Actors/Weapons/{wfile}.txt").decode("latin-1")
        own_ingram = gun == "machine_pistol"
        foreign = ASHES_FOREIGN - ({"INGG"} if own_ingram else set())
        jobs[gun] = {"name": "af_" + gun, "blend": os.path.join(ASHES_BLENDS, gun + ".blend"),
                     "model_path": "models/ashes2063/forge/" + gun,
                     "classes": {c: hand_frames(src, c, foreign) for c in classes}}
        if gun in ASHES_SCOPES:
            jobs[gun]["glass_part"], jobs[gun]["glass_surface"] = ASHES_SCOPES[gun]
    return jobs


if __name__ == "__main__":
    game, out = sys.argv[1], sys.argv[2]
    jobs = doom_jobs() if game == "doom" else ashes_jobs()
    for gun, j in jobs.items():
        for c, fr in j["classes"].items():
            assert fr, f"{gun}: no hand frames found for {c}"
            print(f"{gun:20s} {c:24s} {len(fr):3d} frames, sprites {sorted({s for s, _ in fr})}")
    json.dump(jobs, open(out, "w"), indent=1)
    print(f"{len(jobs)} guns -> {out}")
