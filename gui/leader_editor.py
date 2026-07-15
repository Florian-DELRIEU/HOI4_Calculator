"""Éditeur de leaders (CDC §10.3) : compétences, traits, tactique favorite,
capacités activables."""
from __future__ import annotations

import json
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QDoubleSpinBox, QFormLayout, QGroupBox, QHBoxLayout, QInputDialog,
    QLabel, QLineEdit, QListWidget, QListWidgetItem, QMessageBox, QPushButton,
    QSpinBox, QComboBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
)

from engine.gamedata import DATA_DIR
from engine.leader import Leader, LeaderAbility
from engine.tactics import TacticRegistry
from persistence.leaders import LeaderStore


def _load_default_traits() -> list[str]:
    try:
        with open(DATA_DIR / "leader_traits.json", encoding="utf-8") as f:
            return json.load(f)["traits"]
    except (OSError, KeyError, json.JSONDecodeError):
        return []


class LeaderEditor(QDialog):
    def __init__(self, store: LeaderStore | None = None,
                 registry: TacticRegistry | None = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Éditeur de leaders")
        self.resize(860, 560)
        self.store = store or LeaderStore()
        self.registry = registry or TacticRegistry()
        self.current: Leader | None = None

        root = QHBoxLayout(self)

        # ------------------------------------------------ liste des leaders
        left = QVBoxLayout()
        self.leader_list = QListWidget()
        self.leader_list.currentItemChanged.connect(self._on_select)
        left.addWidget(self.leader_list)
        btn_row = QHBoxLayout()
        new_btn = QPushButton("Nouveau")
        new_btn.clicked.connect(self._on_new)
        del_btn = QPushButton("Supprimer")
        del_btn.clicked.connect(self._on_delete)
        btn_row.addWidget(new_btn)
        btn_row.addWidget(del_btn)
        left.addLayout(btn_row)
        root.addLayout(left, stretch=1)

        # ------------------------------------------------------ formulaire
        right = QVBoxLayout()
        form_box = QGroupBox("Leader")
        form = QFormLayout(form_box)
        self.name_edit = QLineEdit()
        form.addRow("Nom", self.name_edit)
        self.attack_spin = QSpinBox()
        self.attack_spin.setRange(0, 10)
        form.addRow("Compétence attaque (+2,5 %/pt)", self.attack_spin)
        self.defense_spin = QSpinBox()
        self.defense_spin.setRange(0, 10)
        form.addRow("Compétence défense (+2,5 %/pt)", self.defense_spin)
        self.preferred_combo = QComboBox()
        self.preferred_combo.addItem("— Aucune —", "")
        for name in self.registry.all_names():
            self.preferred_combo.addItem(name, name)
        form.addRow("Tactique favorite (+50 % poids)", self.preferred_combo)
        right.addWidget(form_box)

        # Traits
        traits_box = QGroupBox("Traits")
        traits_layout = QVBoxLayout(traits_box)
        self.traits_list = QListWidget()
        self.traits_list.setSelectionMode(QListWidget.NoSelection)
        traits_layout.addWidget(self.traits_list)
        add_trait_btn = QPushButton("Ajouter un trait personnalisé…")
        add_trait_btn.clicked.connect(self._on_add_trait)
        traits_layout.addWidget(add_trait_btn)
        right.addWidget(traits_box, stretch=1)

        # Capacités
        abilities_box = QGroupBox("Capacités de maréchal (activation manuelle en bataille)")
        abilities_layout = QVBoxLayout(abilities_box)
        self.abilities_table = QTableWidget(0, 5)
        self.abilities_table.setHorizontalHeaderLabels(
            ["Nom", "Attaque %", "Défense %", "Org rendue", "Durée (tours)"])
        abilities_layout.addWidget(self.abilities_table)
        ab_row = QHBoxLayout()
        add_ab_btn = QPushButton("Ajouter")
        add_ab_btn.clicked.connect(self._on_add_ability)
        del_ab_btn = QPushButton("Retirer la ligne")
        del_ab_btn.clicked.connect(self._on_del_ability)
        ab_row.addWidget(add_ab_btn)
        ab_row.addWidget(del_ab_btn)
        abilities_layout.addLayout(ab_row)
        right.addWidget(abilities_box, stretch=1)

        save_btn = QPushButton("Enregistrer le leader")
        save_btn.clicked.connect(self._on_save)
        right.addWidget(save_btn)

        root.addLayout(right, stretch=2)

        self._known_traits = _load_default_traits()
        self._refresh_list()

    # ----------------------------------------------------------- helpers

    def _refresh_list(self, select: str | None = None) -> None:
        self.leader_list.clear()
        for leader in self.store.list_leaders():
            item = QListWidgetItem(f"{leader.name} (A{leader.attack_level}/D{leader.defense_level})")
            item.setData(Qt.UserRole, leader)
            self.leader_list.addItem(item)
            if select and leader.name == select:
                self.leader_list.setCurrentItem(item)

    def _refresh_traits(self, checked: list[str]) -> None:
        self.traits_list.clear()
        for trait in dict.fromkeys(self._known_traits + checked):
            item = QListWidgetItem(trait)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked if trait in checked else Qt.Unchecked)
            self.traits_list.addItem(item)

    def _load_form(self, leader: Leader) -> None:
        self.current = leader
        self.name_edit.setText(leader.name)
        self.attack_spin.setValue(leader.attack_level)
        self.defense_spin.setValue(leader.defense_level)
        index = self.preferred_combo.findData(leader.preferred_tactic)
        self.preferred_combo.setCurrentIndex(max(index, 0))
        self._refresh_traits(leader.traits)
        self.abilities_table.setRowCount(0)
        for ability in leader.abilities:
            self._append_ability_row(ability)

    def _append_ability_row(self, ability: LeaderAbility) -> None:
        row = self.abilities_table.rowCount()
        self.abilities_table.insertRow(row)
        values = [ability.name, str(ability.attack_bonus), str(ability.defense_bonus),
                  str(ability.org_restore), str(ability.duration_rounds)]
        for col, value in enumerate(values):
            self.abilities_table.setItem(row, col, QTableWidgetItem(value))

    def _collect_form(self) -> Leader | None:
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Nom manquant", "Donnez un nom au leader.")
            return None
        traits = []
        for i in range(self.traits_list.count()):
            item = self.traits_list.item(i)
            if item.checkState() == Qt.Checked:
                traits.append(item.text())
        abilities = []
        for row in range(self.abilities_table.rowCount()):
            def cell(col, default="0"):
                item = self.abilities_table.item(row, col)
                return item.text() if item and item.text() else default
            ab_name = cell(0, "")
            if not ab_name:
                continue
            try:
                abilities.append(LeaderAbility(
                    name=ab_name,
                    attack_bonus=float(cell(1)),
                    defense_bonus=float(cell(2)),
                    org_restore=float(cell(3)),
                    duration_rounds=int(float(cell(4, "24"))),
                ))
            except ValueError:
                QMessageBox.warning(self, "Valeur invalide",
                                    f"Capacité « {ab_name} » : valeurs numériques attendues.")
                return None
        return Leader(name=name,
                      attack_level=self.attack_spin.value(),
                      defense_level=self.defense_spin.value(),
                      traits=traits,
                      preferred_tactic=self.preferred_combo.currentData() or "",
                      abilities=abilities)

    # ------------------------------------------------------------- slots

    def _on_select(self, item, _previous=None) -> None:
        if item is not None:
            self._load_form(item.data(Qt.UserRole))

    def _on_new(self) -> None:
        self._load_form(Leader(name="Nouveau leader"))

    def _on_delete(self) -> None:
        item = self.leader_list.currentItem()
        if item is None:
            return
        leader = item.data(Qt.UserRole)
        if QMessageBox.question(self, "Supprimer",
                                f"Supprimer le leader « {leader.name} » ?") == QMessageBox.Yes:
            self.store.delete(leader.name)
            self._refresh_list()

    def _on_add_trait(self) -> None:
        trait, ok = QInputDialog.getText(self, "Nouveau trait", "Nom du trait :")
        if ok and trait.strip():
            self._known_traits.append(trait.strip())
            checked = []
            for i in range(self.traits_list.count()):
                item = self.traits_list.item(i)
                if item.checkState() == Qt.Checked:
                    checked.append(item.text())
            checked.append(trait.strip())
            self._refresh_traits(checked)

    def _on_add_ability(self) -> None:
        self._append_ability_row(LeaderAbility(name="Nouvelle capacité"))

    def _on_del_ability(self) -> None:
        row = self.abilities_table.currentRow()
        if row >= 0:
            self.abilities_table.removeRow(row)

    def _on_save(self) -> None:
        leader = self._collect_form()
        if leader is None:
            return
        if self.current and self.current.name != leader.name:
            self.store.delete(self.current.name)
        self.store.upsert(leader)
        self._refresh_list(select=leader.name)
        QMessageBox.information(self, "Enregistré",
                                f"Leader « {leader.name} » enregistré.")
