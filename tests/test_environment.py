"""Tests du cycle jour/nuit et de la météo dynamique."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from engine import settings as settings_module
from engine.battle import Battle
from engine.gamedata import WEATHER, WEATHER_TRANSITIONS
from engine.params import BattleParams
from engine.settings import SETTINGS
from tests.test_engine import make_template


@pytest.fixture(autouse=True)
def restore_settings():
    saved = SETTINGS.to_dict()
    yield
    SETTINGS.update_from(saved)


def _battle(seed=1, **params):
    battle = Battle(BattleParams(**params), seed=seed, use_tactics=False)
    battle.attacker.add_division(make_template().spawn())
    battle.defender.add_division(make_template().spawn())
    return battle


# ---------------------------------------------------- cycle jour/nuit

def test_night_window_is_18h_to_6h():
    assert Battle._is_night_at(18) is True
    assert Battle._is_night_at(23) is True
    assert Battle._is_night_at(0) is True
    assert Battle._is_night_at(5) is True
    assert Battle._is_night_at(6) is False    # lever du jour
    assert Battle._is_night_at(12) is False
    assert Battle._is_night_at(17) is False
    # Exactement 12 heures de nuit sur 24
    assert sum(Battle._is_night_at(h) for h in range(24)) == 12


def test_current_hour_advances_from_start_hour():
    SETTINGS.day_night_cycle_enabled = True
    SETTINGS.battle_start_hour = 8
    battle = _battle()
    assert battle.current_hour == 8      # round 0, avant le 1er tour
    battle.run_round()
    assert battle.current_hour == 8      # tour 1 = heure de départ
    battle.run_round()
    assert battle.current_hour == 9


def test_day_night_cycle_sets_is_night_from_hour():
    SETTINGS.day_night_cycle_enabled = True
    SETTINGS.battle_start_hour = 17      # jour ; la nuit tombe au tour 2 (18 h)
    battle = _battle(is_night=False)
    battle.run_round()
    assert battle.params.is_night is False   # 17 h = jour
    log = battle.run_round()
    assert battle.params.is_night is True    # 18 h = nuit
    assert any("nuit tombe" in e for e in log.events)


def test_day_night_disabled_leaves_manual_is_night():
    SETTINGS.day_night_cycle_enabled = False
    battle = _battle(is_night=True)
    battle.run_round()
    assert battle.params.is_night is True    # non touché par le cycle


def test_dawn_event_logged():
    SETTINGS.day_night_cycle_enabled = True
    SETTINGS.battle_start_hour = 5           # nuit ; le jour se lève au tour 2 (6 h)
    battle = _battle(is_night=True)
    battle.run_round()
    log = battle.run_round()
    assert battle.params.is_night is False
    assert any("jour se lève" in e for e in log.events)


# ------------------------------------------------------ météo dynamique

def test_weather_transitions_cover_all_conditions():
    # Chaque météo a une table de transition, ne pointant que vers des météos connues
    for src, weights in WEATHER_TRANSITIONS.items():
        assert src in WEATHER
        assert weights, f"transitions vides pour {src}"
        for dst in weights:
            assert dst in WEATHER, f"cible inconnue {dst} depuis {src}"


def test_dynamic_weather_rerolls_on_period():
    SETTINGS.dynamic_weather_enabled = True
    SETTINGS.weather_change_period = 3
    battle = _battle(seed=5, weather_id="clear")
    # Le tour 1 conserve la météo de départ
    battle.run_round()
    assert battle.round == 1
    # Sur de nombreux tours, la météo doit avoir changé au moins une fois
    seen = {battle.params.weather_id}
    for _ in range(60):
        battle.run_round()
        seen.add(battle.params.weather_id)
    assert len(seen) > 1, "la météo dynamique n'a jamais changé"


def test_dynamic_weather_disabled_keeps_weather_fixed():
    SETTINGS.dynamic_weather_enabled = False
    battle = _battle(weather_id="rain")
    for _ in range(50):
        battle.run_round()
    assert battle.params.weather_id == "rain"


def test_weather_change_is_deterministic_with_seed():
    SETTINGS.dynamic_weather_enabled = True
    SETTINGS.weather_change_period = 2

    def play(seed):
        battle = _battle(seed=seed, weather_id="clear")
        seq = []
        for _ in range(40):
            battle.run_round()
            seq.append(battle.params.weather_id)
        return seq

    assert play(123) == play(123)


def test_roll_weather_unknown_condition_is_stable():
    SETTINGS.dynamic_weather_enabled = True
    battle = _battle(weather_id="clear")
    battle.params.weather_id = "condition_bidon"
    assert battle._roll_weather() == "condition_bidon"   # pas de plantage


def test_environment_snapshot_shows_hour_when_cycle_on():
    SETTINGS.day_night_cycle_enabled = True
    SETTINGS.battle_start_hour = 20
    battle = _battle()
    battle.run_round()
    snap = battle.environment_snapshot()
    assert "Heure : 20 h (Nuit)" in snap
