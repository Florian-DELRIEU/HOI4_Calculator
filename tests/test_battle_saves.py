"""Tests jalon 5 : sauvegardes de bataille nommées et export CSV."""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from engine.battle import Battle
from engine.leader import Leader, LeaderAbility
from engine.params import BattleParams
from persistence.battles import BattleSaveStore, battle_from_dict, battle_to_dict
from persistence.csv_export import export_battle_csv
from tests.test_engine import make_template


def make_running_battle(seed=42):
    battle = Battle(BattleParams(terrain_id="hills", fort_level=3,
                                 entrenchment=4, is_night=True),
                    attacker_leader=Leader("Von Test", attack_level=3,
                                           traits=["Panzer Leader"],
                                           preferred_tactic="Blitz",
                                           abilities=[LeaderAbility("Assaut", attack_bonus=10)]),
                    defender_leader=Leader("Defensor", defense_level=2),
                    seed=seed)
    battle.params.attacker.coordination = 0.15
    battle.params.defender.supply_shortage = 0.5
    for i in range(3):
        battle.attacker.add_division(make_template(name=f"Att {i}").spawn())
    for i in range(2):
        battle.defender.add_division(make_template(name=f"Def {i}").spawn())
    battle.run_rounds(15)
    return battle


def test_battle_roundtrip_preserves_state():
    battle = make_running_battle()
    data = battle_to_dict(battle, log_text="ligne1\nligne2")
    loaded, log_text = battle_from_dict(data)

    assert log_text == "ligne1\nligne2"
    assert loaded.round == battle.round
    assert loaded.battle_phase == battle.battle_phase
    assert loaded.result == battle.result
    assert loaded.params.terrain_id == "hills"
    assert loaded.params.fort_level == battle.params.fort_level
    assert loaded.params.is_night is True
    assert loaded.params.attacker.coordination == pytest.approx(0.15)
    assert loaded.params.defender.supply_shortage == pytest.approx(0.5)
    assert loaded.attacker.leader.name == "Von Test"
    assert loaded.attacker.leader.traits == ["Panzer Leader"]
    assert loaded.attacker.leader.preferred_tactic == "Blitz"
    assert loaded.attacker.leader.abilities[0].attack_bonus == 10

    # Divisions : PV/organisation courants et positions conservés
    assert len(loaded.attacker.divisions) == 3
    for orig, copy in zip(battle.attacker.divisions, loaded.attacker.divisions):
        assert copy.name == orig.name
        assert copy.current_hp == pytest.approx(orig.current_hp)
        assert copy.current_org == pytest.approx(orig.current_org)
    assert len(loaded.attacker.frontline) == len(battle.attacker.frontline)
    assert len(loaded.defender.retreated) == len(battle.defender.retreated)

    # Tactiques actives restaurées
    for side in ("attacker", "defender"):
        orig_t, loaded_t = battle.active_tactics[side], loaded.active_tactics[side]
        if orig_t is None:
            assert loaded_t is None
        else:
            assert loaded_t.name == orig_t.name
            assert loaded_t.countered == orig_t.countered


def test_battle_roundtrip_rng_state_identical_continuation():
    battle = make_running_battle(seed=7)
    data = battle_to_dict(battle)
    loaded, _ = battle_from_dict(data)
    battle.run_rounds(5)
    loaded.run_rounds(5)
    orig = [(d.current_hp, d.current_org) for d in battle.attacker.divisions]
    copy = [(d.current_hp, d.current_org) for d in loaded.attacker.divisions]
    assert orig == copy   # même état RNG → même suite de bataille


def test_save_store_crud(tmp_path):
    store = BattleSaveStore(tmp_path)
    battle = make_running_battle()
    store.save("Ma bataille", battle, "logs")
    assert [s["nom"] for s in store.list_saves()] == ["Ma bataille"]
    assert store.list_saves()[0]["round"] == battle.round

    loaded, log_text = store.load("Ma bataille")
    assert loaded.round == battle.round and log_text == "logs"

    assert store.rename("Ma bataille", "Bataille 2")
    assert [s["nom"] for s in store.list_saves()] == ["Bataille 2"]
    assert not store.rename("Inexistante", "X")
    assert store.delete("Bataille 2")
    assert store.list_saves() == []


def test_csv_export(tmp_path):
    battle = make_running_battle()
    path = tmp_path / "logs.csv"
    rows = export_battle_csv(battle, path)
    assert rows > 0
    with open(path, encoding="utf-8-sig") as f:
        reader = list(csv.reader(f, delimiter=";"))
    assert reader[0][0] == "tour"
    assert len(reader) == rows + 1
    # Chaque ligne a bien toutes les colonnes
    assert all(len(row) == len(reader[0]) for row in reader)


def test_csv_export_is_always_complete(tmp_path):
    """L'export CSV doit toujours contenir attaques + événements + état,
    quel que soit le niveau d'affichage choisi dans la GUI (§11)."""
    battle = make_running_battle()
    path = tmp_path / "logs_complets.csv"
    export_battle_csv(battle, path)
    with open(path, encoding="utf-8-sig") as f:
        reader = list(csv.reader(f, delimiter=";"))
    header = reader[0]
    type_col = header.index("type")
    types_present = {row[type_col] for row in reader[1:]}
    assert "attaque" in types_present
    assert "evenement" in types_present
    assert "etat" in types_present
    # Une ligne "etat" par tour joué, avec le message d'environnement
    message_col = header.index("message")
    etat_rows = [row for row in reader[1:] if row[type_col] == "etat"]
    assert len(etat_rows) == len(battle.logs)
    assert all("Terrain" in row[message_col] for row in etat_rows)
