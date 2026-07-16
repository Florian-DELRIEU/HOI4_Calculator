"""Agrégation d'une composition en bataillons vers les stats de division
(CDC §6.1) — formules confirmées par la source :

- HP = somme ; Organisation = moyenne de tous (compagnies incluses) ;
- attaques/défense/percée/attaque aérienne = somme ;
- Blindage = 30 % du max + 70 % de la moyenne ;
- Perce-blindage = 40 % du max + 60 % de la moyenne ;
- Largeur = somme des bataillons de ligne (soutiens = 0) ;
- Dureté = moyenne des bataillons de ligne ;
- Vitesse = celle du bataillon de ligne le plus lent ;
- Initiative/Recon = apport des compagnies (transmission, reconnaissance).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field

from engine.division import DivisionStats
from engine.gamedata import DATA_DIR

MAX_LINE_BATTALIONS = 25
MAX_SUPPORT_COMPANIES = 5


@dataclass(frozen=True)
class BattalionDef:
    id: str
    nom: str
    group: str
    line: bool
    width: float
    hp: float
    org: float
    soft: float
    hard: float
    air: float
    defense: float
    breakthrough: float
    armor: float
    piercing: float
    hardness: float
    speed: float
    artillery: bool = False
    recon: float = 0.0
    initiative: float = 0.0
    recovery: float = 0.3
    special: str = ""

    def __str__(self):
        return self.nom


def _load_battalions() -> dict[str, BattalionDef]:
    with open(DATA_DIR / "battalions.json", encoding="utf-8") as f:
        payload = json.load(f)
    return {b["id"]: BattalionDef(**b) for b in payload["battalions"]}


BATTALIONS: dict[str, BattalionDef] = _load_battalions()

LINE_BATTALIONS = {k: b for k, b in BATTALIONS.items() if b.line}
SUPPORT_COMPANIES = {k: b for k, b in BATTALIONS.items() if not b.line}


def is_artillery(battalion_id: str) -> bool:
    b = BATTALIONS.get(battalion_id)
    return b is not None and b.artillery


def validate(battalions: list[str], supports: list[str]) -> list[str]:
    """Renvoie la liste des problèmes de composition (vide = valide)."""
    problems = []
    if len(battalions) > MAX_LINE_BATTALIONS:
        problems.append(f"Plus de {MAX_LINE_BATTALIONS} bataillons de ligne.")
    if len(supports) > MAX_SUPPORT_COMPANIES:
        problems.append(f"Plus de {MAX_SUPPORT_COMPANIES} compagnies de soutien.")
    for bid in battalions:
        if bid not in LINE_BATTALIONS:
            problems.append(f"Bataillon inconnu ou non de ligne : {bid}")
    seen = set()
    for sid in supports:
        if sid not in SUPPORT_COMPANIES:
            problems.append(f"Compagnie de soutien inconnue : {sid}")
        elif sid in seen:
            problems.append(f"Compagnie de soutien en double : {sid}")
        seen.add(sid)
    return problems


def aggregate(battalions: list[str], supports: list[str]) -> tuple[DivisionStats, float]:
    """Calcule les stats finales d'une division composée.

    Renvoie ``(stats, recon)``. Lève ``ValueError`` si la composition est
    invalide.
    """
    problems = validate(battalions, supports)
    if problems:
        raise ValueError(" ; ".join(problems))

    line = [BATTALIONS[b] for b in battalions]
    supp = [BATTALIONS[s] for s in supports]
    all_units = line + supp
    if not all_units:
        return DivisionStats(), 0.0

    stats = DivisionStats()
    stats.hp = sum(u.hp for u in all_units)
    stats.organisation = sum(u.org for u in all_units) / len(all_units)
    stats.soft_attack = sum(u.soft for u in all_units)
    stats.hard_attack = sum(u.hard for u in all_units)
    stats.air_attack = sum(u.air for u in all_units)
    stats.defense = sum(u.defense for u in all_units)
    stats.breakthrough = sum(u.breakthrough for u in all_units)

    armors = [u.armor for u in all_units]
    stats.armor = 0.3 * max(armors) + 0.7 * (sum(armors) / len(armors))
    piercings = [u.piercing for u in all_units]
    stats.piercing = 0.4 * max(piercings) + 0.6 * (sum(piercings) / len(piercings))

    stats.width = sum(u.width for u in line)
    stats.hardness = (sum(u.hardness for u in line) / len(line)) if line else 0.0
    stats.speed = min((u.speed for u in line), default=4.0)
    stats.initiative = sum(u.initiative for u in all_units)
    # Taux de récupération d'organisation : moyenne de tous les bataillons
    # et compagnies (confirmé par le wiki officiel, cf. recherche du 2026-07-16).
    stats.recovery_rate = sum(u.recovery for u in all_units) / len(all_units)
    recon = sum(u.recon for u in all_units)

    # Arrondis d'affichage raisonnables
    for attr in ("hp", "organisation", "soft_attack", "hard_attack", "air_attack",
                 "defense", "breakthrough", "armor", "piercing"):
        setattr(stats, attr, round(getattr(stats, attr), 2))
    stats.hardness = round(stats.hardness, 3)
    stats.recovery_rate = round(stats.recovery_rate, 3)
    return stats, recon
