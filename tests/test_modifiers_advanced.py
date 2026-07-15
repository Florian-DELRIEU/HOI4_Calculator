"""Tests jalon 4 : météo, aviation, ravitaillement, érosion de fort."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from engine import modifiers
from engine.battle import FORT_INTEGRITY_PER_LEVEL, Battle
from engine.params import BattleParams
from tests.test_engine import _battle_with_divisions, make_template


def test_weather_deep_snow_penalties():
    battle = _battle_with_divisions(weather_id="deep_snow")
    battle.run_round()
    div = battle.attacker.frontline[0]
    atk = dict(modifiers.attack_entries(div, battle.attacker, battle))
    assert atk["Météo (Neige profonde)"] == pytest.approx(-40.0)
    # La percée de l'attaquant subit le modificateur breakthrough (−30 %)
    deff = dict(modifiers.defense_entries(div, battle.attacker, battle))
    assert deff["Météo (Neige profonde)"] == pytest.approx(-30.0)


def test_weather_flood_boosts_defender():
    battle = _battle_with_divisions(weather_id="flood")
    battle.run_round()
    div = battle.defender.frontline[0]
    entries = dict(modifiers.defense_entries(div, battle.defender, battle))
    assert entries["Météo (Inondation)"] == pytest.approx(50.0)


def test_enemy_air_superiority_terrain_mitigation():
    # En urbain, la supériorité aérienne ennemie est atténuée de 50 %
    battle = _battle_with_divisions(terrain_id="urban")
    battle.params.attacker.enemy_air_superiority = 0.35
    battle.run_round()
    div = battle.attacker.frontline[0]
    entries = dict(modifiers.attack_entries(div, battle.attacker, battle))
    assert entries["Supériorité aérienne ennemie"] == pytest.approx(-17.5)


def test_supply_shortage_asymmetric():
    battle = _battle_with_divisions()
    battle.params.attacker.supply_shortage = 1.0
    battle.params.defender.supply_shortage = 1.0
    battle.run_round()
    atk_div = battle.attacker.frontline[0]
    def_div = battle.defender.frontline[0]
    atk_attack = dict(modifiers.attack_entries(atk_div, battle.attacker, battle))
    atk_defense = dict(modifiers.defense_entries(atk_div, battle.attacker, battle))
    def_attack = dict(modifiers.attack_entries(def_div, battle.defender, battle))
    def_defense = dict(modifiers.defense_entries(def_div, battle.defender, battle))
    assert atk_attack["Manque de ravitaillement"] == pytest.approx(-25.0)
    assert atk_defense["Manque de ravitaillement"] == pytest.approx(-65.0)
    assert def_attack["Manque de ravitaillement"] == pytest.approx(-35.0)
    assert def_defense["Manque de ravitaillement"] == pytest.approx(-15.0)


def test_paradrop_penalty_expires():
    battle = _battle_with_divisions()
    battle.run_round()
    div = battle.attacker.frontline[0]
    div.paradropped_rounds_left = 2
    entries = dict(modifiers.attack_entries(div, battle.attacker, battle))
    assert entries["Parachutage récent"] == pytest.approx(-30.0)
    battle.run_rounds(2)
    entries = dict(modifiers.attack_entries(div, battle.attacker, battle))
    assert "Parachutage récent" not in entries


def test_fort_erosion_reduces_level():
    battle = Battle(BattleParams(fort_level=2), seed=3)
    battle.attacker.add_division(make_template(soft=400).spawn())
    battle.defender.add_division(make_template(defense=400, org=500, hp=5000).spawn())
    battle.apply_fort_damage(FORT_INTEGRITY_PER_LEVEL + 1)
    assert battle.params.fort_level == 1
    battle.apply_fort_damage(FORT_INTEGRITY_PER_LEVEL * 3)
    assert battle.params.fort_level == 0


def test_fort_erodes_during_long_battle():
    battle = Battle(BattleParams(fort_level=1), seed=8)
    battle.attacker.add_division(make_template(soft=600, org=2000, hp=5000).spawn())
    battle.defender.add_division(make_template(defense=100, org=2000, hp=5000).spawn())
    battle.run_rounds(300)
    assert battle.params.fort_level == 0
    assert any("fortifications" in e for log in battle.logs for e in log.events)
