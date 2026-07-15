"""Éditeur de division (CDC §10.2) : composition par bataillons OU édition
manuelle des statistiques finales (mode « debug »), les deux coexistant."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QDialog, QDoubleSpinBox, QFormLayout, QGroupBox, QHBoxLayout,
    QInputDialog, QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMessageBox, QPushButton, QSpinBox, QTabWidget, QVBoxLayout, QWidget,
)

from engine import composition
from engine.division import (EXPERIENCE_LABELS, DivisionStats, DivisionTemplate)
from persistence.divisions import DivisionStore

STAT_FIELDS = [
    ("hp", "PV", 0, 10000),
    ("organisation", "Organisation", 0, 1000),
    ("soft_attack", "Attaque douce (soft attack)", 0, 10000),
    ("hard_attack", "Attaque dure (hard attack)", 0, 10000),
    ("air_attack", "Attaque aérienne", 0, 10000),
    ("defense", "Défense", 0, 10000),
    ("breakthrough", "Percée (breakthrough)", 0, 10000),
    ("armor", "Blindage (armor)", 0, 1000),
    ("piercing", "Perce-blindage (piercing)", 0, 1000),
    ("hardness", "Dureté (0 à 1)", 0, 1),
    ("width", "Largeur de combat", 0, 200),
    ("initiative", "Initiative", 0, 1),
    ("speed", "Vitesse max (km/h)", 0, 50),
]


class DivisionEditor(QDialog):
    def __init__(self, store: DivisionStore | None = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Éditeur de divisions")
        self.resize(1020, 640)
        self.store = store or DivisionStore()
        self.current: DivisionTemplate | None = None

        root = QHBoxLayout(self)

        # ------------------------------------------------------ liste gauche
        left = QVBoxLayout()
        self.template_list = QListWidget()
        self.template_list.currentItemChanged.connect(self._on_select)
        left.addWidget(self.template_list, stretch=1)
        row1 = QHBoxLayout()
        for label, slot in (("Nouveau", self._on_new), ("Dupliquer", self._on_duplicate)):
            btn = QPushButton(label)
            btn.clicked.connect(slot)
            row1.addWidget(btn)
        left.addLayout(row1)
        row2 = QHBoxLayout()
        for label, slot in (("Renommer", self._on_rename), ("Supprimer", self._on_delete)):
            btn = QPushButton(label)
            btn.clicked.connect(slot)
            row2.addWidget(btn)
        left.addLayout(row2)
        root.addLayout(left, stretch=1)

        # -------------------------------------------------- formulaire droit
        right = QVBoxLayout()
        header = QFormLayout()
        self.name_edit = QLineEdit()
        header.addRow("Nom du template", self.name_edit)
        self.folder_edit = QLineEdit()
        self.folder_edit.setPlaceholderText("Sous-dossier de rangement (optionnel), ex. Infanterie/1936")
        header.addRow("Dossier", self.folder_edit)
        self.experience_combo = QComboBox()
        for exp_id, label in EXPERIENCE_LABELS.items():
            self.experience_combo.addItem(label, exp_id)
        header.addRow("Expérience", self.experience_combo)
        self.recon_spin = QDoubleSpinBox()
        self.recon_spin.setRange(0, 100)
        header.addRow("Reconnaissance", self.recon_spin)
        right.addLayout(header)

        self.tabs = QTabWidget()
        right.addWidget(self.tabs, stretch=1)

        # --- Onglet composition
        comp_tab = QWidget()
        comp_layout = QVBoxLayout(comp_tab)

        line_box = QGroupBox("Bataillons de ligne (max 25)")
        line_layout = QVBoxLayout(line_box)
        add_line = QHBoxLayout()
        self.battalion_combo = QComboBox()
        for bid, b in sorted(composition.LINE_BATTALIONS.items(),
                             key=lambda kv: (kv[1].group, kv[1].nom)):
            self.battalion_combo.addItem(f"[{b.group}] {b.nom}", bid)
        self.battalion_count = QSpinBox()
        self.battalion_count.setRange(1, 25)
        self.battalion_count.setPrefix("×")
        add_line_btn = QPushButton("Ajouter")
        add_line_btn.clicked.connect(self._on_add_battalion)
        add_line.addWidget(self.battalion_combo, stretch=1)
        add_line.addWidget(self.battalion_count)
        add_line.addWidget(add_line_btn)
        line_layout.addLayout(add_line)
        self.battalion_list = QListWidget()
        line_layout.addWidget(self.battalion_list, stretch=1)
        rm_line_btn = QPushButton("Retirer la sélection")
        rm_line_btn.clicked.connect(lambda: self._remove_selected(self.battalion_list))
        line_layout.addWidget(rm_line_btn)
        comp_layout.addWidget(line_box, stretch=2)

        supp_box = QGroupBox("Compagnies de soutien (max 5)")
        supp_layout = QVBoxLayout(supp_box)
        add_supp = QHBoxLayout()
        self.support_combo = QComboBox()
        for sid, s in sorted(composition.SUPPORT_COMPANIES.items(),
                             key=lambda kv: kv[1].nom):
            self.support_combo.addItem(s.nom, sid)
        add_supp_btn = QPushButton("Ajouter")
        add_supp_btn.clicked.connect(self._on_add_support)
        add_supp.addWidget(self.support_combo, stretch=1)
        add_supp.addWidget(add_supp_btn)
        supp_layout.addLayout(add_supp)
        self.support_list = QListWidget()
        supp_layout.addWidget(self.support_list)
        rm_supp_btn = QPushButton("Retirer la sélection")
        rm_supp_btn.clicked.connect(lambda: self._remove_selected(self.support_list))
        supp_layout.addWidget(rm_supp_btn)
        comp_layout.addWidget(supp_box, stretch=1)

        self.preview_label = QLabel("—")
        self.preview_label.setWordWrap(True)
        comp_layout.addWidget(self.preview_label)
        apply_btn = QPushButton("Recalculer les statistiques depuis la composition (§6.1)")
        apply_btn.clicked.connect(self._on_apply_composition)
        comp_layout.addWidget(apply_btn)

        self.tabs.addTab(comp_tab, "Composition (fidèle au jeu)")

        # --- Onglet stats manuelles
        stats_tab = QWidget()
        stats_form = QFormLayout(stats_tab)
        self.stat_spins: dict[str, QDoubleSpinBox] = {}
        for attr, label, lo, hi in STAT_FIELDS:
            spin = QDoubleSpinBox()
            spin.setRange(lo, hi)
            spin.setDecimals(3 if hi <= 1 else 2)
            spin.setSingleStep(0.05 if hi <= 1 else 1.0)
            stats_form.addRow(label, spin)
            self.stat_spins[attr] = spin
        self.tabs.addTab(stats_tab, "Statistiques (manuel / debug)")

        save_btn = QPushButton("Enregistrer le template")
        save_btn.clicked.connect(self._on_save)
        right.addWidget(save_btn)
        root.addLayout(right, stretch=3)

        self._refresh_list()

    # ------------------------------------------------------------- helpers

    def _refresh_list(self, select: str | None = None) -> None:
        self.template_list.clear()
        for template in sorted(self.store.list_templates(),
                               key=lambda t: (t.folder, t.name)):
            label = f"{template.folder}/{template.name}" if template.folder else template.name
            item = QListWidgetItem(label)
            item.setData(Qt.UserRole, template)
            self.template_list.addItem(item)
            if select and template.name == select:
                self.template_list.setCurrentItem(item)

    def _load_form(self, template: DivisionTemplate) -> None:
        self.current = template
        self.name_edit.setText(template.name)
        self.folder_edit.setText(template.folder)
        idx = self.experience_combo.findData(template.experience)
        self.experience_combo.setCurrentIndex(max(idx, 0))
        self.recon_spin.setValue(template.recon)
        self.battalion_list.clear()
        for bid in template.battalions:
            self._append_unit(self.battalion_list, bid)
        self.support_list.clear()
        for sid in template.support_companies:
            self._append_unit(self.support_list, sid)
        for attr, spin in self.stat_spins.items():
            spin.setValue(getattr(template.stats, attr))
        self._refresh_preview()

    def _append_unit(self, widget: QListWidget, unit_id: str) -> None:
        b = composition.BATTALIONS.get(unit_id)
        item = QListWidgetItem(b.nom if b else unit_id)
        item.setData(Qt.UserRole, unit_id)
        widget.addItem(item)

    def _collect_composition(self) -> tuple[list[str], list[str]]:
        battalions = [self.battalion_list.item(i).data(Qt.UserRole)
                      for i in range(self.battalion_list.count())]
        supports = [self.support_list.item(i).data(Qt.UserRole)
                    for i in range(self.support_list.count())]
        return battalions, supports

    def _refresh_preview(self) -> None:
        battalions, supports = self._collect_composition()
        if not battalions and not supports:
            self.preview_label.setText("Composition vide — mode manuel pur.")
            return
        problems = composition.validate(battalions, supports)
        if problems:
            self.preview_label.setText("⚠ " + " ; ".join(problems))
            return
        stats, recon = composition.aggregate(battalions, supports)
        self.preview_label.setText(
            f"Aperçu — PV {stats.hp} | Org {stats.organisation} | "
            f"SA {stats.soft_attack} | HA {stats.hard_attack} | "
            f"Déf {stats.defense} | Percée {stats.breakthrough} | "
            f"Blind. {stats.armor} | Perce. {stats.piercing} | "
            f"Dureté {stats.hardness:.0%} | Largeur {stats.width:g} | "
            f"Vitesse {stats.speed:g} km/h | Init. {stats.initiative:g} | Recon {recon:g}")

    # ------------------------------------------------------------- slots

    def _on_select(self, item, _prev=None) -> None:
        if item is not None:
            self._load_form(item.data(Qt.UserRole))

    def _on_new(self) -> None:
        self._load_form(DivisionTemplate(name="Nouvelle division"))

    def _on_duplicate(self) -> None:
        item = self.template_list.currentItem()
        if item is None:
            return
        template = item.data(Qt.UserRole)
        copy = self.store.duplicate(template.name)
        if copy:
            self._refresh_list(select=copy.name)

    def _on_rename(self) -> None:
        item = self.template_list.currentItem()
        if item is None:
            return
        template = item.data(Qt.UserRole)
        new_name, ok = QInputDialog.getText(self, "Renommer", "Nouveau nom :",
                                            text=template.name)
        if ok and new_name.strip() and new_name != template.name:
            self.store.rename(template.name, new_name.strip())
            self._refresh_list(select=new_name.strip())

    def _on_delete(self) -> None:
        item = self.template_list.currentItem()
        if item is None:
            return
        template = item.data(Qt.UserRole)
        if QMessageBox.question(self, "Supprimer",
                                f"Supprimer « {template.name} » ?") == QMessageBox.Yes:
            self.store.delete(template.name)
            self._refresh_list()

    def _on_add_battalion(self) -> None:
        bid = self.battalion_combo.currentData()
        count = self.battalion_count.value()
        if self.battalion_list.count() + count > composition.MAX_LINE_BATTALIONS:
            QMessageBox.warning(self, "Limite atteinte",
                                f"Maximum {composition.MAX_LINE_BATTALIONS} bataillons de ligne.")
            return
        for _ in range(count):
            self._append_unit(self.battalion_list, bid)
        self._refresh_preview()

    def _on_add_support(self) -> None:
        sid = self.support_combo.currentData()
        existing = [self.support_list.item(i).data(Qt.UserRole)
                    for i in range(self.support_list.count())]
        if sid in existing:
            QMessageBox.warning(self, "Doublon", "Cette compagnie est déjà présente.")
            return
        if self.support_list.count() >= composition.MAX_SUPPORT_COMPANIES:
            QMessageBox.warning(self, "Limite atteinte",
                                f"Maximum {composition.MAX_SUPPORT_COMPANIES} compagnies de soutien.")
            return
        self._append_unit(self.support_list, sid)
        self._refresh_preview()

    def _remove_selected(self, widget: QListWidget) -> None:
        row = widget.currentRow()
        if row >= 0:
            widget.takeItem(row)
            self._refresh_preview()

    def _on_apply_composition(self) -> None:
        battalions, supports = self._collect_composition()
        problems = composition.validate(battalions, supports)
        if problems:
            QMessageBox.warning(self, "Composition invalide", "\n".join(problems))
            return
        stats, recon = composition.aggregate(battalions, supports)
        for attr, spin in self.stat_spins.items():
            spin.setValue(getattr(stats, attr))
        self.recon_spin.setValue(recon)
        self._refresh_preview()
        self.tabs.setCurrentIndex(1)   # montre le résultat dans l'onglet stats

    def _on_save(self) -> None:
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Nom manquant", "Donnez un nom au template.")
            return
        battalions, supports = self._collect_composition()
        if battalions or supports:
            problems = composition.validate(battalions, supports)
            if problems:
                QMessageBox.warning(self, "Composition invalide", "\n".join(problems))
                return
        stats = DivisionStats(**{attr: spin.value() for attr, spin in self.stat_spins.items()})
        template = DivisionTemplate(
            name=name,
            stats=stats,
            experience=self.experience_combo.currentData(),
            recon=self.recon_spin.value(),
            battalions=battalions,
            support_companies=supports,
            folder=self.folder_edit.text().strip().replace("\\", "/"),
        )
        old_name = self.current.name if self.current else None
        if old_name and old_name != name:
            pass  # nouveau fichier : l'ancien template est conservé (duplication implicite)
        self.store.save(template)
        self.current = template
        self._refresh_list(select=name)
        QMessageBox.information(self, "Enregistré", f"Template « {name} » enregistré.")
