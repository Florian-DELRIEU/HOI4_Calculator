"""Tests du moteur de combat (jalon 1)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from engine import modifiers
from engine.battle import Battle, Camp
from engine.division import Division, DivisionStats, DivisionTemplate
from engine.leader import Leader
from engine.params import BattleParams, SideParams
from engine.rng import CombatRNG
from persistence.divisions import (DivisionStore, template_from_dict,
                                   template_to_dict)


def make_template(name="Test", hp=100, org=50, soft=100, hard=10, defense=150,
                  brk=30, armor=0, piercing=5, hardness=0.0, width=20,
                  initiative=0.0, experience="trained", recon=0.0):
    stats = DivisionStats(hp=hp, organisation=org, soft_attack=soft,
                          hard_attack=hard, defense=defense, breakthrough=brk,
                          armor=armor, piercing=piercing, hardness=hardness,
                          width=width, initiative=initiative)
    return DivisionTemplate(name=name, stats=stats, experience=experience, recon=recon)


# ------------------------------------------------------------------- RNG

def test_prob_round_integer_stays_exact():
    rng = CombatRNG(1)
    assert all(rng.prob_round(7.0) == 7 for _ in range(50))
    assert rng.prob_round(0) == 0
    assert rng.prob_round(-3) == 0


def test_prob_round_is_probabilistic():
    rng = CombatRNG(42)
    draws = [rng.prob_round(3.5) for _ in range(4000)]
    assert set(draws) == {3, 4}
    mean = sum(draws) / len(draws)
    assert 3.45 < mean < 3.55  # espérance = 3,5


# -------------------------------------------------------------- paliers

def test_armor_piercing_tiers():
    f = modifiers.armor_piercing_factor
    assert f(10, 0) == 1.0        # cible sans blindage
    assert f(10, 10) == 1.0       # ratio 100 %
    assert f(8, 10) == 0.8        # ratio 80 %
    assert f(7.5, 10) == 0.8      # ratio 75 % pile
    assert f(6, 10) == 0.65       # ratio 60 %
    assert f(5, 10) == 0.65       # ratio 50 % pile
    assert f(4.9, 10) == 0.5      # ratio < 50 %


def test_combine_multiplicative_and_floor():
    assert modifiers.combine([("a", -50.0), ("b", -50.0)]) == pytest.approx(0.25)
    assert modifiers.combine([("a", 25.0), ("b", 20.0)]) == pytest.approx(1.5)
    # plancher à 1 % : jamais négatif ni nul
    assert modifiers.combine([("a", -90.0), ("b", -90.0), ("c", -90.0)]) == 0.01
    assert modifiers.combine([("a", -100.0)]) == 0.01


def test_strength_step_by_10_percent():
    div = make_template(hp=100).spawn()
    assert div.strength_step == 1.0
    div.current_hp = 95
    assert div.strength_step == pytest.approx(0.9)
    div.current_hp = 90
    assert div.strength_step == pytest.approx(0.9)
    div.current_hp = 41
    assert div.strength_step == pytest.approx(0.4)
    div.current_hp = 3
    assert div.strength_step == pytest.approx(0.1)  # plancher


# ---------------------------------------------------------------- fort

def test_effective_fort_level_extra_directions():
    p = BattleParams(fort_level=4, extra_directions=2)
    assert p.effective_fort_level == 2
    p = BattleParams(fort_level=2, extra_directions=5)
    assert p.effective_fort_level == 1    # jamais le dernier niveau
    p = BattleParams(fort_level=0, extra_directions=3)
    assert p.effective_fort_level == 0


def test_base_combat_width_uses_terrain_extra():
    p = BattleParams(terrain_id="plains", extra_directions=2)
    assert p.base_combat_width == 70 + 2 * 35
    p = BattleParams(terrain_id="mountain", extra_directions=1)
    assert p.base_combat_width == 50 + 25


def test_combat_width_manual_override():
    p = BattleParams(terrain_id="mountain", extra_directions=2)
    assert p.base_combat_width == 50 + 2 * 25   # auto
    p.combat_width_override = 120
    assert p.base_combat_width == 120           # imposé, terrain/directions ignorés
    p.combat_width_override = 0
    assert p.base_combat_width == 50 + 2 * 25   # 0 = retour à l'auto


# ----------------------------------------------------------- pénalités

def _battle_with_divisions(n_att=1, n_def=1, width=20, seed=7, **params):
    battle = Battle(BattleParams(**params), seed=seed)
    for _ in range(n_att):
        battle.attacker.add_division(make_template(width=width).spawn())
    for _ in range(n_def):
        battle.defender.add_division(make_template(width=width).spawn())
    return battle


def test_width_penalty_capped():
    battle = _battle_with_divisions()
    camp = battle.attacker
    for _ in range(10):
        camp.frontline.append(make_template(width=20).spawn())
    camp.compute_penalties(battle)   # 220 de largeur pour 70 → plafonné
    assert camp.width_penalty == -33.0


def test_stacking_penalty():
    battle = _battle_with_divisions(extra_directions=1)   # limite = 8
    camp = battle.attacker
    for _ in range(10):
        camp.frontline.append(make_template(width=5).spawn())
    camp.compute_penalties(battle)
    assert camp.stacking_penalty == -4.0   # 10 divisions, 2 au-delà de 8


def test_deploy_respects_width_limit():
    battle = _battle_with_divisions(n_att=8, n_def=1, width=20)  # 8×20=160 > 1,33×70
    battle.run_round()
    assert battle.attacker.frontline_width <= 1.33 * 70 + 20
    assert battle.attacker.reserves   # au moins une division en réserve


def test_force_to_reserve_moves_division_and_preserves_state():
    battle = _battle_with_divisions()
    battle.run_round()
    camp = battle.attacker
    division = camp.frontline[0]
    division.current_hp = 12.5
    division.current_org = 3.0

    assert camp.force_to_reserve(division) is True
    assert division not in camp.frontline
    assert division in camp.reserves
    assert division.in_frontline is False
    assert division.current_hp == 12.5   # état préservé, pas réinitialisé
    assert division.current_org == 3.0


def test_force_to_reserve_no_op_if_not_in_frontline():
    battle = _battle_with_divisions()
    battle.run_round()
    outsider = make_template().spawn()   # jamais ajoutée à ce camp
    assert outsider not in battle.attacker.frontline
    assert battle.attacker.force_to_reserve(outsider) is False


def test_force_to_frontline_from_reserve():
    battle = _battle_with_divisions(n_att=8, n_def=1, width=20)  # surcharge → réserve
    battle.run_round()
    camp = battle.attacker
    assert camp.reserves
    division = camp.reserves[0]
    assert camp.force_to_frontline(division) is True
    assert division in camp.frontline
    assert division not in camp.reserves
    assert division.in_frontline is True


def test_force_to_frontline_from_retreated():
    battle = _battle_with_divisions()
    battle.run_round()
    camp = battle.attacker
    division = camp.frontline[0]
    camp.frontline.remove(division)
    camp.retreated.append(division)
    assert camp.force_to_frontline(division) is True
    assert division in camp.frontline
    assert division not in camp.retreated


def test_force_to_frontline_no_op_if_already_front_or_foreign():
    battle = _battle_with_divisions()
    battle.run_round()
    camp = battle.attacker
    assert camp.force_to_frontline(camp.frontline[0]) is False   # déjà au front
    assert camp.force_to_frontline(make_template().spawn()) is False  # étrangère


# ------------------------------------------------------------- ciblage

def test_targeting_engagement_width():
    from engine.combat import build_target_list
    rng = CombatRNG(3)
    div = make_template(width=10).spawn()      # engagement = 20
    enemies = [make_template(name=f"E{i}", width=10).spawn() for i in range(5)]
    build_target_list(div, enemies, rng)
    assert 1 <= len(div.target_list) <= 2
    assert div.primary_target in div.target_list


def test_targeting_fallback_random_choice():
    from engine.combat import build_target_list
    rng = CombatRNG(3)
    div = make_template(width=10).spawn()      # engagement = 20
    enemies = [make_template(name="Grosse", width=50).spawn()]
    build_target_list(div, enemies, rng)
    assert div.target_list == enemies


def test_priority_target_prefers_low_org_and_soft():
    from engine.combat import _priority_target
    div = make_template(soft=200, hard=10, piercing=0).spawn()
    weak = make_template(name="Faible", hardness=0.0).spawn()
    weak.current_org = 5
    strong = make_template(name="Forte", hardness=0.0).spawn()
    assert _priority_target(div, [weak, strong]) is weak


# --------------------------------------------------------- modificateurs

def test_attacker_terrain_and_fort_penalties():
    battle = _battle_with_divisions(terrain_id="mountain", fort_level=2)
    battle.run_round()
    div = battle.attacker.frontline[0]
    entries = modifiers.attack_entries(div, battle.attacker, battle)
    labels = {label for label, _ in entries}
    assert any("Terrain" in lab for lab in labels)
    assert any("Fort" in lab for lab in labels)
    values = dict(entries)
    assert values[next(lab for lab in labels if "Terrain" in lab)] == -50.0
    assert values[next(lab for lab in labels if "Fort" in lab)] == -30.0


def test_defender_entrenchment_and_encirclement():
    battle = _battle_with_divisions(entrenchment=5, encirclement=True)
    battle.run_round()
    div = battle.defender.frontline[0]
    entries = dict(modifiers.defense_entries(div, battle.defender, battle))
    assert entries["Retranchement"] == 10.0
    assert entries["Encerclement"] == -30.0


def test_night_penalty_mitigation():
    battle = _battle_with_divisions(is_night=True)
    battle.params.attacker.night_attack_bonus = 0.5
    battle.run_round()
    div = battle.attacker.frontline[0]
    entries = dict(modifiers.attack_entries(div, battle.attacker, battle))
    assert entries["Nuit"] == -25.0   # −50 % atténué de moitié


def test_leader_skill_bonus():
    battle = Battle(BattleParams(), attacker_leader=Leader("Général", attack_level=4))
    battle.attacker.add_division(make_template().spawn())
    battle.defender.add_division(make_template().spawn())
    battle.run_round()
    div = battle.attacker.frontline[0]
    entries = dict(modifiers.attack_entries(div, battle.attacker, battle))
    assert entries["Compétence du commandant"] == 10.0


# ------------------------------------------------------------ bataille

def test_full_battle_deterministic_with_seed():
    def play(seed):
        battle = _battle_with_divisions(n_att=2, n_def=2, seed=seed)
        battle.run_rounds(30)
        return [(d.current_hp, d.current_org)
                for d in battle.attacker.divisions + battle.defender.divisions]

    assert play(123) == play(123)
    assert play(123) != play(456)


def test_battle_ends_when_side_breaks():
    battle = Battle(BattleParams(), seed=11)
    battle.attacker.add_division(make_template(soft=800, defense=400, brk=400, org=80).spawn())
    battle.defender.add_division(make_template(soft=20, defense=30, org=10).spawn())
    battle.run_rounds(500)
    assert battle.result == "attacker"
    assert battle.defender.retreated or battle.defender.destroyed


def test_run_rounds_stops_after_end():
    battle = Battle(BattleParams(), seed=11)
    battle.attacker.add_division(make_template(soft=800, org=80).spawn())
    battle.defender.add_division(make_template(soft=20, defense=30, org=10).spawn())
    battle.run_rounds(500)
    played = battle.round
    battle.run_rounds(10)
    assert battle.round == played   # plus aucun tour joué après la fin


def test_victory_balance_bounds():
    battle = _battle_with_divisions(n_att=2, n_def=2)
    assert battle.victory_balance() == pytest.approx(0.5)
    battle.run_rounds(20)
    assert 0.0 <= battle.victory_balance() <= 1.0


def test_victory_balance_reaches_100_percent_when_enemy_fully_retreated():
    """Une division repliée garde souvent l'essentiel de ses PV (elle se
    replie quand son ORGANISATION tombe à 0, pas ses PV) : la barre
    d'équilibre ne doit pas rester bloquée à mi-chemin sous prétexte que
    ces PV comptent encore — reproduit le cas signalé par Florian."""
    battle = _battle_with_divisions(n_att=1, n_def=1, seed=1)
    defender_div = battle.defender.divisions[0]
    attacker_div = battle.attacker.divisions[0]
    battle.run_round()   # déploiement

    # Le défenseur se replie : plus d'organisation, mais encore ~85 % de PV
    battle.defender.frontline.remove(defender_div)
    battle.defender.retreated.append(defender_div)
    defender_div.current_org = 0.0
    defender_div.current_hp = 0.85 * defender_div.stats.hp

    assert battle.victory_balance() == pytest.approx(1.0)


def test_active_hp_pool_excludes_retreated_but_hp_pool_keeps_them():
    battle = _battle_with_divisions(n_att=1, n_def=1, seed=1)
    battle.run_round()
    division = battle.defender.divisions[0]
    battle.defender.frontline.remove(division)
    battle.defender.retreated.append(division)
    division.current_hp = 42.0

    active_cur, active_tot = battle.defender.active_hp_pool()
    full_cur, full_tot = battle.defender.hp_pool()
    assert active_cur == 0.0            # plus aucune division active
    assert active_tot == full_tot       # même dénominateur (composition totale)
    assert full_cur == pytest.approx(42.0)   # hp_pool() la compte toujours


# ---------------------------------------------------------- persistance

LEGACY_ENTRY = {
    "Nom de Template": "Infanterie 36",
    "PV": 176.2,
    "Organisation": 46.6,
    "Soft Attack": 97.0,
    "Hard Attack": 11.0,
    "Defense": 181.7,
    "Attaque": 34.1,
    "Piercing": 4.5,
    "Armor": 0.0,
    "Hardness": 0.0,
    "Width": 40,
    "Initiative": 0.05,
}


def test_legacy_template_loading():
    template = template_from_dict(LEGACY_ENTRY)
    assert template.name == "Infanterie 36"
    assert template.stats.hp == 176.2
    assert template.stats.breakthrough == 34.1   # « Attaque » = percée
    assert template.stats.width == 40
    assert template.experience == "regular"      # défaut


def test_template_roundtrip_keeps_legacy_keys():
    template = template_from_dict(LEGACY_ENTRY)
    data = template_to_dict(template)
    for key, value in LEGACY_ENTRY.items():
        assert data[key] == value
    assert data["Experience"] == "regular"


def test_division_store(tmp_path):
    store = DivisionStore(tmp_path)
    template = template_from_dict(LEGACY_ENTRY)
    store.save(template)
    assert [t.name for t in store.list_templates()] == ["Infanterie 36"]

    store.duplicate("Infanterie 36")
    assert len(store.list_templates()) == 2

    assert store.rename("Infanterie 36 (copie)", "Infanterie 39")
    names = {t.name for t in store.list_templates()}
    assert names == {"Infanterie 36", "Infanterie 39"}

    assert store.delete("Infanterie 39")
    assert len(store.list_templates()) == 1


def test_import_legacy_array_file(tmp_path):
    legacy = tmp_path / "divisions.json"
    legacy.write_text(json.dumps([LEGACY_ENTRY,
                                  {**LEGACY_ENTRY, "Nom de Template": "Blindés 36"}]),
                      encoding="utf-8")
    store = DivisionStore(tmp_path / "store")
    assert store.import_legacy_file(legacy) == 2
    assert {t.name for t in store.list_templates()} == {"Infanterie 36", "Blindés 36"}
