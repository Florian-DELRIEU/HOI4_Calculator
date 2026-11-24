"""Génère data/battalions.json depuis les CSV vanilla (tools/sources/).

Les CSV sont des extractions brutes du wiki : valeurs aplaties, pourcentages
en texte, vitesses « 10/12/14 », cellules non alignées pour les compagnies de
soutien. Ce script normalise tout cela une fois pour toutes ; le moteur ne lit
que le JSON produit.

    python tools/import_csv.py            # réécrit data/battalions.json
    python tools/import_csv.py --check    # n'écrit rien, affiche le rapport

Périmètre : stats **génériques** (équipement de base, sans concepteur de
chars). Les lignes dont les stats de combat sont absentes ou impossibles à
aligner sont écartées et listées dans le rapport.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = Path(__file__).resolve().parent / "sources"
OUTPUT = ROOT / "data" / "battalions.json"

# --------------------------------------------------------------- bataillons

# nom CSV -> (id, nom français). Les ids historiques sont conservés pour que
# les templates déjà enregistrés restent valides.
LINE_UNITS = {
    "Infantry": ("infantry", "Infanterie"),
    "Bicycle": ("bicycle", "Vélo"),
    "Penal Battalion": ("penal_battalion", "Bataillon disciplinaire"),
    "Irregular Infantry": ("irregular_infantry", "Infanterie irrégulière"),
    "Militia": ("militia", "Milice"),
    "Mountaineers": ("mountain", "Montagne"),
    "Marines": ("marines", "Marines"),
    "Marine Commandos": ("marine_commandos", "Commandos de marine"),
    "Paratrooper": ("paratrooper", "Parachutistes"),
    "Rangers": ("rangers", "Rangers"),
    "Cavalry": ("cavalry", "Cavalerie"),
    "Camelry": ("camelry", "Chameliers"),
    "Elephantry": ("elephantry", "Cavalerie d'éléphants"),
    "Motorized Infantry": ("motorized", "Motorisée"),
    "Mechanized Infantry": ("mechanized", "Mécanisée"),
    "Amtrac Battalion": ("amtrac", "Véhicules amphibies (Amtrac)"),
    "Armored Car": ("armored_car", "Voitures blindées"),
    "Anti-Tank": ("anti_tank", "Antichar"),
    "Anti-Air": ("anti_air", "Antiaérien"),
    "Artillery": ("artillery", "Artillerie"),
    "Rocket Artillery": ("rocket_artillery", "Artillerie de roquettes"),
    "Motorized Anti-Tank": ("motorized_anti_tank", "Antichar motorisé"),
    "Motorized Anti-Air": ("motorized_anti_air", "Antiaérien motorisé"),
    "Motorized Artillery": ("motorized_artillery", "Artillerie motorisée"),
    "Truck-drawn Rocket Artillery": ("truck_rocket_artillery", "Roquettes tractées (camions)"),
    "Motorized Rocket Artillery": ("motorized_rocket_artillery", "Artillerie de roquettes motorisée"),
    "Light Tank": ("light_tank", "Char léger"),
    "Medium Tank": ("medium_tank", "Char moyen"),
    "Heavy Tank": ("heavy_tank", "Char lourd"),
    "Modern Tank": ("modern_tank", "Char moderne"),
    "Amphibious Tank Battalion": ("amphibious_tank", "Char amphibie"),
    "Light Tank Destroyer": ("light_td", "Chasseur de chars léger"),
    "Medium Tank Destroyer": ("medium_td", "Chasseur de chars moyen"),
    "Heavy Tank Destroyer": ("heavy_td", "Chasseur de chars lourd"),
    "Modern Tank Destroyer": ("modern_td", "Chasseur de chars moderne"),
    "Light SP Artillery": ("light_spg", "Artillerie automotrice légère"),
    "Medium SP Artillery": ("medium_spg", "Artillerie automotrice moyenne"),
    "Heavy SP Artillery": ("heavy_spg", "Artillerie automotrice lourde"),
    "Modern SP Artillery": ("modern_spg", "Artillerie automotrice moderne"),
    "Light SP Anti-Air": ("light_spaa", "Antiaérien automoteur léger"),
    "Medium SP Anti-Air": ("medium_spaa", "Antiaérien automoteur moyen"),
    "Heavy SP Anti-Air": ("heavy_spaa", "Antiaérien automoteur lourd"),
    "Modern SP Anti-Air": ("modern_spaa", "Antiaérien automoteur moderne"),
}

CATEGORY_GROUP = {
    "Infanterie": "infanterie",
    "Mobile": "mobile",
    "Soutien de combat": "artillerie",
    "Soutien de combat mobile": "artillerie",
    "Blindés": "blinde",
    "Soutien de combat blindé": "blinde",
}

LINE_NOTES = {
    "Camelry": "Alignement des stats douteux dans la source — à vérifier.",
    "Elephantry": "Alignement des stats douteux dans la source — à vérifier.",
}

# ---------------------------------------------------------------- compagnies

# nom CSV -> (id, nom français, layout des stats de combat, layout des stats
# de structure). Layouts : voir _COMBAT_LAYOUTS / _STRUCT_LAYOUTS.
SUPPORT_UNITS = {
    "Support Anti-Tank": ("support_anti_tank", "Antichar (soutien)", "at", "std"),
    "Support Anti-Air": ("support_anti_air", "Antiaérien (soutien)", "aa", "std"),
    "Support Artillery": ("support_artillery", "Artillerie (soutien)", "s5", "std"),
    "Support Rocket Artillery": ("support_rocket_artillery", "Artillerie de roquettes (soutien)", "s5", "std"),
    "Super-Heavy Artillery": ("super_heavy_artillery", "Artillerie super-lourde", "s5", "std"),
    "Self-Propelled Super-Heavy Artillery": ("sp_super_heavy_howitzer", "Obusier super-lourd automoteur", "s6", "std"),
    "Cavalry Recon Company": ("recon", "Reconnaissance (cavalerie)", "s5", "std"),
    "Recon Rangers": ("recon_rangers", "Rangers de reconnaissance", "s5", "std"),
    "Long Range Patrol Company": ("long_range_patrol", "Patrouille longue portée", "s5", "std"),
    "Motorized Recon Company": ("motorized_recon", "Reconnaissance motorisée", "s5", "std"),
    "Armored Car Recon Company": ("armored_car_recon", "Reconnaissance en voitures blindées", "s6", "std"),
    "Light Tank Recon Company": ("light_tank_recon", "Reconnaissance en chars légers", "s6", "std"),
    "Airborne Light Armor": ("airborne_light_armor", "Blindés légers aéroportés", "s6", "std"),
    "Engineer Company": ("engineer", "Génie", "s5", "std"),
    "Armored Engineer Company": ("armored_engineer", "Génie blindé", "s6", "std"),
    "Assault Engineer Company": ("assault_engineer", "Génie d'assaut", "s6", "std"),
    "Pioneers": ("pioneers", "Pionniers", "s5", "std"),
    "Jungle Pioneers": ("jungle_pioneers", "Pionniers de jungle", "s5", "std"),
    "Field Hospital": ("field_hospital", "Hôpital de campagne", "bt", "std"),
    "Maintenance Company": ("maintenance", "Compagnie de maintenance", "none", "std"),
    "Armored Maintenance Company": ("armored_maintenance", "Maintenance blindée", "s6", "std"),
    "Logistics Company": ("logistics", "Compagnie de logistique", "bt", "std"),
    "Military Police": ("military_police", "Police militaire", "s5", "std"),
    "Motorized Military Police": ("motorized_military_police", "Police militaire motorisée", "s5", "std"),
    "Signal Company": ("signal", "Compagnie de transmission", "bt", "std"),
    "Armored Signal Company": ("armored_signal", "Transmissions blindées", "s6", "std"),
    "Super Heavy Tank": ("super_heavy_tank", "Char super-lourd", "h7", "heavy"),
    "Super Heavy SP Artillery": ("super_heavy_spg", "Artillerie automotrice super-lourde", "h7", "heavy"),
    "Super Heavy Tank Destroyer": ("super_heavy_td", "Chasseur de chars super-lourd", "h7", "heavy"),
    "Super Heavy SP Anti-Air": ("super_heavy_spaa", "Antiaérien automoteur super-lourd", "h8", "heavy"),
    "Land Cruiser": ("land_cruiser", "Croiseur terrestre", "h8", "heavy"),
    "Assault Battalion": ("assault_battalion", "Bataillon d'assaut", "s5", "heavy"),
    "Winter Logistics Company": ("winter_logistics", "Logistique hivernale", "s5", "std"),
    "Sturmtruppe Battalion": ("sturmtruppe", "Sturmtruppen", "s5", "heavy"),
}

# Écartées : stats de combat absentes ou format qu'on ne sait pas aligner.
SKIPPED_SUPPORT = {
    "Helicopter Recon": "format de stats hélicoptère non aligné",
    "Helicopter Brigade": "format de stats hélicoptère non aligné",
    "Helicopter Med-Evac": "format de stats hélicoptère non aligné",
    "Helicopter Transports": "format de stats hélicoptère non aligné",
    "Light Flame Tank Company": "stats de combat absentes",
    "Medium Flame Tank Company": "stats de combat absentes",
    "Heavy Flame Tank Company": "stats de combat absentes",
}

# Familles mutuellement exclusives (texte « bloque autres … » de la source).
EXCLUSION = {
    "recon": ["recon", "recon_rangers", "long_range_patrol", "motorized_recon",
              "armored_car_recon", "light_tank_recon", "airborne_light_armor"],
    "engineer": ["engineer", "armored_engineer", "assault_engineer", "pioneers",
                 "jungle_pioneers"],
    "maintenance": ["maintenance", "armored_maintenance"],
    "signal": ["signal", "armored_signal"],
    "military_police": ["military_police", "motorized_military_police"],
}
EXCLUSION_OF = {uid: fam for fam, ids in EXCLUSION.items() for uid in ids}

# Compagnies dont la vitesse (et donc celle de la division) est imposée.
SLOWS_DIVISION = {"super_heavy_tank", "super_heavy_spg", "super_heavy_td",
                  "super_heavy_spaa", "land_cruiser"}

SUPPORT_NOTES = {
    "super_heavy_artillery": "Vitesse non fournie par la source (ne ralentit pas la division ici).",
    "sp_super_heavy_howitzer": "Vitesse non fournie par la source (ne ralentit pas la division ici).",
    "land_cruiser": "Coût douteux dans la source (1 véhicule).",
    "airborne_light_armor": "Alignement des stats déduit des modificateurs — à vérifier.",
}

# Layouts des cellules « équipement » (avant les 3 dernières : carburant
# capacité, carburant conso, coût). Les compagnies de soutien n'ont pas de
# largeur.
_COMBAT_LAYOUTS = {
    "none": [],
    "bt": ["breakthrough"],
    "at": ["soft", "hard", "defense", "piercing"],
    "s5": ["soft", "hard", "defense", "breakthrough", "piercing"],
    "aa": ["soft", "hard", "air", "defense", "breakthrough", "piercing"],
    "s6": ["soft", "hard", "defense", "breakthrough", "armor", "piercing"],
    "h7": ["speed", "soft", "hard", "defense", "breakthrough", "armor", "piercing"],
    "h8": ["speed", "soft", "hard", "air", "defense", "breakthrough", "armor", "piercing"],
}
# Cellules de structure (avant « | ») : la 6ᵉ valeur est, pour les compagnies
# de reconnaissance, la reconnaissance apportée.
_STRUCT_LAYOUTS = {
    "std": ["hp", "org", "recovery", "suppression", "supply", "extra"],
    "heavy": ["hp", "org", "recovery", "suppression", "weight", "supply"],
}


def _num(text: str | None, default: float = 0.0) -> float:
    if text is None:
        return default
    text = text.strip().replace("%", "")
    if not text:
        return default
    return float(text)


def _pct(text: str | None) -> float:
    return _num(text) / 100.0


def _read_csv(name: str) -> list[dict]:
    with open(SOURCES / name, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _clean(value: float) -> float:
    value = round(value, 4)
    return int(value) if value == int(value) and abs(value) < 1e9 else value


def import_line_units(report: dict) -> list[dict]:
    entries = []
    for row in _read_csv("vanilla_bataillons_terrestres.csv"):
        name = row["nom"]
        if name not in LINE_UNITS:
            report["skipped"].append((name, "absent de la table de correspondance"))
            continue
        if not row["attaque_souple"]:
            report["skipped"].append((name, "stats de combat absentes dans la source"))
            continue
        uid, nom = LINE_UNITS[name]
        raw_speed = row["vitesse_kmh"]
        speed = float(raw_speed.split("/")[0])
        notes = []
        if "/" in raw_speed:
            notes.append(f"Vitesse « {raw_speed} » dans la source : 1ʳᵉ valeur retenue.")
        if name in LINE_NOTES:
            notes.append(LINE_NOTES[name])
        entry = {
            "id": uid, "nom": nom, "group": CATEGORY_GROUP[row["categorie"]],
            "line": True, "width": _num(row["largeur"]),
            "hp": _num(row["pv"]), "org": _num(row["organisation"]),
            "soft": _num(row["attaque_souple"]), "hard": _num(row["attaque_dure"]),
            "air": _num(row["attaque_air"]), "defense": _num(row["defense"]),
            "breakthrough": _num(row["percee"]), "armor": _num(row["blindage"]),
            "piercing": _num(row["perforation"]), "hardness": _pct(row["durete"]),
            "speed": speed,
        }
        if "artillery" in name.lower():
            entry["artillery"] = True
        entry.update({
            "manpower": _num(row["effectif_hommes"]),
            "training_days": _num(row["entrainement_jours"]),
            "ic_cost": _num(row["cout_production_ic"]),
            "supply_use": _num(row["ravitaillement"]),
            "fuel_capacity": _num(row["carburant_capacite"]),
            "fuel_use": _num(row["carburant_conso"]),
        })
        if notes:
            entry["note"] = " ".join(notes)
        entries.append(entry)
    return entries


def _floats(text: str) -> list[float]:
    return [float(t) for t in text.replace(" ", "").split(",") if t]


def import_support_units(report: dict) -> list[dict]:
    entries = []
    for row in _read_csv("vanilla_compagnies_soutien.csv"):
        name = row["nom"]
        if name in SKIPPED_SUPPORT:
            report["skipped"].append((name, SKIPPED_SUPPORT[name]))
            continue
        if name not in SUPPORT_UNITS:
            report["skipped"].append((name, "absent de la table de correspondance"))
            continue
        uid, nom, combat_layout, struct_layout = SUPPORT_UNITS[name]
        left, _, right = row["valeurs_brutes_wiki"].partition("|")
        struct = dict(zip(_STRUCT_LAYOUTS[struct_layout], _floats(left)))
        right_values = _floats(right)
        fields = _COMBAT_LAYOUTS[combat_layout]
        if len(right_values) != len(fields) + 3:
            raise ValueError(f"{name} : {len(right_values)} valeurs, "
                             f"layout {combat_layout} attend {len(fields) + 3}")
        combat = dict(zip(fields, right_values[:len(fields)]))
        fuel_capacity, fuel_use, cost = right_values[len(fields):]
        special = row["effets_speciaux"]
        entry = {
            "id": uid, "nom": nom, "group": "soutien", "line": False, "width": 0,
            "hp": struct["hp"], "org": struct["org"],
            "soft": combat.get("soft", 0), "hard": combat.get("hard", 0),
            "air": combat.get("air", 0), "defense": combat.get("defense", 0),
            "breakthrough": combat.get("breakthrough", 0),
            "armor": combat.get("armor", 0), "piercing": combat.get("piercing", 0),
            "hardness": 0.0, "speed": combat.get("speed", 0.0),
        }
        if "artillery" in name.lower() or "Artillery" in nom:
            entry["artillery"] = True
        recon = 0.0
        if uid in EXCLUSION["recon"]:
            recon = struct.get("extra", 0.0)
        m = re.search(r"\+(\d+(?:\.\d+)?) reconnaissance", special)
        if m:
            recon = float(m.group(1))
        if recon:
            entry["recon"] = recon
        m = re.search(r"\+(\d+(?:\.\d+)?)% initiative", special)
        if m:
            entry["initiative"] = float(m.group(1)) / 100.0
        if uid in EXCLUSION_OF:
            entry["exclusion"] = EXCLUSION_OF[uid]
        if uid in SLOWS_DIVISION:
            entry["slows_division"] = True
        entry["special"] = special
        entry.update({
            "manpower": _num(row["effectif_hommes"]),
            "training_days": _num(row["entrainement_jours"]),
            "ic_cost": cost,
            "supply_use": struct.get("supply", 0.0),
            "fuel_capacity": fuel_capacity,
            "fuel_use": fuel_use,
        })
        if uid in SUPPORT_NOTES:
            entry["note"] = SUPPORT_NOTES[uid]
        if uid in EXCLUSION["recon"]:
            entry.setdefault("note", "")
            entry["note"] = (entry["note"] + " Reconnaissance déduite d'une colonne "
                             "brute de la source.").strip()
        entries.append(entry)
    return entries


def build() -> tuple[list[dict], dict]:
    report: dict = {"skipped": []}
    entries = import_line_units(report) + import_support_units(report)
    ids = [e["id"] for e in entries]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError(f"identifiants en double : {sorted(dupes)}")
    return entries, report


def _clean_entry(entry: dict) -> dict:
    return {k: (_clean(v) if isinstance(v, float) else v) for k, v in entry.items()}


def write(entries: list[dict]) -> None:
    comment = ("Généré par tools/import_csv.py depuis tools/sources/*.csv "
               "(stats génériques, équipement de base, sans concepteur de chars). "
               "Ne pas éditer à la main : relancer le script. Les compagnies de "
               "soutien ont une largeur de 0 et ne comptent ni pour la dureté ni "
               "(sauf `slows_division`) pour la vitesse.")
    lines = ['{', f'  "_comment": {json.dumps(comment, ensure_ascii=False)},',
             '  "battalions": [']
    for i, entry in enumerate(entries):
        sep = "," if i < len(entries) - 1 else ""
        lines.append("    " + json.dumps(_clean_entry(entry), ensure_ascii=False) + sep)
    lines += ["  ]", "}", ""]
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str]) -> int:
    entries, report = build()
    line = sum(1 for e in entries if e["line"])
    print(f"{line} bataillons de ligne, {len(entries) - line} compagnies de soutien.")
    for name, why in report["skipped"]:
        print(f"  écarté : {name} — {why}")
    if "--check" not in argv:
        write(entries)
        print(f"Écrit : {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
