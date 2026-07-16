"""Dialogue d'édition d'une division EN COURS de bataille — accessible par
clic droit depuis la fenêtre de bataille. Modifie l'instance en jeu (PV/
organisation actuels et statistiques finales), jamais le template sur disque."""
from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog, QDialogButtonBox, QDoubleSpinBox, QFormLayout, QVBoxLayout,
)

from engine.division import Division
from gui.division_editor import STAT_FIELDS


class DivisionInstanceDialog(QDialog):
    def __init__(self, division: Division, parent=None):
        super().__init__(parent)
        self.division = division
        self.setWindowTitle(f"Modifier — {division.name}")
        self.resize(420, 600)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.hp_current_spin = QDoubleSpinBox()
        self.hp_current_spin.setRange(0, 10000)
        self.hp_current_spin.setDecimals(2)
        self.hp_current_spin.setValue(division.current_hp)
        form.addRow("PV actuels", self.hp_current_spin)

        self.org_current_spin = QDoubleSpinBox()
        self.org_current_spin.setRange(0, 1000)
        self.org_current_spin.setDecimals(2)
        self.org_current_spin.setValue(division.current_org)
        form.addRow("Organisation actuelle", self.org_current_spin)

        self.stat_spins: dict[str, QDoubleSpinBox] = {}
        for attr, label, lo, hi in STAT_FIELDS:
            spin = QDoubleSpinBox()
            spin.setRange(lo, hi)
            spin.setDecimals(3 if hi <= 1 else 2)
            spin.setSingleStep(0.05 if hi <= 1 else 1.0)
            spin.setValue(getattr(division.stats, attr))
            form.addRow(label, spin)
            self.stat_spins[attr] = spin

        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def apply(self) -> None:
        """Applique les valeurs saisies à la division en jeu (à appeler
        après un exec() ayant renvoyé Accepted)."""
        self.division.current_hp = self.hp_current_spin.value()
        self.division.current_org = self.org_current_spin.value()
        for attr, spin in self.stat_spins.items():
            setattr(self.division.stats, attr, spin.value())
