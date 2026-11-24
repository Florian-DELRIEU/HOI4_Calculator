"""Éditeur de division (CDC §10.2) : concepteur de division à la manière du
jeu (grille 5×5 de bataillons + 5 compagnies de soutien) OU édition manuelle
des statistiques finales (mode « debug »), les deux coexistant."""
from __future__ import annotations

from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import (
    QComboBox, QDialog, QDoubleSpinBox, QFormLayout, QGridLayout, QGroupBox,
    QHBoxLayout, QInputDialog, QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMessageBox, QPushButton, QTabWidget, QToolButton, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget,
)

from engine import composition
from engine.composition import GRID_COLS, GRID_ROWS, MAX_SUPPORT_COMPANIES
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

GROUP_LABELS = {
    "infanterie": "Infanterie",
    "mobile": "Mobiles",
    "artillerie": "Appui de combat",
    "blinde": "Blindés",
    "soutien": "Compagnies de soutien",
}
# Teinte des cases par groupe (translucide : lisible en thème clair et sombre).
GROUP_COLORS = {
    "infanterie": "90, 150, 90",
    "mobile": "190, 150, 60",
    "artillerie": "190, 90, 80",
    "blinde": "90, 120, 190",
    "soutien": "150, 110, 180",
}
CELL_W, CELL_H = 104, 54


def _unit_tooltip(b: composition.BattalionDef) -> str:
    lines = [f"<b>{b.nom}</b> — {GROUP_LABELS.get(b.group, b.group)}"]
    if b.line:
        lines.append(f"Largeur {b.width:g} · Vitesse {b.speed:g} km/h · "
                     f"Dureté {b.hardness:.0%}")
    lines.append(f"PV {b.hp:g} · Org {b.org:g}")
    lines.append(f"Att. douce {b.soft:g} · Att. dure {b.hard:g}"
                 + (f" · Att. air {b.air:g}" if b.air else ""))
    lines.append(f"Défense {b.defense:g} · Percée {b.breakthrough:g} · "
                 f"Blindage {b.armor:g} · Perce-blindage {b.piercing:g}")
    if b.manpower or b.ic_cost:
        lines.append(f"Effectif {b.manpower:g} · Coût {b.ic_cost:g} IC · "
                     f"Ravitaillement {b.supply_use:g}")
    if b.special:
        lines.append(f"<i>{b.special}</i>")
    if b.exclusion:
        lines.append(f"Famille exclusive : {b.exclusion}")
    if b.note:
        lines.append(f"⚠ {b.note}")
    return "<br>".join(lines)


class _Cell(QToolButton):
    """Case de la grille : clic gauche = poser, clic droit = vider."""

    def __init__(self, index: int, on_place, on_clear, width: int = CELL_W):
        super().__init__()
        self.index = index
        self._on_place = on_place
        self._on_clear = on_clear
        self._max_chars = 17 if width <= CELL_W else 26
        self.setFixedSize(width, CELL_H)
        self.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.clicked.connect(lambda: self._on_place(self.index))
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(lambda _pos: self._on_clear(self.index))
        self._unit_id: str | None = None

    def changeEvent(self, event) -> None:
        # Les feuilles de style figent la palette : on les réapplique quand
        # le thème clair/sombre bascule.
        if event.type() == QEvent.PaletteChange:
            self.show_unit(self._unit_id)
        super().changeEvent(event)

    def show_unit(self, unit_id: str | None) -> None:
        self._unit_id = unit_id
        b = composition.BATTALIONS.get(unit_id) if unit_id else None
        if unit_id and b is None:        # id inconnu (ex. bataillon supprimé)
            self.setText(f"? {unit_id}"[:16])
            self.setToolTip(f"Unité inconnue : {unit_id}")
            self.setStyleSheet("QToolButton { border: 1px dashed #c33; }")
            return
        if b is None:
            self.setText("")
            self.setToolTip("Case vide — choisissez une unité dans la palette, "
                            "puis cliquez ici. Clic droit pour vider.")
            self.setStyleSheet("QToolButton { border: 1px dashed palette(mid); }")
            return
        name = b.nom if len(b.nom) <= self._max_chars else b.nom[:self._max_chars - 1] + "…"
        size = f"L{b.width:g}" if b.line else "soutien"
        self.setText(f"{name}\n{size}")
        self.setToolTip(_unit_tooltip(b))
        color = GROUP_COLORS.get(b.group, "128, 128, 128")
        self.setStyleSheet(
            f"QToolButton {{ background-color: rgba({color}, 90); "
            f"border: 1px solid rgba({color}, 220); border-radius: 3px; "
            f"color: palette(button-text); font-size: 11px; }}")


