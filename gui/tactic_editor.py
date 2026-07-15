"""Éditeur de tactiques personnalisées (CDC §9.4).

Les tactiques personnalisées coexistent avec la table officielle : elles
sont stockées dans ``saves/tactics_custom.json`` et rechargées par le
registre. Une tactique personnalisée portant la même clé (nom, camp, phase)
qu'une officielle la remplace tant qu'elle existe.
"""
from __future__ import annotations

import json

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QDialog, QDoubleSpinBox, QFormLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem, QMessageBox,
    QPlainTextEdit, QPushButton, QVBoxLayout,
)

from engine.tactics import PHASE_LABELS, TacticDef, TacticRegistry


class TacticEditor(QDialog):
    def __init__(self, registry: TacticRegistry | None = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Éditeur de tactiques personnalisées")
        self.resize(900, 560)
        self.registry = registry or TacticRegistry()

        root = QHBoxLayout(self)

        # -------------------------------------------------------- listes
        left = QVBoxLayout()
        left.addWidget(QLabel("Tactiques personnalisées :"))
        self.custom_list = QListWidget()
        self.custom_list.currentItemChanged.connect(self._on_select)
        left.addWidget(self.custom_list, stretch=2)
        del_btn = QPushButton("Supprimer la tactique sélectionnée")
        del_btn.clicked.connect(self._on_delete)
        left.addWidget(del_btn)
        left.addWidget(QLabel("Tactiques officielles (lecture seule,\nsélection = pré-remplir le formulaire) :"))
        self.official_list = QListWidget()
        self.official_list.currentItemChanged.connect(self._on_select_official)
        left.addWidget(self.official_list, stretch=3)
        root.addLayout(left, stretch=1)

        # ---------------------------------------------------- formulaire
        right = QVBoxLayout()
        box = QGroupBox("Tactique")
        form = QFormLayout(box)
        self.name_edit = QLineEdit()
        form.addRow("Nom", self.name_edit)
        self.side_combo = QComboBox()
        self.side_combo.addItem("Attaquant", "attacker")
        self.side_combo.addItem("Défenseur", "defender")
        form.addRow("Camp", self.side_combo)
        self.phase_combo = QComboBox()
        for pid, label in PHASE_LABELS.items():
            self.phase_combo.addItem(label, pid)
        form.addRow("Phase de bataille", self.phase_combo)
        self.weight_spin = QDoubleSpinBox()
        self.weight_spin.setRange(0.0, 100.0)
        self.weight_spin.setValue(4.0)
        form.addRow("Poids de base", self.weight_spin)

        def pct_spin(minimum=-100.0, maximum=200.0):
            s = QDoubleSpinBox()
            s.setRange(minimum, maximum)
            s.setSuffix(" %")
            return s

        self.atk_damage_spin = pct_spin()
        form.addRow("Dégâts attaquant", self.atk_damage_spin)
        self.def_damage_spin = pct_spin()
        form.addRow("Dégâts défenseur", self.def_damage_spin)
        self.width_spin = pct_spin()
        form.addRow("Largeur de combat", self.width_spin)
        self.movement_spin = pct_spin()
        form.addRow("Mouvement", self.movement_spin)
        self.countered_edit = QLineEdit()
        self.countered_edit.setPlaceholderText("Noms séparés par des virgules, ex. Counter-Attack, Ambush")
        form.addRow("Contrée par", self.countered_edit)
        self.begins_combo = QComboBox()
        self.begins_combo.addItem("— Aucune —", "")
        for pid, label in PHASE_LABELS.items():
            self.begins_combo.addItem(label, pid)
        form.addRow("Démarre la phase", self.begins_combo)
        self.trigger_edit = QPlainTextEdit()
        self.trigger_edit.setPlaceholderText(
            'Déclencheur JSON optionnel, ex. {"any": [{"skill_gt": 2}, {"trait": "Trickster"}]}')
        self.trigger_edit.setMaximumHeight(90)
        form.addRow("Déclencheur (JSON)", self.trigger_edit)
        right.addWidget(box)

        save_btn = QPushButton("Enregistrer la tactique personnalisée")
        save_btn.clicked.connect(self._on_save)
        right.addWidget(save_btn)
        right.addStretch(1)
        root.addLayout(right, stretch=2)

        self._refresh_lists()

    # ----------------------------------------------------------- helpers

    def _refresh_lists(self) -> None:
        self.custom_list.clear()
        self.official_list.clear()
        for tactic in sorted(self.registry.tactics.values(),
                             key=lambda t: (t.phase, t.side, t.name)):
            label = (f"{tactic.name} — "
                     f"{'ATK' if tactic.side == 'attacker' else 'DEF'} — "
                     f"{PHASE_LABELS.get(tactic.phase, tactic.phase)}")
            item = QListWidgetItem(label)
            item.setData(Qt.UserRole, tactic)
            (self.custom_list if tactic.custom else self.official_list).addItem(item)

    def _load_form(self, tactic: TacticDef) -> None:
        self.name_edit.setText(tactic.name)
        self.side_combo.setCurrentIndex(0 if tactic.side == "attacker" else 1)
        self.phase_combo.setCurrentIndex(max(self.phase_combo.findData(tactic.phase), 0))
        self.weight_spin.setValue(tactic.weight)
        self.atk_damage_spin.setValue(tactic.attacker_damage * 100)
        self.def_damage_spin.setValue(tactic.defender_damage * 100)
        self.width_spin.setValue(tactic.width * 100)
        self.movement_spin.setValue(tactic.movement * 100)
        self.countered_edit.setText(", ".join(tactic.countered_by))
        self.begins_combo.setCurrentIndex(
            max(self.begins_combo.findData(tactic.begins_phase or ""), 0))
        self.trigger_edit.setPlainText(
            json.dumps(tactic.trigger, ensure_ascii=False) if tactic.trigger else "")

    # ------------------------------------------------------------- slots

    def _on_select(self, item, _prev=None) -> None:
        if item is not None:
            self._load_form(item.data(Qt.UserRole))

    def _on_select_official(self, item, _prev=None) -> None:
        if item is not None:
            self._load_form(item.data(Qt.UserRole))

    def _on_delete(self) -> None:
        item = self.custom_list.currentItem()
        if item is None:
            return
        tactic = item.data(Qt.UserRole)
        if QMessageBox.question(self, "Supprimer",
                                f"Supprimer la tactique « {tactic.name} » ?") == QMessageBox.Yes:
            self.registry.remove_custom(tactic.key)
            self._refresh_lists()

    def _on_save(self) -> None:
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Nom manquant", "Donnez un nom à la tactique.")
            return
        trigger_text = self.trigger_edit.toPlainText().strip()
        trigger = None
        if trigger_text:
            try:
                trigger = json.loads(trigger_text)
            except json.JSONDecodeError as exc:
                QMessageBox.warning(self, "Déclencheur invalide", f"JSON invalide : {exc}")
                return
        tactic = TacticDef(
            name=name,
            side=self.side_combo.currentData(),
            phase=self.phase_combo.currentData(),
            weight=self.weight_spin.value(),
            trigger=trigger,
            countered_by=[s.strip() for s in self.countered_edit.text().split(",") if s.strip()],
            attacker_damage=self.atk_damage_spin.value() / 100.0,
            defender_damage=self.def_damage_spin.value() / 100.0,
            width=self.width_spin.value() / 100.0,
            movement=self.movement_spin.value() / 100.0,
            begins_phase=self.begins_combo.currentData() or None,
            custom=True,
        )
        self.registry.add_custom(tactic)
        self._refresh_lists()
        QMessageBox.information(self, "Enregistré", f"Tactique « {name} » enregistrée.")
