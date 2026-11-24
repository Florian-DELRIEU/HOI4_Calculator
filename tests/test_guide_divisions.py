"""Divisions d'exemple du guide Paradox (tools/guide_divisions.py)."""
import sys
from collections import Counter
from pathlib import Path

from engine.composition import aggregate, validate
from persistence.divisions import DivisionStore

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import guide_divisions  # noqa: E402


def test_every_design_is_valid_and_uniquely_named():
    templates = [t for t, _ in guide_divisions.build()]
    assert len(guide_divisions.DESIGNS) == 15
    assert len(templates) == 43
    assert len({t.name for t in templates}) == len(templates)
    for t in templates:
        assert validate(t.battalions, t.support_companies) == [], t.name
        assert t.stats == aggregate(t.battalions, t.support_companies, t.equipment)[0]


def test_compositions_match_the_guide():
    by_name = {t.name: t for t, _ in guide_divisions.build()}
    heavy = by_name["Infanterie lourde (1942)"]
    assert Counter(heavy.battalions) == {"infantry": 6, "artillery": 2, "heavy_td": 1}
    assert heavy.stats.width == 20
    spear = by_name["Fer de lance blindé (1939, chars moyens)"]
    assert Counter(spear.battalions) == {"medium_spg": 2, "medium_tank": 3, "motorized": 4}
    assert spear.equipment == "1939"
    modern = by_name["Blindée mixte (1945, chars modernes)"]
    assert "modern_td" in modern.battalions and modern.equipment == "1942"


def test_install_is_idempotent_and_keeps_user_edits(tmp_path):
    store = DivisionStore(tmp_path)
    assert guide_divisions.install(store) == 43
    edited = store.get("Infanterie de base (1936)")
    edited.experience = "veteran"
    store.save(edited)
    assert guide_divisions.install(store) == 0
    assert store.get("Infanterie de base (1936)").experience == "veteran"
    loaded = store.get("Canons d'assaut (1942, chars lourds)")
    assert loaded.folder == "Guide Paradox/1942" and loaded.equipment == "1942"
    assert guide_divisions.install(store, force=True) == 43
    assert store.get("Infanterie de base (1936)").experience == "regular"
