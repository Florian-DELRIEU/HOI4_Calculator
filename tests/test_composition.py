"""Tests de l'agrégation par bataillons (jalon 3, CDC §6.1)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from engine import composition
from engine.composition import (BATTALIONS, LINE_BATTALIONS, SUPPORT_COMPANIES,
                                BattalionDef, aggregate, is_artillery, validate)
from engine.division import DivisionTemplate
from persistence.battalions import CustomBattalionStore


def test_battalion_tables_loaded():
    # Types exigés par le CDC §6.1 a minima
    required = {"infantry", "bicycle", "mountain", "marines", "paratrooper",
                "cavalry", "motorized", "mechanized", "anti_tank", "anti_air",
                "artillery", "rocket_artillery", "light_tank", "medium_tank",
                "heavy_tank", "super_heavy_tank", "modern_tank",
                "light_td", "light_spg", "light_spaa"}
    assert required <= set(LINE_BATTALIONS)
    required_supports = {"recon", "engineer", "field_hospital", "logistics",
                         "maintenance", "military_police", "signal",
                         "support_artillery", "support_anti_tank", "support_anti_air",
                         "support_rocket_artillery"}
    assert required_supports <= set(SUPPORT_COMPANIES)


def test_widths_and_hp_match_cdc():
    # Largeurs (CDC §6.1) : inf/blindés 2, artillerie 3, AT/AA 1, soutien 0
    assert BATTALIONS["infantry"].width == 2
    assert BATTALIONS["light_tank"].width == 2
    assert BATTALIONS["artillery"].width == 3
    assert BATTALIONS["anti_tank"].width == 1
    assert BATTALIONS["anti_air"].width == 1
    assert BATTALIONS["engineer"].width == 0
    # HP (CDC §6.1)
    assert BATTALIONS["mechanized"].hp == 30
    assert BATTALIONS["infantry"].hp == 25
    assert BATTALIONS["cavalry"].hp == 25
    assert BATTALIONS["motorized"].hp == 25
    assert BATTALIONS["paratrooper"].hp == 22
    assert BATTALIONS["mountain"].hp == 20
    assert BATTALIONS["marines"].hp == 20
    assert BATTALIONS["medium_tank"].hp == 2
    assert BATTALIONS["artillery"].hp == 0.6
    assert BATTALIONS["recon"].hp == 2
    assert BATTALIONS["military_police"].hp == 1
    assert BATTALIONS["support_artillery"].hp == 0.2


def test_aggregate_classic_7_2():
    """7 infanterie + 2 artillerie : recoupe le template historique."""
    stats, recon = aggregate(["infantry"] * 7 + ["artillery"] * 2, [])
    assert stats.hp == pytest.approx(7 * 25 + 2 * 0.6)          # 176.2
    assert stats.organisation == pytest.approx((7 * 60) / 9, abs=0.01)  # 46.67
    assert stats.soft_attack == pytest.approx(7 * 3 + 2 * 25)   # 71
    assert stats.width == 7 * 2 + 2 * 3                          # 20
    assert stats.speed == 4.0
    assert stats.hardness == 0.0
    assert recon == 0.0


def test_aggregate_armor_and_piercing_formulas():
    stats, _ = aggregate(["infantry", "medium_tank"], [])
    # Blindage = 0,3×max + 0,7×moyenne
    assert stats.armor == pytest.approx(0.3 * 60 + 0.7 * 30)
    # Piercing = 0,4×max + 0,6×moyenne
    assert stats.piercing == pytest.approx(0.4 * 61 + 0.6 * 31)


def test_aggregate_speed_is_slowest_line_battalion():
    stats, _ = aggregate(["motorized", "heavy_tank"], [])
    assert stats.speed == 5.0
    # Les compagnies de soutien ne comptent pas pour la vitesse
    stats, _ = aggregate(["motorized"], ["engineer"])
    assert stats.speed == 12.0


def test_aggregate_supports_contribute_stats_not_width():
    base, _ = aggregate(["infantry"] * 4, [])
    with_art, recon = aggregate(["infantry"] * 4, ["support_artillery", "recon"])
    assert with_art.width == base.width
    assert with_art.soft_attack == pytest.approx(base.soft_attack + 15.0 + 0.3)
    assert recon == 1.0
    # La transmission apporte l'initiative
    with_signal, _ = aggregate(["infantry"] * 4, ["signal"])
    assert with_signal.initiative == pytest.approx(0.10)


def test_aggregate_org_includes_supports():
    stats, _ = aggregate(["infantry"] * 4, ["engineer"])
    assert stats.organisation == pytest.approx((4 * 60 + 20) / 5)


def test_validation_limits():
    assert validate(["infantry"] * 26, []) != []
    assert validate(["infantry"], ["engineer"] * 6) != []
    assert validate(["engineer"], []) != []          # soutien en ligne interdit
    assert validate(["infantry"], ["infantry"]) != []  # ligne en soutien interdit
    assert validate(["infantry"], ["engineer", "engineer"]) != []  # doublon
    assert validate(["infantry"] * 10, ["engineer", "recon"]) == []
    with pytest.raises(ValueError):
        aggregate(["infantry"] * 26, [])


def test_artillery_ratio_trigger():
    assert is_artillery("artillery")
    assert is_artillery("rocket_artillery")
    assert is_artillery("light_spg")
    assert not is_artillery("infantry")
    template = DivisionTemplate(name="T", battalions=["infantry"] * 8 + ["artillery"] * 2)
    assert template.artillery_ratio() == pytest.approx(0.2)


def test_template_recalculate_roundtrip():
    from persistence.divisions import template_from_dict, template_to_dict
    template = DivisionTemplate(name="Composée",
                                battalions=["infantry"] * 6 + ["artillery"] * 2,
                                support_companies=["engineer", "signal"])
    stats, recon = aggregate(template.battalions, template.support_companies)
    template.stats = stats
    template.recon = recon
    data = template_to_dict(template)
    assert data["Bataillons"] == template.battalions
    assert data["Compagnies de soutien"] == template.support_companies
    loaded = template_from_dict(data)
    assert loaded.battalions == template.battalions
    assert loaded.stats.hp == template.stats.hp


# ------------------------------------------------ bataillons personnalisés

@pytest.fixture
def custom_path(tmp_path, monkeypatch):
    """Redirige la persistance des bataillons personnalisés vers un fichier
    temporaire et restaure l'état officiel à la fin."""
    path = tmp_path / "battalions_custom.json"
    monkeypatch.setattr(composition, "CUSTOM_BATTALIONS_PATH", path)
    yield path
    composition.reload()   # recharge sans les personnalisés de test


