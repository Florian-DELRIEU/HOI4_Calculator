"""Tests du système de tactiques (jalon 2)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from engine.battle import Battle
from engine.division import DivisionStats, DivisionTemplate
from engine.leader import Leader, LeaderAbility
from engine.params import BattleParams
from engine.tactics import (ActiveTactic, TacticContext, TacticDef,
                            TacticManager, TacticRegistry, eval_condition)
from tests.test_engine import make_template


@pytest.fixture(scope="module")
def registry():
    return TacticRegistry(custom_path=None)


def make_battle(atk_leader=None, def_leader=None, seed=5, n_div=2, **params):
    battle = Battle(BattleParams(**params), attacker_leader=atk_leader,
                    defender_leader=def_leader, seed=seed)
    for _ in range(n_div):
        battle.attacker.add_division(make_template().spawn())
        battle.defender.add_division(make_template().spawn())
    return battle


# ------------------------------------------------------------- registre

def test_registry_loads_official_tables(registry):
    # Les deux « Hold Bridge » sont distincts grâce à la clé (nom, camp, phase)
    keys = [k for k in registry.tactics if k[0] == "Hold Bridge"]
    assert len(keys) >= 3   # default/DEF, seize_bridge/ATK, hold_bridge/DEF
    phases = {k[2] for k in keys}
    assert {"default", "seize_bridge", "hold_bridge"} <= phases


def test_registry_all_phases_covered(registry):
    phases = {t.phase for t in registry.tactics.values()}
    assert phases == {"default", "close_combat", "tactical_withdrawal",
                      "seize_bridge", "hold_bridge", "street_fighting"}


def test_custom_tactic_persistence(tmp_path):
    path = tmp_path / "custom.json"
    reg = TacticRegistry(custom_path=path)
    n_before = len(reg.tactics)
    custom = TacticDef(name="Ma Tactique", side="attacker", phase="default",
                       weight=6, attacker_damage=0.42)
    reg.add_custom(custom)
    assert path.exists()

    reg2 = TacticRegistry(custom_path=path)
    assert len(reg2.tactics) == n_before + 1
    loaded = reg2.tactics[("Ma Tactique", "attacker", "default")]
    assert loaded.custom and loaded.attacker_damage == 0.42

    assert reg2.remove_custom(("Ma Tactique", "attacker", "default"))
    assert len(TacticRegistry(custom_path=path).tactics) == n_before


# --------------------------------------------------------- déclencheurs

def test_trigger_skill_and_traits():
    battle = make_battle(atk_leader=Leader("A", attack_level=2, defense_level=2),
                         def_leader=Leader("D"))
    ctx = TacticContext(battle.attacker, battle)
    assert eval_condition({"skill_gt": 3}, ctx)
    assert not eval_condition({"skill_gt": 4}, ctx)
    assert eval_condition({"skill_advantage_gt": 3}, ctx)
    assert not eval_condition({"trait": "Trickster"}, ctx)
    battle.attacker.leader.traits.append("Trickster")
    assert eval_condition({"trait": "Trickster"}, ctx)


def test_trigger_river_terrain_flags():
    battle = make_battle(small_river=True, terrain_id="urban")
    battle.params.attacker.is_japan = True
    ctx = TacticContext(battle.attacker, battle)
    assert eval_condition({"river": True}, ctx)
    assert eval_condition({"terrain": "urban"}, ctx)
    assert eval_condition({"flag": "is_japan"}, ctx)
    assert not eval_condition({"flag": "masterful_blitz"}, ctx)
    assert eval_condition({"not": {"flag": "masterful_blitz"}}, ctx)


def test_trigger_hardness():
    battle = Battle(BattleParams(), seed=1)
    tank = make_template(hardness=0.8)
    battle.attacker.add_division(tank.spawn())
    battle.defender.add_division(make_template().spawn())
    ctx = TacticContext(battle.attacker, battle)
    assert eval_condition({"hardness_gt": 0.5}, ctx)
    assert not eval_condition({"hardness_gt": 0.9}, ctx)


def test_unknown_condition_disables_tactic():
    battle = make_battle()
    ctx = TacticContext(battle.attacker, battle)
    assert not eval_condition({"condition_inconnue": 1}, ctx)


# ------------------------------------------------------------ initiative

def test_initiative_deterministic_defender_wins_ties(registry):
    manager = TacticManager(registry)
    battle = make_battle()   # compétences égales (0/0)
    from engine.logs import RoundLog
    log = RoundLog(round=1)
    battle.round = 1
    manager.reselect(battle, log)
    assert any("Initiative : Défenseur" in e for e in log.events)


def test_initiative_recon_bonus(registry):
    manager = TacticManager(registry)
    battle = make_battle(atk_leader=Leader("A", attack_level=2),
                         def_leader=Leader("D", attack_level=3))
    # Sans recon, le défenseur gagne (3 > 2). Avec recon, l'attaquant
    # obtient +5 → 7 > 3.
    recon_div = make_template()
    recon_div.recon = 2.0
    battle.attacker.add_division(recon_div.spawn())
    from engine.logs import RoundLog
    log = RoundLog(round=1)
    battle.round = 1
    manager.reselect(battle, log)
    assert any("Initiative : Attaquant" in e for e in log.events)


def test_manual_override(registry):
    manager = TacticManager(registry)
    battle = make_battle()
    battle.attacker.manual_tactic = "Well-Planned Attack"
    from engine.logs import RoundLog
    log = RoundLog(round=1)
    battle.round = 1
    manager.reselect(battle, log)
    tactic = battle.active_tactics["attacker"]
    assert tactic.name == "Well-Planned Attack" and tactic.forced


def test_counter_cancels_effects(registry):
    manager = TacticManager(registry)
    battle = make_battle()
    battle.attacker.manual_tactic = "Attack"          # contrée par Counter-Attack
    battle.defender.manual_tactic = "Counter-Attack"  # contrée par Attack
    from engine.logs import RoundLog
    log = RoundLog(round=1)
    battle.round = 1
    manager.reselect(battle, log)
    atk = battle.active_tactics["attacker"]
    deff = battle.active_tactics["defender"]
    assert atk.countered and deff.countered   # contre mutuel (table CDC)
    assert atk.damage_factor_for("attacker") == 1.0
    assert deff.damage_factor_for("defender") == 1.0


def test_tactic_damage_factors():
    tactic = ActiveTactic(TacticDef(name="X", side="attacker",
                                    attacker_damage=0.25, defender_damage=-0.15))
    assert tactic.damage_factor_for("attacker") == pytest.approx(1.25)
    assert tactic.damage_factor_for("defender") == pytest.approx(0.85)


def test_phase_change_via_forced_tactic(registry):
    manager = TacticManager(registry)
    battle = make_battle(small_river=True,
                         atk_leader=Leader("A", attack_level=5, defense_level=0))
    battle.attacker.manual_tactic = "Seize Bridge"
    from engine.logs import RoundLog
    log = RoundLog(round=1)
    battle.round = 1
    manager.reselect(battle, log)
    assert battle.battle_phase == "seize_bridge"
    # À la re-sélection suivante, les tactiques viennent de la phase en cours
    battle.attacker.manual_tactic = None
    log2 = RoundLog(round=13)
    battle.round = 13
    manager.reselect(battle, log2)
    assert battle.active_tactics["attacker"].tactic.phase == "seize_bridge"


def test_reselection_every_12_rounds():
    battle = make_battle()
    battle.run_rounds(13)
    reselect_rounds = [log.round for log in battle.logs
                       if any("Tactique Attaquant" in e for e in log.events)]
    assert reselect_rounds == [1, 13]


def test_battle_runs_with_tactics_end_to_end():
    battle = make_battle(seed=99)
    battle.run_rounds(24)
    assert battle.active_tactics["attacker"] is not None
    assert battle.active_tactics["defender"] is not None
    assert battle.round == 24 or battle.is_over


def test_preferred_tactic_weight(registry):
    battle = make_battle(atk_leader=Leader("A", preferred_tactic="Shock"))
    ctx = TacticContext(battle.attacker, battle)
    shock = registry.tactics[("Shock", "attacker", "default")]
    base = TacticManager._weight(shock, ctx, battle.defender)   # camp sans préférence
    boosted = TacticManager._weight(shock, ctx, battle.attacker)
    assert boosted == pytest.approx(base * 1.5)


def test_weight_rules_urban_assault(registry):
    assault = registry.tactics[("Assault", "attacker", "default")]
    battle = make_battle(terrain_id="urban",
                         atk_leader=Leader("A", traits=["Aggressive Assaulter"]))
    ctx = TacticContext(battle.attacker, battle)
    # base 0,4 → « set 2 » en urbain → ×2 avec Aggressive Assaulter = 4
    assert TacticManager._weight(assault, ctx, battle.attacker) == pytest.approx(4.0)


# ------------------------------------------------------------ capacités

def test_leader_ability_activation_and_expiry():
    battle = make_battle()
    battle.run_round()
    ability = LeaderAbility(name="Assaut renforcé", attack_bonus=20.0,
                            duration_rounds=2, uses_per_battle=1)
    events = []
    assert battle.attacker.activate_ability(ability, events)
    assert not battle.attacker.activate_ability(ability, events)   # plus d'usage
    from engine import modifiers
    div = battle.attacker.frontline[0]
    entries = dict(modifiers.attack_entries(div, battle.attacker, battle))
    assert entries["Capacité : Assaut renforcé"] == 20.0
    battle.run_rounds(2)
    assert not battle.attacker.active_abilities   # expirée


def test_ability_org_restore():
    battle = make_battle()
    battle.run_rounds(6)
    div = battle.attacker.frontline[0]
    div.current_org = 10.0
    ability = LeaderAbility(name="Dernier carré", org_restore=15.0)
    battle.attacker.activate_ability(ability, [])
    assert div.current_org == 25.0
