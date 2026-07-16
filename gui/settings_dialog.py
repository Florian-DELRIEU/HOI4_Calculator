"""Dialogue de paramètres (bouton « Paramètres »).

Construit automatiquement ses widgets depuis ``engine.settings.FIELD_META``.
Permet de configurer/activer/désactiver les paramètres, de les enregistrer
sur disque, de les recharger, et de rétablir les valeurs par défaut.
Les modifications validées (OK / Appliquer) prennent effet immédiatement
pour les batailles suivantes (l'objet SETTINGS est partagé par le moteur)."""
from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox, QDialog, QDoubleSpinBox, QFormLayout, QGroupBox, QHBoxLayout,
    QMessageBox, QPushButton, QSpinBox, QVBoxLayout,
)

from engine import settings as settings_module
from engine.settings import DEFAULTS, FIELD_META, GROUP_ORDER, SETTINGS


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Paramètres")
        self.resize(560, 620)
        self.widgets: dict[str, object] = {}

        root = QVBoxLayout(self)

        # Un groupe (QGroupBox) par catégorie déclarée dans FIELD_META.
        groups: dict[str, QFormLayout] = {}
        for group_name in GROUP_ORDER:
            box = QGroupBox(group_name)
            form = QFormLayout(box)
            groups[group_name] = form
            root.addWidget(box)

        for key, label, kind, lo, hi, step, group, help_text in FIELD_META:
            widget = self._make_widget(kind, lo, hi, step)
            if help_text:
                widget.setToolTip(help_text)
            self.widgets[key] = widget
            form = groups.get(group)
            if form is not None:
                if kind == "bool":
                    widget.setText(label)
                    form.addRow(widget)
                else:
                    form.addRow(label, widget)

        # --- Boutons de gestion ---
        manage_row = QHBoxLayout()
        reset_btn = QPushButton("Rétablir par défaut")
        reset_btn.clicked.connect(self._on_reset)
        load_btn = QPushButton("Charger")
        load_btn.clicked.connect(self._on_load)
        save_btn = QPushButton("Enregistrer")
        save_btn.clicked.connect(self._on_save)
        manage_row.addWidget(reset_btn)
        manage_row.addWidget(load_btn)
        manage_row.addWidget(save_btn)
        root.addLayout(manage_row)

        # --- Validation ---
        action_row = QHBoxLayout()
        action_row.addStretch(1)
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self._on_ok)
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(self.reject)
        action_row.addWidget(ok_btn)
        action_row.addWidget(cancel_btn)
        root.addLayout(action_row)

        self._load_into_widgets(SETTINGS.to_dict())

    # ------------------------------------------------------------- widgets

    @staticmethod
    def _make_widget(kind: str, lo, hi, step):
        if kind == "bool":
            return QCheckBox()
        if kind == "int":
            spin = QSpinBox()
            spin.setRange(int(lo), int(hi))
            spin.setSingleStep(int(step) or 1)
            return spin
        spin = QDoubleSpinBox()
        spin.setRange(float(lo), float(hi))
        spin.setSingleStep(float(step) or 0.01)
        spin.setDecimals(3 if step and step < 0.01 else 2)
        return spin

    def _load_into_widgets(self, data: dict) -> None:
        for key, widget in self.widgets.items():
            if key not in data:
                continue
            value = data[key]
            if isinstance(widget, QCheckBox):
                widget.setChecked(bool(value))
            elif isinstance(widget, QSpinBox):
                widget.setValue(int(value))
            elif isinstance(widget, QDoubleSpinBox):
                widget.setValue(float(value))

    def _collect_from_widgets(self) -> dict:
        data = {}
        for key, widget in self.widgets.items():
            if isinstance(widget, QCheckBox):
                data[key] = widget.isChecked()
            elif isinstance(widget, QSpinBox):
                data[key] = widget.value()
            elif isinstance(widget, QDoubleSpinBox):
                data[key] = widget.value()
        return data

    # --------------------------------------------------------------- slots

    def _apply_to_settings(self) -> None:
        SETTINGS.update_from(self._collect_from_widgets())

    def _on_reset(self) -> None:
        if QMessageBox.question(
                self, "Rétablir par défaut",
                "Rétablir tous les paramètres à leurs valeurs par défaut ?") == QMessageBox.Yes:
            self._load_into_widgets(DEFAULTS.to_dict())

    def _on_load(self) -> None:
        # Charge depuis le disque dans SETTINGS puis rafraîchit les widgets.
        settings_module.load()
        self._load_into_widgets(SETTINGS.to_dict())
        QMessageBox.information(self, "Chargé",
                               "Paramètres rechargés depuis le disque.")

    def _on_save(self) -> None:
        self._apply_to_settings()
        settings_module.save()
        QMessageBox.information(self, "Enregistré",
                               f"Paramètres enregistrés dans :\n{settings_module.SETTINGS_PATH}")

    def _on_ok(self) -> None:
        self._apply_to_settings()   # effet immédiat, sans écrire sur le disque
        self.accept()
