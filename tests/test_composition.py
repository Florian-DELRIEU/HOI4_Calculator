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
                "heavy_tank", "modern_tank",
                "light_td", "light_spg", "light_spaa"}
    assert required <= set(LINE_BATTALIONS)
    required_supports = {"recon", "engineer", "field_hospital", "logistics",
                         "maintenance", "military_police", "signal",
                         "support_artillery", "support_anti_tank", "support_anti_air",
                         "support_rocket_artillery",
                         # compagnies (et non bataillons) dans les CSV vanilla
                         "super_heavy_tank", "super_heavy_td", "super_heavy_spg",
                         "super_heavy_spaa", "land_cruiser"}
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


# ------------------------------------------------ données issues des CSV

ROOT = Path(__file__).resolve().parent.parent


def test_battalion_data_integrity():
    assert len(BATTALIONS) == 81
    for b in BATTALIONS.values():
        if b.line:
            assert b.width > 0, b.id
        else:
            assert b.width == 0, b.id
        assert b.hp > 0 and b.nom, b.id
    # chaque famille d'exclusion compte au moins deux compagnies de soutien
    families: dict[str, list[str]] = {}
    for b in SUPPORT_COMPANIES.values():
        for family in composition.exclusion_families(b):
            families.setdefault(family, []).append(b.id)
    assert set(families) == {"recon", "engineer", "maintenance", "signal", "military_police",
                             "field_hospital", "logistics", "helicopter_brigade_recon",
                             "helicopter_brigade_med_evac", "helicopter_brigade_transports"}
    assert all(len(ids) >= 2 for ids in families.values())


def test_battalions_json_is_in_sync_with_csv():
    """data/battalions.json doit être exactement ce que génère le script
    d'import depuis tools/sources (sinon : relancer tools/import_csv.py)."""
    import json
    sys.path.insert(0, str(ROOT / "tools"))
    import import_csv
    entries, _ = import_csv.build()
    with open(ROOT / "data" / "battalions.json", encoding="utf-8") as f:
        committed = json.load(f)["battalions"]
    assert committed == [import_csv._clean_entry(e) for e in entries]


def test_super_heavy_and_land_cruiser_are_support_companies():
    for uid in ("super_heavy_tank", "super_heavy_td", "super_heavy_spg",
                "super_heavy_spaa", "land_cruiser"):
        assert uid in SUPPORT_COMPANIES and uid not in LINE_BATTALIONS
        assert SUPPORT_COMPANIES[uid].slows_division


def test_new_vanilla_units_present():
    for uid in ("penal_battalion", "militia", "rangers", "camelry", "armored_car",
                "amtrac", "motorized_artillery", "modern_spaa"):
        assert uid in LINE_BATTALIONS
    assert BATTALIONS["armored_car"].armor == 3
    assert BATTALIONS["mechanized"].hardness == pytest.approx(0.6)


# ------------------------------------------------------- concepteur (grille)

def test_exclusive_support_families():
    assert validate(["infantry"], ["engineer", "armored_engineer"]) != []
    assert validate(["infantry"], ["recon", "armored_car_recon"]) != []
    assert validate(["infantry"], ["engineer", "recon", "signal"]) == []
    assert composition.blocked_by("pioneers", ["recon", "engineer"]) == "engineer"
    assert composition.blocked_by("pioneers", ["recon"]) is None
    assert composition.blocked_by("engineer", ["engineer"]) is None   # doublon : autre règle


def test_helicopter_companies_match_wiki():
    """Stats du tableau « Land units » (hélicoptères) et exclusions croisées."""
    recon = BATTALIONS["helicopter_recon"]
    assert (recon.soft, recon.hard, recon.defense, recon.breakthrough,
            recon.armor, recon.piercing, recon.recon) == (3, 0.5, 26, 10, 4, 11, 2)
    brigade = BATTALIONS["helicopter_brigade"]
    assert (brigade.defense, brigade.breakthrough, brigade.armor, brigade.piercing) == (6, 8, 4, 11)
    assert (BATTALIONS["helicopter_med_evac"].breakthrough,
            BATTALIONS["helicopter_transports"].breakthrough) == (13, 13)
    # la brigade bloque les autres compagnies d'hélicoptères, qui se cumulent entre elles
    for other in ("helicopter_recon", "helicopter_med_evac", "helicopter_transports"):
        assert validate(["infantry"], ["helicopter_brigade", other]) != []
    assert validate(["infantry"], ["helicopter_recon", "helicopter_med_evac",
                                   "helicopter_transports"]) == []
    # blocages avec les compagnies classiques
    assert validate(["infantry"], ["field_hospital", "helicopter_med_evac"]) != []
    assert validate(["infantry"], ["logistics", "helicopter_transports"]) != []
    assert validate(["infantry"], ["recon", "helicopter_recon"]) != []
    assert composition.blocked_by("helicopter_brigade", ["helicopter_med_evac"]) == "helicopter_med_evac"


