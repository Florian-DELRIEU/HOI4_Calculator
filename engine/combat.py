"""Résolution des combats : ciblage (§8.3) et dégâts (§8.4)."""
from __future__ import annotations

from typing import TYPE_CHECKING

from engine import modifiers
from engine.division import Division
from engine.logs import AttackReport
from engine.rng import CombatRNG

if TYPE_CHECKING:
    from engine.battle import Battle, Camp

HP_DAMAGE_COEF = 0.06
ORG_DAMAGE_COEF = 0.053
HIT_CHANCE_DEFENDED = 0.10
HIT_CHANCE_UNDEFENDED = 0.40
BASE_COORDINATED_SHARE = 0.35
MAX_COORDINATED_SHARE = 0.90
FORT_DAMAGE_CHANCE = 0.05      # 5 % par attaque d'endommager le fort (§8.6)


# ------------------------------------------------------------------ ciblage

def build_target_list(division: Division, enemy_frontline: list[Division],
                      rng: CombatRNG) -> None:
    """Construit la liste de cibles d'une division (§8.3).

    Largeur d'engagement = 2 × largeur propre ; les ennemis sont ajoutés en
    ordre aléatoire tant qu'ils tiennent dans la largeur d'engagement. Si
    aucun ne rentre, une cible est choisie au hasard.
    """
    candidates = [d for d in enemy_frontline if d.can_fight]
    division.target_list = []
    division.primary_target = None
    if not candidates:
        return

    engagement_width = 2 * division.stats.width
    order = list(candidates)
    rng.shuffle(order)

    total = 0.0
    targets: list[Division] = []
    for enemy in order:
        if total + enemy.stats.width <= engagement_width:
            targets.append(enemy)
            total += enemy.stats.width
    if not targets:
        targets = [rng.choice(candidates)]

    division.target_list = targets
    division.primary_target = _priority_target(division, targets)


def _priority_target(division: Division, targets: list[Division]) -> Division:
    """Cible prioritaire : maximise le score du CDC §8.3."""

    def score(target: Division) -> float:
        h = target.stats.hardness
        base = (division.stats.soft_attack * (1 - h) * 1.0
                + division.stats.hard_attack * h * 1.2)
        if target.stats.armor > 0 and division.stats.piercing < target.stats.armor:
            base *= 0.5
        return base * (1.0 - target.org_ratio / 4.0)

    return max(targets, key=score)


def coordinated_share(division: Division, camp: "Camp", battle: "Battle") -> float:
    """Part coordonnée = 35 % + coordination × (1 + initiative), plafond 90 %."""
    sp = battle.params.attacker if camp.is_attacker else battle.params.defender
    share = BASE_COORDINATED_SHARE + sp.coordination * (1.0 + division.stats.initiative)
    return min(share, MAX_COORDINATED_SHARE)


# ------------------------------------------------------------------ défense

def compute_defense_pool(division: Division, camp: "Camp", battle: "Battle",
                         rng: CombatRNG) -> None:
    """Nombre de défenses du tour = round_prob(stat défensive modifiée / 10).

    Le défenseur utilise sa ``defense``, l'attaquant sa ``breakthrough``.
    """
    stat = division.stats.defense if not camp.is_attacker else division.stats.breakthrough
    entries = modifiers.defense_entries(division, camp, battle)
    factor = modifiers.combine(entries)
    division.defense_pool = rng.prob_round(stat * factor / 10.0)


# ------------------------------------------------------------------ attaque

def resolve_attacks(division: Division, camp: "Camp", battle: "Battle",
                    rng: CombatRNG) -> list[AttackReport]:
    """Résout toutes les attaques d'une division contre sa liste de cibles."""
    reports: list[AttackReport] = []
    targets = [t for t in division.target_list if not t.is_destroyed]
    if not targets or not division.can_fight:
        return reports

    share_primary = coordinated_share(division, camp, battle)
    total_width = sum(t.stats.width for t in targets) or 1.0

    attack_detail = modifiers.attack_entries(division, camp, battle)
    attack_factor = modifiers.combine(attack_detail)

    tactic_factor, tactic_name = battle.damage_factor_for(camp)

    for target in targets:
        # Répartition : part non coordonnée au prorata des largeurs,
        # part coordonnée entièrement à la cible prioritaire (§8.3).
        share = (1.0 - share_primary) * (target.stats.width / total_width)
        if target is division.primary_target:
            share += share_primary

        h = target.stats.hardness
        base_attack = (division.stats.soft_attack * share * (1 - h)
                       + division.stats.hard_attack * share * h)
        n_attacks = rng.prob_round(base_attack * attack_factor / 10.0)

        # Facteur de dégâts par coup (§8.4.5, §8.4.6, §9.1)
        armor_factor = modifiers.armor_piercing_factor(
            division.stats.piercing, target.stats.armor)
        strength_factor = division.strength_step
        damage_detail = []
        if armor_factor != 1.0:
            damage_detail.append(("Blindage non percé (palier)", armor_factor))
        if strength_factor != 1.0:
            damage_detail.append(("Force de la division", strength_factor))
        if tactic_factor != 1.0:
            damage_detail.append((f"Tactique ({tactic_name})", tactic_factor))
        damage_factor = armor_factor * strength_factor * tactic_factor

        # Dé d'organisation : 1d6 si le blindage de l'attaquant n'est pas
        # percé par la cible (« il bouge plus librement »), sinon 1d4.
        org_die = 6 if (division.stats.armor > 0
                        and division.stats.armor > target.stats.piercing) else 4

        report = AttackReport(
            round=battle.round,
            striker_side="attacker" if camp.is_attacker else "defender",
            striker=division.name,
            target=target.name,
            tactic=tactic_name,
            n_attacks=n_attacks,
            defenses_before=target.defense_pool,
            attack_factor=attack_factor,
            attack_detail=list(attack_detail),
            damage_factor=damage_factor,
            damage_detail=damage_detail,
        )

        hp_dmg = 0.0
        org_dmg = 0.0
        hits = 0
        for _ in range(n_attacks):
            if target.defense_pool > 0:
                target.defense_pool -= 1
                hit_chance = HIT_CHANCE_DEFENDED
            else:
                hit_chance = HIT_CHANCE_UNDEFENDED
            if rng.chance(hit_chance):
                hits += 1
                hp_dmg += rng.die(2) * HP_DAMAGE_COEF * damage_factor
                org_dmg += rng.die(org_die) * ORG_DAMAGE_COEF * damage_factor

        target.take_damage(hp_dmg, org_dmg)
        report.hits = hits
        report.hp_damage = round(hp_dmg, 3)
        report.org_damage = round(org_dmg, 3)
        reports.append(report)

        # Dégâts collatéraux sur le fort (§8.6) : seul l'attaquant érode
        # les fortifications du défenseur.
        if (camp.is_attacker and battle.params.fort_level > 0
                and n_attacks > 0 and rng.chance(FORT_DAMAGE_CHANCE)):
            collateral = 0.1 * division.stats.soft_attack * n_attacks * damage_factor
            battle.apply_fort_damage(collateral)

    return reports
