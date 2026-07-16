"""Gestionnaire de sauvegardes de bataille nommées (CDC §10.5, §12)."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QHBoxLayout, QInputDialog, QListWidget, QListWidgetItem,
    QMessageBox, QPushButton, QVBoxLayout,
)

from persistence.battles import BattleSaveStore


class SaveManager(QDialog):
    """Liste des sauvegardes : sauvegarder, charger, renommer, supprimer."""

    def __init__(self, store: BattleSaveStore, get_battle, get_log_text,
                 on_loaded, registry=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sauvegardes de bataille")
        self.resize(520, 420)
        self.store = store
        self.get_battle = get_battle
        self.get_log_text = get_log_text
        self.on_loaded = on_loaded
        self.registry = registry

        layout = QVBoxLayout(self)
        self.save_list = QListWidget()
        layout.addWidget(self.save_list, stretch=1)

        row1 = QHBoxLayout()
        save_btn = QPushButton("Sauvegarder la bataille actuelle sous…")
        save_btn.clicked.connect(self._on_save)
        row1.addWidget(save_btn)
        load_btn = QPushButton("Charger")
        load_btn.clicked.connect(self._on_load)
        row1.addWidget(load_btn)
        layout.addLayout(row1)

        row2 = QHBoxLayout()
        rename_btn = QPushButton("Renommer")
        rename_btn.clicked.connect(self._on_rename)
        row2.addWidget(rename_btn)
        delete_btn = QPushButton("Supprimer")
        delete_btn.clicked.connect(self._on_delete)
        row2.addWidget(delete_btn)
        layout.addLayout(row2)

        self._refresh()

    def _refresh(self) -> None:
        self.save_list.clear()
        for info in self.store.list_saves():
            status = f"tour {info['round']}"
            if info["resultat"] == "attacker":
                status += ", victoire attaquant"
            elif info["resultat"] == "defender":
                status += ", victoire défenseur"
            item = QListWidgetItem(f"{info['nom']}  ({status})")
            item.setData(Qt.UserRole, info["nom"])
            self.save_list.addItem(item)

    def _selected_name(self) -> str | None:
        item = self.save_list.currentItem()
        return item.data(Qt.UserRole) if item else None

    def _on_save(self) -> None:
        name, ok = QInputDialog.getText(self, "Nom de la sauvegarde",
                                        "Nom :")
        if not ok or not name.strip():
            return
        name = name.strip()
        existing = {info["nom"] for info in self.store.list_saves()}
        if name in existing and QMessageBox.question(
                self, "Écraser ?",
                f"La sauvegarde « {name} » existe déjà. L'écraser ?") != QMessageBox.Yes:
            return
        self.store.save(name, self.get_battle(), self.get_log_text())
        self._refresh()

    def _on_load(self) -> None:
        name = self._selected_name()
        if name is None:
            return
        try:
            battle, log_text = self.store.load(name, self.registry)
        except (OSError, KeyError, ValueError) as exc:
            QMessageBox.warning(self, "Erreur", f"Chargement impossible : {exc}")
            return
        self.on_loaded(battle, log_text)
        self.accept()

    def _on_rename(self) -> None:
        name = self._selected_name()
        if name is None:
            return
        new_name, ok = QInputDialog.getText(self, "Renommer", "Nouveau nom :",
                                            text=name)
        if ok and new_name.strip() and new_name.strip() != name:
            if not self.store.rename(name, new_name.strip()):
                QMessageBox.warning(self, "Erreur",
                                    "Renommage impossible (nom déjà pris ?).")
            self._refresh()

    def _on_delete(self) -> None:
        name = self._selected_name()
        if name is None:
            return
        if QMessageBox.question(self, "Supprimer",
                                f"Supprimer la sauvegarde « {name} » ?") == QMessageBox.Yes:
            self.store.delete(name)
            self._refresh()
