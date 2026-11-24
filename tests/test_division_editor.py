"""Concepteur de division (GUI) : grille 5×5, soutien, stats en direct."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

pytest.importorskip("PySide6")

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMessageBox

from engine import composition
from engine.division import DivisionTemplate
from gui.division_editor import DivisionEditor
from persistence.divisions import DivisionStore


@pytest.fixture(scope="module")
def app():
    return QApplication.instance() or QApplication([])


@pytest.fixture
def editor(app, tmp_path):
    store = DivisionStore(tmp_path / "divisions")
    store.save(DivisionTemplate(
        name="Infanterie 7-2", battalions=["infantry"] * 7 + ["artillery"] * 2,
        support_companies=["engineer", "recon", "signal"]))
    ed = DivisionEditor(store)
    ed.template_list.setCurrentRow(0)
    return ed


def _pick(ed, uid):
    for g in range(ed.palette.topLevelItemCount()):
        top = ed.palette.topLevelItem(g)
        for c in range(top.childCount()):
            if top.child(c).data(0, Qt.UserRole) == uid:
                ed.palette.setCurrentItem(top.child(c))
                return
    raise KeyError(uid)


def test_loading_a_template_fills_the_grid_without_touching_stats(editor):
    assert [s for s in editor.slots if s] == ["infantry"] * 7 + ["artillery"] * 2
    assert [s for s in editor.support_slots if s] == ["engineer", "recon", "signal"]
    # stats enregistrées du template (vides) conservées au chargement
    assert editor.stat_spins["hp"].value() == 0


def test_editing_the_grid_updates_stats_live(editor):
    _pick(editor, "infantry")
    editor._place_line(24)                       # dernière case
    expected, recon = composition.aggregate(*editor._collect_composition())
    assert editor.stat_spins["hp"].value() == pytest.approx(expected.hp)
    assert editor.recon_spin.value() == pytest.approx(recon)
    editor._clear_line(24)
    expected, _ = composition.aggregate(*editor._collect_composition())
    assert editor.stat_spins["hp"].value() == pytest.approx(176.2 + 5.0)


def test_fill_column_and_clear_all(editor):
    _pick(editor, "medium_tank")
    editor._fill_column(4)
    assert editor.slots[20:25] == ["medium_tank"] * 5
    editor._clear_all()
    assert not any(editor.slots) and not any(editor.support_slots)


def test_support_rules_are_enforced(editor):
    _pick(editor, "armored_signal")
    editor._place_support(3)                     # « signal » déjà présent : même famille
    assert editor.support_slots[3] is None
    assert "incompatible" in editor.status_label.text()
    _pick(editor, "maintenance")
    editor._place_support(3)
    assert editor.support_slots[3] == "maintenance"
    _pick(editor, "infantry")                    # une unité de ligne ne va pas en soutien
    editor._place_support(4)
    assert editor.support_slots[4] is None


def test_save_persists_grid_layout(editor, monkeypatch):
    _pick(editor, "heavy_tank")
    editor._place_line(24)
    editor.name_edit.setText("Avec trou")
    monkeypatch.setattr(QMessageBox, "information", staticmethod(lambda *a, **k: None))
    editor._on_save()
    saved = editor.store.get("Avec trou")
    assert saved.grid[24] == "heavy_tank" and saved.grid[9] is None
    assert saved.stats.hp == pytest.approx(editor.stat_spins["hp"].value())