def test_support_company_can_cap_division_speed():
    stats, _ = aggregate(["motorized"] * 3, ["super_heavy_tank"])
    assert stats.speed == 4.0
    stats, _ = aggregate(["motorized"] * 3, ["engineer"])
    assert stats.speed == 12.0


def test_grid_slot_helpers():
    slots = composition.slots_from_list(["infantry", "artillery"])
    assert len(slots) == composition.MAX_LINE_BATTALIONS == 25
    assert slots[:3] == ["infantry", "artillery", None]
    sparse = [None] * 25
    sparse[7], sparse[20] = "infantry", "medium_tank"
    assert composition.list_from_slots(sparse) == ["infantry", "medium_tank"]


def test_design_info_sums():
    info = composition.design_info(["infantry"] * 2, ["engineer"])
    assert info.manpower == 2 * 1000 + 300
    assert info.training_days == 120
    assert info.ic_cost == pytest.approx(2 * 43 + 124)


def test_grid_persistence_roundtrip_and_legacy():
    from persistence.divisions import template_from_dict, template_to_dict
    grid = [None] * 25
    grid[0], grid[1], grid[10] = "infantry", "artillery", "medium_tank"
    template = DivisionTemplate(name="Grille", battalions=["infantry", "artillery", "medium_tank"],
                                grid=grid, support_companies=["engineer"])
    data = template_to_dict(template)
    assert data["Grille"] == grid
    loaded = template_from_dict(data)
    assert loaded.grid == grid
    assert loaded.battalions == ["infantry", "artillery", "medium_tank"]
    # ancien fichier sans « Grille » : lu tel quel, grille reconstruite à l'écriture
    legacy = {"Nom de Template": "Ancien", "Bataillons": ["infantry"] * 3}
    old = template_from_dict(legacy)
    assert old.grid == [] and old.battalions == ["infantry"] * 3
    assert template_to_dict(old)["Grille"][:4] == ["infantry"] * 3 + [None]


def test_saved_templates_match_their_composition():
    """Non-régression : les templates d'exemple composés en bataillons
    redonnent leurs stats enregistrées."""
    from persistence.divisions import DivisionStore
    checked = 0
    for t in DivisionStore(ROOT / "saves" / "divisions").list_templates():
        if not (t.battalions or t.support_companies):
            continue
        assert validate(t.battalions, t.support_companies) == [], t.name
        stats, recon = aggregate(t.battalions, t.support_companies)
        for attr in ("hp", "organisation", "soft_attack", "hard_attack", "defense",
                     "breakthrough", "armor", "piercing", "hardness", "width",
                     "speed", "initiative", "air_attack"):
            assert getattr(t.stats, attr) == pytest.approx(getattr(stats, attr), abs=0.02), \
                f"{t.name} : {attr}"
        assert t.recon == pytest.approx(recon), t.name
        checked += 1
    assert checked >= 10


# ------------------------------------------------ bataillons personnalisés

@pytest.fixture
def custom_path(tmp_path, monkeypatch):
    """Redirige la persistance des bataillons personnalisés vers un fichier
    temporaire et restaure l'état officiel à la fin."""
    path = tmp_path / "battalions_custom.json"
    monkeypatch.setattr(composition, "CUSTOM_BATTALIONS_PATH", path)
    yield path
    # Supprimer le fichier AVANT de recharger : le monkeypatch du chemin n'est
    # annulé qu'après ce teardown, reload() relirait sinon les unités de test
    # (et un « infantry » personnalisé fausserait les autres tests).
    path.unlink(missing_ok=True)
    composition.reload()


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


# ------------------------------------------------- générations d'équipement

def test_default_equipment_leaves_stats_unchanged():
    """Non-régression : sans choix explicite, équipement de base (1918)."""
    stats, _ = aggregate(["infantry"] * 4, [])
    explicit, _ = aggregate(["infantry"] * 4, [], "basic")
    assert stats == explicit
    assert stats.soft_attack == 12 and stats.defense == 80 and stats.breakthrough == 8


@pytest.mark.parametrize("gen, soft, hard, defense, brk, pierc", [
    ("1936", 6, 1, 22, 3, 4),
    ("1939", 9, 1.5, 28, 4, 5),
    ("1942", 12, 2, 34, 5, 10),
])
def test_infantry_stats_match_wiki_equipment(gen, soft, hard, defense, brk, pierc):
    """Un bataillon d'infanterie reçoit exactement les stats de l'équipement
    (wiki Infantry_technology) ; PV, organisation, largeur inchangés."""
    stats, _ = aggregate(["infantry"], [], gen)
    assert stats.soft_attack == pytest.approx(soft)
    assert stats.hard_attack == pytest.approx(hard)
    assert stats.defense == pytest.approx(defense)
    assert stats.breakthrough == pytest.approx(brk)
    assert stats.piercing == pytest.approx(pierc)
    assert (stats.hp, stats.organisation, stats.width) == (25, 60, 2)


def test_equipment_keeps_unit_specific_modifiers():
    irr, _ = aggregate(["irregular_infantry"], [], "1939")    # −5 % soft, −15 % déf.
    assert irr.soft_attack == pytest.approx(9 * 0.95)
    assert irr.defense == pytest.approx(28 * 0.85)
    mnt, _ = aggregate(["mountain"], [], "1939")              # +30 % percée
    assert mnt.breakthrough == pytest.approx(4 * 1.3)


