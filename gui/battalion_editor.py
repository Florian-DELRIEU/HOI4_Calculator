"""Éditeur de bataillons personnalisés.

Permet de créer/modifier/supprimer des bataillons (et compagnies de soutien)
personnalisés, persistés dans ``saves/battalions_custom.json`` et fusionnés
avec les bataillons officiels. Ils deviennent aussitôt disponibles dans
l'éditeur de division."""
from __future__ import annotations

import re

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QDialog, QDoubleSpinBox, QFormLayout, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem, QMessageBox, QPushButton,
    QVBoxLayout,
)

from engine import composition
from engine.composition import BattalionDef
from persistence.battalions import CustomBattalionStore

# Champs numériques éditables : (attribut, libellé, min, max, pas, décimales)
NUM_FIELDS = [
    ("width", "Largeur de combat", 0, 200, 1, 1),
    ("hp", "PV", 0, 1000, 0.1, 2),
    ("org", "Organisation", 0, 300, 1, 1),
    ("soft", "Attaque douce", 0, 1000, 0.1, 2),
    ("hard", "Attaque dure", 0, 1000, 0.1, 2),
    ("air", "Attaque aérienne", 0, 1000, 0.1, 2),
    ("defense", "Défense", 0, 1000, 0.1, 2),
    ("breakthrough", "Percée", 0, 1000, 0.1, 2),
    ("armor", "Blindage", 0, 1000, 1, 1),
    ("piercing", "Perce-blindage", 0, 1000, 0.1, 2),
    ("hardness", "Dureté (0 à 1)", 0, 1, 0.05, 3),
    ("speed", "Vitesse (km/h)", 0, 50, 0.1, 1),
    ("recon", "Reconnaissance", 0, 10, 0.1, 2),
    ("initiative", "Initiative", 0, 1, 0.01, 3),
]

GROUPS = ["infanterie", "mobile", "artillerie", "blinde", "soutien"]


def _slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return f"custom_{slug}" if slug else "custom_bataillon"


