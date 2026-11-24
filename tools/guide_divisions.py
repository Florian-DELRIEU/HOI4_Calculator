"""Crée les divisions d'exemple du guide Paradox dans saves/divisions/.

Source : « Beginner's Guide to Unit Types & Division Design » (GAGA Extrem,
2016), section « Example Division Designs » —
https://forum.paradoxplaza.com/forum/threads/beginners-guide-to-unit-types-division-design.942449/

Chaque design est décliné par époque : génération d'équipement pour
l'infanterie et l'artillerie, classe de chars pour les divisions blindées.
Une époque n'est proposée que si le design y a un sens (pas de roquettes ni de
mécanisés en 1936). Les statistiques sont calculées depuis la composition.

    python tools/guide_divisions.py            # crée les fichiers manquants
    python tools/guide_divisions.py --force    # réécrit aussi les existants
    python tools/guide_divisions.py --check    # n'écrit rien, affiche le rapport
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine.composition import aggregate              # noqa: E402
from engine.division import DivisionTemplate          # noqa: E402
from persistence.divisions import DivisionStore       # noqa: E402

FOLDER = "Guide Paradox"

# Époque -> (génération d'équipement, classe de chars, libellé de la classe)
ERAS = {
    "1936": ("1936", "light", "chars légers"),
    "1939": ("1939", "medium", "chars moyens"),
    "1942": ("1942", "heavy", "chars lourds"),
    "1945": ("1942", "modern", "chars modernes"),
}
ALL_WAR = ("1936", "1939", "1942")
FROM_1939 = ("1939", "1942")

# (nom, époques, largeur annoncée par le guide, bataillons, soutien).
# « {c} » est remplacé par la classe de chars de l'époque.
DESIGNS = [
    ("Infanterie de base", ALL_WAR, 20,
     {"infantry": 10},
     ["support_artillery", "engineer"]),
    ("Infanterie intermédiaire", ALL_WAR, 20,
     {"infantry": 7, "artillery": 2},
     ["support_artillery", "support_anti_tank", "engineer"]),
    ("Infanterie de luxe", ALL_WAR, 20,
     {"infantry": 7, "artillery": 2},
     ["support_artillery", "support_anti_tank", "support_anti_air", "engineer", "logistics"]),
    ("Infanterie de luxe XL", ALL_WAR, 22,
     {"infantry": 8, "artillery": 2},
     ["support_artillery", "support_anti_tank", "support_anti_air", "engineer", "logistics"]),
    ("Assaut de masse", FROM_1939, None,
     {"infantry": 10, "artillery": 2},
     ["support_artillery", "support_anti_tank", "support_rocket_artillery", "engineer",
      "logistics"]),
    ("Infanterie lourde", FROM_1939, 20,
     {"infantry": 6, "artillery": 2, "heavy_td": 1},
     ["support_artillery", "support_rocket_artillery", "engineer", "logistics"]),
    ("Division d'artillerie", FROM_1939, 20,
     {"infantry": 4, "artillery": 4},
     ["support_artillery", "support_rocket_artillery", "logistics"]),
    ("Division antichar", ALL_WAR, 10,
     {"infantry": 4, "anti_tank": 2},
     ["support_anti_tank", "engineer"]),
    ("Division antiaérienne", ALL_WAR, 10,
     {"infantry": 2, "anti_air": 6},
     ["support_anti_air", "engineer"]),
    ("Division de garnison", ALL_WAR, None,
     {"infantry": 4, "anti_air": 2},
     ["engineer", "support_anti_air"]),
    ("Division de sécurité", ALL_WAR, None,
     {"cavalry": 5},
     ["military_police"]),
    ("Division motorisée", FROM_1939, None,
     {"motorized": 7, "motorized_rocket_artillery": 2},
     ["support_artillery", "recon", "engineer"]),
    ("Fer de lance blindé", ("1936", "1939", "1942", "1945"), 20,
     {"{c}_spg": 2, "{c}_tank": 3, "motorized": 4},
     ["support_artillery", "support_anti_tank", "maintenance", "logistics"]),
    ("Canons d'assaut", ("1936", "1939", "1942", "1945"), 20,
     {"{c}_spg": 4, "{c}_tank": 2, "motorized": 2},
     ["support_artillery"]),
    ("Blindée mixte", ("1939", "1942", "1945"), 20,
     {"{c}_spg": 2, "{c}_tank": 3, "{c}_td": 1, "mechanized": 3},
     []),
]


def build() -> list[tuple[DivisionTemplate, int | None]]:
    """Liste de ``(template, largeur annoncée par le guide)``."""
    result = []
    for name, eras, guide_width, battalions, supports in DESIGNS:
        armored = any("{c}" in uid for uid in battalions)
        for era in eras:
            equipment, chassis, chassis_label = ERAS[era]
            line = [uid.format(c=chassis)
                    for uid, count in battalions.items() for _ in range(count)]
            suffix = f"{era}, {chassis_label}" if armored else era
            stats, recon = aggregate(line, supports, equipment)
            template = DivisionTemplate(
                name=f"{name} ({suffix})", stats=stats, recon=recon,
                battalions=line, support_companies=list(supports),
                equipment=equipment, folder=f"{FOLDER}/{era}")
            result.append((template, guide_width))
    return result


def install(store: DivisionStore, force: bool = False) -> int:
    """Enregistre les divisions ; sans ``force``, les noms déjà présents sont
    conservés tels quels (modifications de l'utilisateur comprises)."""
    existing = {t.name for t in store.list_templates()}
    count = 0
    for template, _ in build():
        if force or template.name not in existing:
            store.save(template)
            count += 1
    return count


def main(argv: list[str]) -> int:
    divisions = build()
    for template, guide_width in divisions:
        s = template.stats
        gap = (f"  (guide : {guide_width})"
               if guide_width and s.width != guide_width else "")
        print(f"{template.folder[len(FOLDER) + 1:]}  {template.name:48} larg. {s.width:g}{gap}"
              f"  AS {s.soft_attack:g}  déf {s.defense:g}  percée {s.breakthrough:g}"
              f"  org {s.organisation:g}")
    print(f"{len(divisions)} divisions.")
    if "--check" not in argv:
        print(f"Écrites : {install(DivisionStore(), force='--force' in argv)}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
