"""Cumul des modificateurs de combat (CDC §8.5).

Tous les modificateurs se cumulent **multiplicativement** : chaque entrée
est un pourcentage relatif (ex. −15 pour −15 %) et le facteur final vaut
``max(prod(1 + p/100), 0.01)`` — plancher à 1 %, jamais négatif ni nul.

Chaque fonction renvoie ``(facteur, détail)`` où ``détail`` est la liste
``[(libellé, pourcentage), …]`` utilisée par les logs et les tooltips.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # imports uniquement pour l'annotation, pas à l'exécution
    from engine.battle import Battle, Camp
    from engine.division import Division

MIN_FACTOR = 0.01

# Pénalités maximales de pénurie de ravitaillement (§8.5)
SUPPLY_ATTACK_MAX = {"attacker": -25.0, "defender": -35.0}
SUPPLY_DEFENSE_MAX = {"attacker": -65.0, "defender": -15.0}

NIGHT_PENALTY = -50.0
ENCIRCLEMENT_PENALTY = -30.0
PARADROP_PENALTY = -30.0
NAVAL_INVASION_PENALTY = -50.0
FORT_PENALTY_PER_LEVEL = -15.0
ENTRENCHMENT_PER_POINT = 2.0
LEADER_SKILL_PER_POINT = 2.5


def combine(entries: list[tuple[str, float]]) -> float:
    """Cumul multiplicatif d'une liste de pourcentages, plancher 1 %."""
    factor = 1.0
    for _, pct in entries:
        factor *= 1.0 + pct / 100.0
    return max(factor, MIN_FACTOR)


def _common_entries(division: "Division", camp: "Camp", battle: "Battle",
                    is_attack_stat: bool) -> list[tuple[str, float]]:
    """Modificateurs communs aux deux camps."""
    entries: list[tuple[str, float]] = []
    side = "attacker" if camp.is_attacker else "defender"
    sp = battle.params.attacker if camp.is_attacker else battle.params.defender

    # Expérience de la division
    if division.experience_bonus:
        entries.append((f"Expérience ({division.experience})", division.experience_bonus))

    # Compétence du commandant (+2,5 %/pt)
    if camp.leader is not None:
        lvl = camp.leader.attack_level if is_attack_stat else camp.leader.defense_level
        if lvl:
            entries.append(("Compétence du commandant", LEADER_SKILL_PER_POINT * lvl))

    # Ravitaillement
    if sp.supply_shortage > 0:
        max_pen = SUPPLY_ATTACK_MAX[side] if is_attack_stat else SUPPLY_DEFENSE_MAX[side]
        entries.append(("Manque de ravitaillement", max_pen * sp.supply_shortage))

    # Capacités de leader activées (§5)
    for ability, _rounds_left in camp.active_abilities:
        bonus = ability.attack_bonus if is_attack_stat else ability.defense_bonus
        if bonus:
            entries.append((f"Capacité : {ability.name}", bonus))

    # Renseignement et bonus de nation
    if is_attack_stat:
        if sp.intel_advantage:
            entries.append(("Avantage de renseignement", sp.intel_advantage * 100))
        if sp.nation_attack_bonus:
            entries.append(("Bonus de nation", sp.nation_attack_bonus * 100))
        if sp.air_support_bonus:
            entries.append(("Soutien aérien", sp.air_support_bonus * 100))
    else:
        if sp.nation_defense_bonus:
            entries.append(("Bonus de nation", sp.nation_defense_bonus * 100))

    return entries