class BattalionEditor(QDialog):
    def __init__(self, store: CustomBattalionStore | None = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Éditeur de bataillons personnalisés")
        self.resize(760, 640)
        self.store = store or CustomBattalionStore()
        self.current_id: str | None = None

        root = QHBoxLayout(self)

        # ------------------------------------------------------ liste gauche
        left = QVBoxLayout()
        left.addWidget(QLabel("Bataillons personnalisés :"))
        self.list_widget = QListWidget()
        self.list_widget.currentItemChanged.connect(self._on_select)
        left.addWidget(self.list_widget, stretch=1)
        new_btn = QPushButton("Nouveau")
        new_btn.clicked.connect(self._on_new)
        del_btn = QPushButton("Supprimer")
        del_btn.clicked.connect(self._on_delete)
        left.addWidget(new_btn)
        left.addWidget(del_btn)
        left.addWidget(QLabel("Bataillons officiels (modèle) :"))
        self.official_combo = QComboBox()
        for bid, b in sorted(composition._OFFICIAL.items(),
                             key=lambda kv: (kv[1].group, kv[1].nom)):
            self.official_combo.addItem(f"[{b.group}] {b.nom}", bid)
        copy_btn = QPushButton("Pré-remplir depuis cet officiel")
        copy_btn.clicked.connect(self._on_copy_official)
        left.addWidget(self.official_combo)
        left.addWidget(copy_btn)
        root.addLayout(left, stretch=1)

        # -------------------------------------------------- formulaire droit
        form = QFormLayout()
        self.name_edit = QLineEdit()
        form.addRow("Nom", self.name_edit)
        self.group_combo = QComboBox()
        self.group_combo.addItems(GROUPS)
        form.addRow("Groupe", self.group_combo)
        self.line_check = QCheckBox("Bataillon de ligne (décoché = compagnie de soutien)")
        self.line_check.setChecked(True)
        form.addRow(self.line_check)
        self.artillery_check = QCheckBox("Compte comme artillerie (déclencheurs de tactiques)")
        form.addRow(self.artillery_check)

        self.spins: dict[str, QDoubleSpinBox] = {}
        for attr, label, lo, hi, step, dec in NUM_FIELDS:
            spin = QDoubleSpinBox()
            spin.setRange(lo, hi)
            spin.setSingleStep(step)
            spin.setDecimals(dec)
            form.addRow(label, spin)
            self.spins[attr] = spin

        self.special_edit = QLineEdit()
        self.special_edit.setPlaceholderText("Effet spécial (texte, immersion)")
        form.addRow("Effet spécial", self.special_edit)

        right = QVBoxLayout()
        right.addLayout(form)
        save_btn = QPushButton("Enregistrer le bataillon personnalisé")
        save_btn.clicked.connect(self._on_save)
        right.addWidget(save_btn)
        root.addLayout(right, stretch=2)

        self._refresh_list()

    # ------------------------------------------------------------- helpers

    def _refresh_list(self, select: str | None = None) -> None:
        self.list_widget.clear()
        for b in self.store.list_custom():
            item = QListWidgetItem(f"[{b.group}] {b.nom}")
            item.setData(Qt.UserRole, b)
            self.list_widget.addItem(item)
            if select and b.id == select:
                self.list_widget.setCurrentItem(item)

    def _load_form(self, b: BattalionDef) -> None:
        self.current_id = b.id if b.custom else None
        self.name_edit.setText(b.nom)
        idx = self.group_combo.findText(b.group)
        self.group_combo.setCurrentIndex(max(idx, 0))
        self.line_check.setChecked(b.line)
        self.artillery_check.setChecked(b.artillery)
        for attr, spin in self.spins.items():
            spin.setValue(getattr(b, attr))
        self.special_edit.setText(b.special)

    # ------------------------------------------------------------- slots

    def _on_select(self, item, _prev=None) -> None:
        if item is not None:
            self._load_form(item.data(Qt.UserRole))

    def _on_new(self) -> None:
        self.current_id = None
        self.name_edit.setText("Nouveau bataillon")
        self.group_combo.setCurrentIndex(0)
        self.line_check.setChecked(True)
        self.artillery_check.setChecked(False)
        for spin in self.spins.values():
            spin.setValue(0)
        self.special_edit.clear()

    def _on_copy_official(self) -> None:
        bid = self.official_combo.currentData()
        b = composition._OFFICIAL.get(bid)
        if b is not None:
            self._load_form(b)
            self.current_id = None   # on crée un nouveau, pas d'édition
            self.name_edit.setText(f"{b.nom} (copie)")

    def _on_delete(self) -> None:
        item = self.list_widget.currentItem()
        if item is None:
            return
        b = item.data(Qt.UserRole)
        if QMessageBox.question(self, "Supprimer",
                                f"Supprimer le bataillon « {b.nom} » ?") == QMessageBox.Yes:
            self.store.delete(b.id)
            self._on_new()
            self._refresh_list()

    def _on_save(self) -> None:
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Nom manquant", "Donnez un nom au bataillon.")
            return
        battalion_id = self.current_id or _slugify(name)
        # Évite d'écraser un bataillon officiel par mégarde
        if self.current_id is None and battalion_id in composition._OFFICIAL:
            battalion_id += "_perso"
        values = {attr: spin.value() for attr, spin in self.spins.items()}
        battalion = BattalionDef(
            id=battalion_id,
            nom=name,
            group=self.group_combo.currentText(),
            line=self.line_check.isChecked(),
            artillery=self.artillery_check.isChecked(),
            special=self.special_edit.text().strip(),
            custom=True,
            **values,
        )
        self.store.upsert(battalion)
        self.current_id = battalion_id
        self._refresh_list(select=battalion_id)
        QMessageBox.information(self, "Enregistré",
                               f"Bataillon « {name} » enregistré et disponible "
                               f"dans l'éditeur de division.")