def test_equipment_does_not_touch_other_unit_types():
    for uid in ("anti_tank", "anti_air", "motorized", "motorized_artillery",
                "rocket_artillery", "medium_tank"):
        assert aggregate([uid], [], "1942")[0] == aggregate([uid], [], "basic")[0], uid
    assert aggregate(["infantry"], ["engineer"], "1942")[0].defense \
        == pytest.approx(34 + 22)        # la compagnie du génie ne change pas


def test_artillery_generations_match_wiki_equipment():
    """Canon tracté (1934) -> Improved Artillery (1939) -> Advanced (1942)."""
    for gen, soft, defense, brk in (("basic", 25, 10, 6), ("1936", 25, 10, 6),
                                    ("1939", 30, 15, 7), ("1942", 34, 18, 8)):
        stats, _ = aggregate(["artillery"], [], gen)
        assert (stats.soft_attack, stats.defense, stats.breakthrough)             == pytest.approx((soft, defense, brk)), gen
        assert stats.hard_attack == pytest.approx(2) and stats.piercing == pytest.approx(5)
    # compagnie de soutien : même équipement, ×0,6 propre à la compagnie
    sup, _ = aggregate(["infantry"], ["support_artillery"], "1942")
    inf, _ = aggregate(["infantry"], [], "1942")
    assert sup.soft_attack - inf.soft_attack == pytest.approx(34 * 0.6)


def test_camelry_already_uses_first_generation_stats():
    base = aggregate(["camelry"], [], "1936")[0]
    assert base.soft_attack == pytest.approx(6) and base.defense == pytest.approx(22)
    assert aggregate(["camelry"], [], "1939")[0].soft_attack == pytest.approx(9)
    assert aggregate(["camelry"], [], "basic")[0].soft_attack == pytest.approx(3)


def test_unknown_equipment_is_rejected():
    with pytest.raises(ValueError):
        aggregate(["infantry"], [], "1999")
    assert composition.normalize_equipment("1999") == "basic"
    assert composition.normalize_equipment(None) == "basic"


def test_equipment_units_exist_and_have_matching_base_stats():
    """Chaque unité listée existe et ses stats enregistrées correspondent à
    la génération déclarée (garde-fou si battalions.json est régénéré)."""
    for uid, entry in composition.EQUIPMENT_UNITS.items():
        unit = composition._OFFICIAL[uid]
        ref = composition.EQUIPMENT_FAMILIES[entry["family"]][entry["base"]]
        for stat, value in ref.items():
            ratio = getattr(unit, stat) / value
            # le seul écart admis est un modificateur propre au bataillon
            # (−40 % d'une compagnie de soutien … +30 % de percée)
            assert 0.55 <= ratio <= 1.35, (uid, stat, ratio)


def test_custom_battalion_is_not_rescaled(custom_path):
    CustomBattalionStore(custom_path).upsert(_custom_battalion(bid="infantry"))
    unit = composition.BATTALIONS["infantry"]
    assert unit.custom is True
    assert aggregate(["infantry"], [], "1942")[0] == aggregate(["infantry"], [], "basic")[0]


def test_equipment_persistence_roundtrip_and_legacy():
    from persistence.divisions import template_from_dict, template_to_dict
    template = DivisionTemplate(name="Équipée", battalions=["infantry"], equipment="1939")
    data = template_to_dict(template)
    assert data["Equipement"] == "1939"
    assert template_from_dict(data).equipment == "1939"
    # base : clé absente (fichiers inchangés), et lecture d'anciens fichiers
    assert "Equipement" not in template_to_dict(DivisionTemplate(name="Base"))
    assert template_from_dict({"Nom de Template": "Ancien"}).equipment == "basic"
    assert template_from_dict({"Nom de Template": "X", "Equipement": "zzz"}).equipment == "basic"


def test_better_equipment_shortens_battles():
    """Garde-fou de calibrage : à composition égale, une génération plus
    récente raccourcit nettement les combats (mêmes graines)."""
    from engine.battle import Battle
    from engine.params import BattleParams

    battalions = ["infantry"] * 7 + ["artillery"] * 2

    def median_duration(gen):
        stats, recon = aggregate(battalions, [], gen)
        tpl = DivisionTemplate(name="T", stats=stats, recon=recon,
                               battalions=battalions, equipment=gen)
        rounds = []
        for seed in range(15):
            b = Battle(BattleParams(), seed=seed, use_tactics=False)
            b.attacker.add_division(tpl.spawn())
            b.defender.add_division(tpl.spawn())
            b.run_rounds(3000)
            assert b.is_over
            rounds.append(b.round)
        return sorted(rounds)[len(rounds) // 2]

    basic, y1936, y1942 = median_duration("basic"), median_duration("1936"), median_duration("1942")
    assert y1942 < y1936 < basic
    assert y1936 < 0.85 * basic and y1942 < 0.6 * basic