def attack_entries(division: "Division", camp: "Camp", battle: "Battle") -> list[tuple[str, float]]:
    """Modificateurs appliqués aux stats d'attaque (soft/hard attack)."""
    p = battle.params
    sp = p.attacker if camp.is_attacker else p.defender
    entries = _common_entries(division, camp, battle, is_attack_stat=True)

    # Nuit : −50 % pour les deux camps, atténuable
    if p.is_night:
        entries.append(("Nuit", NIGHT_PENALTY * (1.0 - sp.night_attack_bonus)))

    # Supériorité aérienne ennemie, atténuée par le terrain
    if sp.enemy_air_superiority > 0:
        pen = sp.enemy_air_superiority * (1.0 - p.terrain.enemy_air_mitigation)
        entries.append(("Supériorité aérienne ennemie", -pen * 100))

    # Météo (attaque)
    if p.weather.attack:
        entries.append((f"Météo ({p.weather.nom})", p.weather.attack * 100))

    if camp.is_attacker:
        # Terrain du défenseur
        if p.terrain.attack_modifier:
            entries.append((f"Terrain ({p.terrain.nom})", p.terrain.attack_modifier * 100))
        # Rivières
        if p.large_river:
            entries.append(("Grande rivière", -60.0))
        elif p.small_river:
            entries.append(("Petite rivière", -30.0))
        # Débarquement amphibie
        if p.naval_invasion:
            entries.append(("Débarquement amphibie", NAVAL_INVASION_PENALTY))
        # Fort (niveaux annulés par les directions supplémentaires)
        if p.effective_fort_level:
            entries.append((f"Fort niveau {p.effective_fort_level}",
                            FORT_PENALTY_PER_LEVEL * p.effective_fort_level))
        # Bonus de planification
        if p.planning_bonus:
            entries.append(("Bonus de planification", p.planning_bonus * 100))
    else:
        # Défenseur encerclé : pénalise aussi ses stats
        if p.encirclement:
            entries.append(("Encerclement", ENCIRCLEMENT_PENALTY))

    # Parachutage récent (−30 % pendant 48 h)
    if division.paradropped_rounds_left > 0:
        entries.append(("Parachutage récent", PARADROP_PENALTY))

    # Pénalités de largeur / empilement du camp
    if camp.width_penalty:
        entries.append(("Dépassement de largeur", camp.width_penalty))
    if camp.stacking_penalty:
        entries.append(("Empilement", camp.stacking_penalty))

    return entries


def defense_entries(division: "Division", camp: "Camp", battle: "Battle") -> list[tuple[str, float]]:
    """Modificateurs appliqués à la stat défensive : ``defense`` pour le
    défenseur, ``breakthrough`` (percée) pour l'attaquant."""
    p = battle.params
    entries = _common_entries(division, camp, battle, is_attack_stat=False)

    if camp.is_attacker:
        # La percée de l'attaquant subit terrain, rivières, fort, météo (§7.1, §7.2)
        if p.terrain.attack_modifier:
            entries.append((f"Terrain ({p.terrain.nom})", p.terrain.attack_modifier * 100))
        if p.large_river:
            entries.append(("Grande rivière", -60.0))
        elif p.small_river:
            entries.append(("Petite rivière", -30.0))
        if p.naval_invasion:
            entries.append(("Débarquement amphibie", NAVAL_INVASION_PENALTY))
        if p.effective_fort_level:
            entries.append((f"Fort niveau {p.effective_fort_level}",
                            FORT_PENALTY_PER_LEVEL * p.effective_fort_level))
        if p.weather.breakthrough:
            entries.append((f"Météo ({p.weather.nom})", p.weather.breakthrough * 100))
    else:
        # Retranchement (+2 %/pt)
        if p.entrenchment:
            entries.append(("Retranchement", ENTRENCHMENT_PER_POINT * p.entrenchment))
        # Encerclement (−30 %)
        if p.encirclement:
            entries.append(("Encerclement", ENCIRCLEMENT_PENALTY))
        # Météo (défense, ex. inondation +50 %)
        if p.weather.defense:
            entries.append((f"Météo ({p.weather.nom})", p.weather.defense * 100))

    if division.paradropped_rounds_left > 0:
        entries.append(("Parachutage récent", PARADROP_PENALTY))

    return entries


def armor_piercing_factor(attacker_piercing: float, target_armor: float) -> float:
    """Facteur de dégâts par palier selon le ratio piercing/armor (§8.4.5).

    Remplace la division par 2 forfaitaire du projet de référence.
    """
    if target_armor <= 0:
        return 1.0
    ratio = attacker_piercing / target_armor
    if ratio >= 1.0:
        return 1.0
    if ratio >= 0.75:
        return 0.8
    if ratio >= 0.5:
        return 0.65
    return 0.5