def _custom_battalion(bid="custom_infanterie_elite", line=True):
    return BattalionDef(
        id=bid, nom="Infanterie d'élite", group="infanterie", line=line,
        width=2, hp=30, org=80, soft=8, hard=1, air=0, defense=40,
        breakthrough=5, armor=0, piercing=2, hardness=0.0, speed=4,
        custom=True)


def test_custom_battalion_upsert_merges_into_tables(custom_path):
    store = CustomBattalionStore(custom_path)
    store.upsert(_custom_battalion())

    assert "custom_infanterie_elite" in composition.BATTALIONS
    assert "custom_infanterie_elite" in composition.LINE_BATTALIONS
    b = composition.BATTALIONS["custom_infanterie_elite"]
    assert b.custom is True and b.nom == "Infanterie d'élite"
    # utilisable dans une agrégation de composition
    stats, _ = composition.aggregate(["custom_infanterie_elite"] * 5, [])
    assert stats.hp == 150
    assert stats.soft_attack == 40


def test_custom_battalion_persistence_roundtrip(custom_path):
    store = CustomBattalionStore(custom_path)
    store.upsert(_custom_battalion())
    assert custom_path.exists()
    # rechargement à froid
    reloaded = composition.load_custom()
    assert "custom_infanterie_elite" in reloaded
    assert reloaded["custom_infanterie_elite"].defense == 40


def test_custom_support_company(custom_path):
    store = CustomBattalionStore(custom_path)
    store.upsert(_custom_battalion(bid="custom_soutien", line=False))
    assert "custom_soutien" in composition.SUPPORT_COMPANIES
    assert "custom_soutien" not in composition.LINE_BATTALIONS


def test_custom_battalion_delete(custom_path):
    store = CustomBattalionStore(custom_path)
    store.upsert(_custom_battalion())
    assert store.delete("custom_infanterie_elite") is True
    assert "custom_infanterie_elite" not in composition.BATTALIONS
    assert store.delete("inexistant") is False


def test_custom_does_not_break_official(custom_path):
    store = CustomBattalionStore(custom_path)
    store.upsert(_custom_battalion())
    # les officiels restent présents
    assert "infantry" in composition.BATTALIONS
    assert composition.BATTALIONS["infantry"].custom is False