class DivisionEditor(QDialog):
    def __init__(self, store: DivisionStore | None = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Éditeur de divisions")
        self.resize(1240, 760)
        self.store = store or DivisionStore()
        self.current: DivisionTemplate | None = None
        # Composition en cours d'édition
        self.slots: list[str | None] = [None] * composition.MAX_LINE_BATTALIONS
        self.support_slots: list[str | None] = [None] * MAX_SUPPORT_COMPANIES
        self.brush: str | None = None
        self._loading = False

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
        self.tabs.addTab(self._build_designer_tab(), "Concepteur (fidèle au jeu)")

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
        root.addLayout(right, stretch=4)

        self._refresh_list()
        self._refresh_composition(apply_stats=False)

    # ------------------------------------------------------- onglet concepteur

    def _build_designer_tab(self) -> QWidget:
        tab = QWidget()
        outer = QVBoxLayout(tab)
        body = QHBoxLayout()
        outer.addLayout(body, stretch=1)

        # Palette d'unités
        palette_box = QGroupBox("Unités (cliquer pour choisir, puis poser)")
        palette_layout = QVBoxLayout(palette_box)
        self.palette = QTreeWidget()
        self.palette.setHeaderHidden(True)
        self.palette.currentItemChanged.connect(self._on_palette_select)
        palette_layout.addWidget(self.palette)
        self.brush_label = QLabel("Aucune unité sélectionnée.")
        self.brush_label.setWordWrap(True)
        palette_layout.addWidget(self.brush_label)
        self._fill_palette()
        body.addWidget(palette_box, stretch=2)

        # Grille 5×5 + soutien
        design_box = QGroupBox(
            f"Division — {GRID_COLS} colonnes × {GRID_ROWS} rangées "
            f"(max {composition.MAX_LINE_BATTALIONS} bataillons)")
        design_layout = QVBoxLayout(design_box)
        grid = QGridLayout()
        grid.setHorizontalSpacing(4)
        grid.setVerticalSpacing(4)
        self.cells: list[_Cell] = []
        for col in range(GRID_COLS):
            fill = QPushButton("▼ Colonne")
            fill.setToolTip("Remplir toute la colonne avec l'unité choisie")
            fill.clicked.connect(lambda _=False, c=col: self._fill_column(c))
            grid.addWidget(fill, 0, col)
        for col in range(GRID_COLS):
            for row in range(GRID_ROWS):
                cell = _Cell(col * GRID_ROWS + row, self._place_line, self._clear_line)
                grid.addWidget(cell, row + 1, col)
                self.cells.append(cell)
        design_layout.addLayout(grid)
        clear_btn = QPushButton("Tout vider")
        clear_btn.clicked.connect(self._clear_all)
        design_layout.addWidget(clear_btn)
        design_layout.addStretch(1)
        body.addWidget(design_box, stretch=0)

        support_box = QGroupBox(f"Soutien (max {MAX_SUPPORT_COMPANIES})")
        support_layout = QVBoxLayout(support_box)
        self.support_cells: list[_Cell] = []
        for i in range(MAX_SUPPORT_COMPANIES):
            cell = _Cell(i, self._place_support, self._clear_support,
                         width=int(CELL_W * 1.5))
            support_layout.addWidget(cell)
            self.support_cells.append(cell)
        support_layout.addStretch(1)
        body.addWidget(support_box, stretch=0)

        # Stats en direct
        self.preview_label = QLabel("—")
        self.preview_label.setTextFormat(Qt.RichText)
        self.preview_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        stats_box = QGroupBox("Statistiques de la division")
        stats_box.setMinimumWidth(270)
        stats_layout = QVBoxLayout(stats_box)
        stats_layout.addWidget(self.preview_label)
        self.status_label = QLabel("")
        self.status_label.setTextFormat(Qt.RichText)
        self.status_label.setWordWrap(True)
        stats_layout.addWidget(self.status_label)
        stats_layout.addStretch(1)
        body.addWidget(stats_box, stretch=1)

        apply_btn = QPushButton("Recalculer les statistiques depuis la composition")
        apply_btn.setToolTip("Réécrit l'onglet « Statistiques » à partir de la grille "
                             "(utile après une édition manuelle).")
        apply_btn.clicked.connect(self._on_apply_composition)
        outer.addWidget(apply_btn)
        return tab

    def _fill_palette(self) -> None:
        self.palette.clear()
        by_group: dict[str, list[tuple[str, composition.BattalionDef]]] = {}
        for uid, b in composition.BATTALIONS.items():
            by_group.setdefault(b.group, []).append((uid, b))
        order = [g for g in GROUP_LABELS if g in by_group] + \
                [g for g in by_group if g not in GROUP_LABELS]
        for group in order:
            top = QTreeWidgetItem([GROUP_LABELS.get(group, group)])
            top.setFlags(Qt.ItemIsEnabled)
            self.palette.addTopLevelItem(top)
            for uid, b in sorted(by_group[group], key=lambda kv: kv[1].nom):
                item = QTreeWidgetItem([b.nom])
                item.setData(0, Qt.UserRole, uid)
                item.setToolTip(0, _unit_tooltip(b))
                top.addChild(item)
            top.setExpanded(True)

    def _on_palette_select(self, item, _prev=None) -> None:
        uid = item.data(0, Qt.UserRole) if item is not None else None
        self.brush = uid
        b = composition.BATTALIONS.get(uid) if uid else None
        if b is None:
            self.brush_label.setText("Aucune unité sélectionnée.")
        elif b.line:
            self.brush_label.setText(f"Pinceau : <b>{b.nom}</b> → cases de la grille.")
        else:
            self.brush_label.setText(f"Pinceau : <b>{b.nom}</b> → emplacements de soutien.")

    # ---------------------------------------------------------- composition

    def _line_brush(self) -> str | None:
        b = composition.BATTALIONS.get(self.brush) if self.brush else None
        return self.brush if b is not None and b.line else None

    def _place_line(self, index: int) -> None:
        uid = self._line_brush()
        if uid is None:
            self._say("Choisissez d'abord un bataillon de ligne dans la palette.")
            return
        self.slots[index] = uid
        self._refresh_composition()

    def _clear_line(self, index: int) -> None:
        self.slots[index] = None
        self._refresh_composition()

    def _fill_column(self, col: int) -> None:
        uid = self._line_brush()
        if uid is None:
            self._say("Choisissez d'abord un bataillon de ligne dans la palette.")
            return
        for row in range(GRID_ROWS):
            self.slots[col * GRID_ROWS + row] = uid
        self._refresh_composition()

    def _clear_all(self) -> None:
        self.slots = [None] * composition.MAX_LINE_BATTALIONS
        self.support_slots = [None] * MAX_SUPPORT_COMPANIES
        self._refresh_composition()

    def _place_support(self, index: int) -> None:
        b = composition.BATTALIONS.get(self.brush) if self.brush else None
        if b is None or b.line:
            self._say("Choisissez d'abord une compagnie de soutien dans la palette.")
            return
        others = [s for i, s in enumerate(self.support_slots) if s and i != index]
        if self.brush in others:
            self._say(f"« {b.nom} » est déjà dans la division.")
            return
        blocker = composition.blocked_by(self.brush, others)
        if blocker is not None:
            self._say(f"« {b.nom} » est incompatible avec "
                      f"« {composition.BATTALIONS[blocker].nom} » (même famille).")
            return
        self.support_slots[index] = self.brush
        self._refresh_composition()

    def _clear_support(self, index: int) -> None:
        self.support_slots[index] = None
        self._refresh_composition()

    def _say(self, message: str) -> None:
        self.status_label.setText(f"<span style='color:#d9822b'>{message}</span>")

    def _collect_composition(self) -> tuple[list[str], list[str]]:
        return (composition.list_from_slots(self.slots),
                [s for s in self.support_slots if s])

    def _refresh_composition(self, apply_stats: bool = True) -> None:
        """Redessine la grille et recalcule l'aperçu. Avec ``apply_stats``,
        les statistiques de l'onglet manuel suivent la composition."""
        for cell, uid in zip(self.cells, self.slots):
            cell.show_unit(uid)
        for cell, uid in zip(self.support_cells, self.support_slots):
            cell.show_unit(uid)
        self.status_label.setText("")
        self.preview_label.setWordWrap(False)
        battalions, supports = self._collect_composition()
        if not battalions and not supports:
            self.preview_label.setText("Composition vide — mode manuel pur.")
            return
        problems = composition.validate(battalions, supports)
        if problems:
            self.preview_label.setText(
                "<span style='color:#d9534f'>⚠ " + "<br>⚠ ".join(problems) + "</span>")
            self.preview_label.setWordWrap(True)
            return
        stats, recon = composition.aggregate(battalions, supports)
        info = composition.design_info(battalions, supports)
        self.preview_label.setText(self._format_preview(
            stats, recon, info, len(battalions), len(supports)))
        if apply_stats and not self._loading:
            self._apply_stats(stats, recon)

    @staticmethod
    def _format_preview(stats: DivisionStats, recon: float,
                        info: composition.DesignInfo, n_line: int, n_supp: int) -> str:
        rows = [
            ("Bataillons / soutiens", f"{n_line} / {n_supp}"),
            ("PV", f"{stats.hp:g}"),
            ("Organisation", f"{stats.organisation:g}"),
            ("Attaque douce", f"{stats.soft_attack:g}"),
            ("Attaque dure", f"{stats.hard_attack:g}"),
            ("Attaque aérienne", f"{stats.air_attack:g}"),
            ("Défense", f"{stats.defense:g}"),
            ("Percée", f"{stats.breakthrough:g}"),
            ("Blindage", f"{stats.armor:g}"),
            ("Perce-blindage", f"{stats.piercing:g}"),
            ("Dureté", f"{stats.hardness:.0%}"),
            ("Largeur de combat", f"{stats.width:g}"),
            ("Vitesse", f"{stats.speed:g} km/h"),
            ("Initiative", f"{stats.initiative:g}"),
            ("Reconnaissance", f"{recon:g}"),
            ("Effectif", f"{info.manpower:,.0f}".replace(",", " ")),
            ("Entraînement", f"{info.training_days:g} j"),
            ("Coût de production", f"{info.ic_cost:g} IC"),
            ("Ravitaillement", f"{info.supply_use:g}"),
            ("Carburant (cap. / conso)", f"{info.fuel_capacity:g} / {info.fuel_use:g}"),
        ]
        body = "".join(f"<tr><td>{k}&nbsp;&nbsp;</td><td align='right'><b>{v}</b></td></tr>"
                       for k, v in rows)
        return f"<table cellspacing='2'>{body}</table>"

    def _apply_stats(self, stats: DivisionStats, recon: float) -> None:
        for attr, spin in self.stat_spins.items():
            spin.setValue(getattr(stats, attr))
        self.recon_spin.setValue(recon)

    def _on_apply_composition(self) -> None:
        battalions, supports = self._collect_composition()
        problems = composition.validate(battalions, supports)
        if problems:
            QMessageBox.warning(self, "Composition invalide", "\n".join(problems))
            return
        stats, recon = composition.aggregate(battalions, supports)
        self._apply_stats(stats, recon)
        self._say("Statistiques recalculées depuis la composition.")

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
        for attr, spin in self.stat_spins.items():
            spin.setValue(getattr(template.stats, attr))
        # La composition est chargée sans toucher aux stats enregistrées
        # (un template peut avoir des stats manuelles).
        self._loading = True
        self.slots = list(template.grid) if len(template.grid) == composition.MAX_LINE_BATTALIONS \
            else composition.slots_from_list(template.battalions)
        self.support_slots = (list(template.support_companies) + [None] * MAX_SUPPORT_COMPANIES
                              )[:MAX_SUPPORT_COMPANIES]
        self._refresh_composition(apply_stats=False)
        self._loading = False

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
            grid=list(self.slots) if battalions else [],
            folder=self.folder_edit.text().strip().replace("\\", "/"),
        )
        self.store.save(template)
        self.current = template
        self._refresh_list(select=name)
        QMessageBox.information(self, "Enregistré", f"Template « {name} » enregistré.")
