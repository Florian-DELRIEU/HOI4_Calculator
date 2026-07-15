"""Tests de l'agrégation par bataillons (jalon 3, CDC §6.1)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from engine.composition import (BATTALIONS, LINE_BATTALIONS, SUPPORT_COMPANIES,
                                aggregate, is_artillery, validate)
from engine.division import DivisionTemplate


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
