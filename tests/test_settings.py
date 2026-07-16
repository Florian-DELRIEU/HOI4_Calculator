"""Tests du système de paramètres configurables."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from engine import settings as settings_module
from engine.settings import DEFAULTS, FIELD_META, SETTINGS, Settings


@pytest.fixture(autouse=True)
def restore_settings():
    """Isole chaque test : SETTINGS est un singleton partagé par le moteur."""
    saved = SETTINGS.to_dict()
    yield
    SETTINGS.update_from(saved)


def test_defaults_match_official_constants():
    d = Settings()
    assert d.hp_damage_coef == 0.06
    assert d.org_damage_coef == 0.053
    assert d.hit_chance_defended == 0.10
    assert d.hit_chance_undefended == 0.40
    assert d.reinforce_chance == 0.02
    assert d.tactic_reselect_interval == 12
    assert d.tactics_enabled is True
    assert d.fort_erosion_enabled is True
    assert d.auto_stop_on_victory is True
    assert d.use_fixed_seed is False


def test_field_meta_keys_match_dataclass():
    meta_keys = {m[0] for m in FIELD_META}
    field_keys = set(Settings().to_dict())
    assert meta_keys == field_keys   # tout champ est éditable, et réciproquement


def test_update_from_ignores_unknown_keys():
    s = Settings()
    s.update_from({"hp_damage_coef": 0.2, "cle_inconnue": 999})
    assert s.hp_damage_coef == 0.2
    assert not hasattr(s, "cle_inconnue")


def test_reset_restores_defaults():
    SETTINGS.update_from({"hp_damage_coef": 1.0, "tactics_enabled": False})
    settings_module.reset_to_defaults()
    assert SETTINGS.hp_damage_coef == 0.06
    assert SETTINGS.tactics_enabled is True


def test_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "settings.json"
    SETTINGS.update_from({"hp_damage_coef": 0.5, "fixed_seed": 42,
                          "use_fixed_seed": True, "tactic_reselect_interval": 6})
    settings_module.save(path)

    settings_module.reset_to_defaults()
    assert SETTINGS.hp_damage_coef == 0.06

    settings_module.load(path)
    assert SETTINGS.hp_damage_coef == 0.5
    assert SETTINGS.fixed_seed == 42
    assert SETTINGS.use_fixed_seed is True
    assert SETTINGS.tactic_reselect_interval == 6


def test_load_missing_file_is_noop(tmp_path):
    settings_module.load(tmp_path / "absent.json")
    assert SETTINGS.hp_damage_coef == 0.06   # inchangé


# --------------------------------- effet réel sur le moteur

def _one_round_damage(seed):
    from engine.battle import Battle
    from engine.params import BattleParams
    from tests.test_engine import make_template
    battle = Battle(BattleParams(), seed=seed, use_tactics=False)
    battle.attacker.add_division(make_template(soft=200, org=80).spawn())
    battle.defender.add_division(make_template(defense=30, org=80).spawn())
    battle.run_round()
    target = battle.defender.divisions[0]
    return target.stats.hp - target.current_hp   # PV perdus par le défenseur


def test_hp_damage_coef_scales_engine_damage():
    settings_module.reset_to_defaults()
    base = _one_round_damage(seed=7)
    SETTINGS.hp_damage_coef = 0.60   # ×10 le coefficient officiel
    boosted = _one_round_damage(seed=7)
    assert boosted > base * 5   # même graine, dégâts nettement plus élevés


def test_reselect_interval_setting_controls_tactics_cadence():
    from engine.battle import Battle
    from engine.params import BattleParams
    from tests.test_engine import make_template

    settings_module.reset_to_defaults()
    SETTINGS.tactic_reselect_interval = 3
    battle = Battle(BattleParams(), seed=5)
    for _ in range(2):
        battle.attacker.add_division(make_template().spawn())
        battle.defender.add_division(make_template().spawn())
    battle.run_rounds(7)
    reselect_rounds = [log.round for log in battle.logs
                       if any("Tactique Attaquant" in e for e in log.events)]
    assert reselect_rounds == [1, 4, 7]   # tous les 3 tours


def test_tactics_disabled_setting():
    from engine.battle import Battle
    from engine.params import BattleParams
    from tests.test_engine import make_template
    battle = Battle(BattleParams(), seed=1, use_tactics=False)
    battle.attacker.add_division(make_template().spawn())
    battle.defender.add_division(make_template().spawn())
    battle.run_round()
    assert battle.active_tactics["attacker"] is None
    assert battle.active_tactics["defender"] is None


def test_disabling_tactics_setting_affects_running_battle():
    """Régression : désactiver les tactiques doit stopper immédiatement les
    re-sélections d'une bataille DÉJÀ en cours (le gestionnaire existe mais
    le paramètre le neutralise en temps réel)."""
    from engine.battle import Battle
    from engine.params import BattleParams
    from tests.test_engine import make_template

    settings_module.reset_to_defaults()   # tactics_enabled = True
    battle = Battle(BattleParams(), seed=3, use_tactics=True)
    for _ in range(2):
        battle.attacker.add_division(make_template().spawn())
        battle.defender.add_division(make_template().spawn())
    battle.run_round()
    assert battle.active_tactics["attacker"] is not None   # tactiques actives

    SETTINGS.tactics_enabled = False       # désactivation en cours de bataille
    battle.run_round()
    assert battle.active_tactics["attacker"] is None
    assert battle.active_tactics["defender"] is None

    # Aucune nouvelle sélection de tactique aux périodes suivantes
    battle.run_rounds(13)
    later = battle.logs[-1]
    assert battle.active_tactics["attacker"] is None
    assert not any("Tactique Attaquant" in e
                   for log in battle.logs[2:] for e in log.events)
