"""Fenêtre principale de bataille (CDC §10.1)."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QDoubleSpinBox, QFormLayout, QGroupBox, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QMainWindow, QMessageBox,
    QPlainTextEdit, QProgressBar, QPushButton, QSpinBox, QSplitter,
    QVBoxLayout, QWidget,
)

from engine.battle import Battle
from engine.gamedata import TERRAINS, WEATHER
from engine.leader import Leader
from engine.params import BattleParams
from persistence.divisions import DivisionStore


class CampPanel(QGroupBox):
    """Panneau d'un camp : divisions engagées + leader."""

    def __init__(self, title: str, is_attacker: bool, store: DivisionStore,
                 parent=None):
        super().__init__(title, parent)
        self.is_attacker = is_attacker
        self.store = store

        layout = QVBoxLayout(self)

        # Ajout de divisions depuis les templates
        add_row = QHBoxLayout()
        self.template_combo = QComboBox()
        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 24)
        self.count_spin.setPrefix("×")
        add_btn = QPushButton("Ajouter")
        add_btn.clicked.connect(self._on_add)
        add_row.addWidget(self.template_combo, stretch=1)
        add_row.addWidget(self.count_spin)
        add_row.addWidget(add_btn)
        layout.addLayout(add_row)

        self.division_list = QListWidget()
        layout.addWidget(self.division_list, stretch=1)

        remove_btn = QPushButton("Retirer la division sélectionnée")
        remove_btn.clicked.connect(self._on_remove)
        layout.addWidget(remove_btn)

        # Leader
        leader_box = QGroupBox("Leader")
        leader_form = QFormLayout(leader_box)
        self.leader_attack = QSpinBox()
        self.leader_attack.setRange(0, 10)
        self.leader_defense = QSpinBox()
        self.leader_defense.setRange(0, 10)
        leader_form.addRow("Compétence attaque", self.leader_attack)
        leader_form.addRow("Compétence défense", self.leader_defense)
        layout.addWidget(leader_box)

        self.battle: Battle | None = None
        self.refresh_templates()

    @property
    def camp(self):
        if self.battle is None:
            return None
        return self.battle.attacker if self.is_attacker else self.battle.defender

    def refresh_templates(self) -> None:
        current = self.template_combo.currentText()
        self.template_combo.clear()
        for template in self.store.list_templates():
            label = f"{template.folder}/{template.name}" if template.folder else template.name
            self.template_combo.addItem(label, template)
        index = self.template_combo.findText(current)
        if index >= 0:
            self.template_combo.setCurrentIndex(index)

    def sync_leader(self) -> None:
        if self.camp is not None:
            self.camp.leader = Leader(
                name="Leader", attack_level=self.leader_attack.value(),
                defense_level=self.leader_defense.value())

    def _on_add(self) -> None:
        if self.camp is None:
            return
        template = self.template_combo.currentData()
        if template is None:
            QMessageBox.information(self, "Aucun template",
                                    "Créez d'abord un template de division.")
            return
        for _ in range(self.count_spin.value()):
            self.camp.add_division(template.spawn())
        self.refresh_divisions()

    def _on_remove(self) -> None:
        row = self.division_list.currentRow()
        if self.camp is None or row < 0:
            return
        division = self.division_list.item(row).data(Qt.UserRole)
        for group in (self.camp.divisions, self.camp.frontline, self.camp.reserves):
            if division in group:
                group.remove(division)
        self.refresh_divisions()

    def refresh_divisions(self) -> None:
        self.division_list.clear()
        if self.camp is None:
            return
        for division in self.camp.divisions:
            if division in self.camp.frontline:
                where = "front"
            elif division in self.camp.reserves:
                where = "réserve"
            elif division in self.camp.retreated:
                where = "replié"
            elif division in self.camp.destroyed:
                where = "détruite"
            else:
                where = "en attente"
            text = (f"{division.name} [{where}] — "
                    f"PV {division.current_hp:.1f}/{division.stats.hp:.0f} | "
                    f"ORG {division.current_org:.1f}/{division.stats.organisation:.0f}")
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, division)
            if division.is_destroyed:
                item.setForeground(Qt.red)
            elif division.is_broken:
                item.setForeground(Qt.darkYellow)
            self.division_list.addItem(item)


class ParamsPanel(QGroupBox):
    """Paramètres de bataille : terrain, météo, fort, modificateurs manuels."""

    def __init__(self, parent=None):
        super().__init__("Paramètres de bataille", parent)
        form = QFormLayout(self)

        self.terrain_combo = QComboBox()
        for tid, terrain in TERRAINS.items():
            self.terrain_combo.addItem(terrain.nom, tid)
        form.addRow("Terrain", self.terrain_combo)

        self.weather_combo = QComboBox()
        for wid, weather in WEATHER.items():
            self.weather_combo.addItem(weather.nom, wid)
        form.addRow("Météo", self.weather_combo)

        self.night_check = QCheckBox("Nuit (−50 % attaque)")
        form.addRow(self.night_check)

        self.river_combo = QComboBox()
        self.river_combo.addItems(["Aucune rivière", "Petite rivière (−30 %)",
                                   "Grande rivière (−60 %)"])
        form.addRow("Rivière", self.river_combo)

        self.naval_check = QCheckBox("Débarquement amphibie (−50 %)")
        form.addRow(self.naval_check)

        self.fort_spin = QSpinBox()
        self.fort_spin.setRange(0, 10)
        form.addRow("Niveau de fort", self.fort_spin)

        self.directions_spin = QSpinBox()
        self.directions_spin.setRange(0, 4)
        form.addRow("Directions d'attaque suppl.", self.directions_spin)

        self.encirclement_check = QCheckBox("Défenseur encerclé (−30 %)")
        form.addRow(self.encirclement_check)

        self.entrenchment_spin = QSpinBox()
        self.entrenchment_spin.setRange(0, 50)
        form.addRow("Retranchement défenseur", self.entrenchment_spin)

        self.planning_spin = QDoubleSpinBox()
        self.planning_spin.setRange(0.0, 30.0)
        self.planning_spin.setSuffix(" %")
        form.addRow("Bonus de planification", self.planning_spin)

    def apply_to(self, params: BattleParams) -> None:
        params.terrain_id = self.terrain_combo.currentData()
        params.weather_id = self.weather_combo.currentData()
        params.is_night = self.night_check.isChecked()
        params.small_river = self.river_combo.currentIndex() == 1
        params.large_river = self.river_combo.currentIndex() == 2
        params.naval_invasion = self.naval_check.isChecked()
        params.fort_level = self.fort_spin.value()
        params.extra_directions = self.directions_spin.value()
        params.encirclement = self.encirclement_check.isChecked()
        params.entrenchment = self.entrenchment_spin.value()
        params.planning_bonus = self.planning_spin.value() / 100.0


class BattleWindow(QMainWindow):
    def __init__(self, theme_manager=None):
        super().__init__()
        self.setWindowTitle("Simulateur de bataille HOI4")
        self.resize(1280, 820)
        self.theme_manager = theme_manager
        self.store = DivisionStore()
        self.battle = Battle(BattleParams())

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        # ------------------------------------------------ barre supérieure
        top = QHBoxLayout()
        new_btn = QPushButton("Nouvelle bataille")
        new_btn.clicked.connect(self.new_battle)
        top.addWidget(new_btn)
        top.addStretch(1)
        self.round_label = QLabel("Tour : 0")
        top.addWidget(self.round_label)
        top.addStretch(1)
        theme_btn = QPushButton("Thème clair/sombre")
        theme_btn.clicked.connect(self._toggle_theme)
        top.addWidget(theme_btn)
        root.addLayout(top)

        # -------------------------------------------------- corps principal
        splitter = QSplitter(Qt.Horizontal)
        root.addWidget(splitter, stretch=1)

        self.params_panel = ParamsPanel()
        splitter.addWidget(self.params_panel)

        self.attacker_panel = CampPanel("Attaquant", True, self.store)
        self.defender_panel = CampPanel("Défenseur", False, self.store)
        splitter.addWidget(self.attacker_panel)
        splitter.addWidget(self.defender_panel)
        splitter.setSizes([300, 460, 460])

        # ---------------------------------------------- barre de victoire
        balance_row = QHBoxLayout()
        balance_row.addWidget(QLabel("Défenseur"))
        self.balance_bar = QProgressBar()
        self.balance_bar.setRange(0, 100)
        self.balance_bar.setValue(50)
        self.balance_bar.setTextVisible(False)
        balance_row.addWidget(self.balance_bar, stretch=1)
        balance_row.addWidget(QLabel("Attaquant"))
        root.addLayout(balance_row)

        # ------------------------------------------------------- contrôles
        controls = QHBoxLayout()
        run1_btn = QPushButton("Lancer 1 tour")
        run1_btn.clicked.connect(lambda: self.run_turns(1))
        controls.addWidget(run1_btn)
        self.n_spin = QSpinBox()
        self.n_spin.setRange(1, 1000)
        self.n_spin.setValue(12)
        controls.addWidget(self.n_spin)
        runn_btn = QPushButton("Lancer N tours")
        runn_btn.clicked.connect(lambda: self.run_turns(self.n_spin.value()))
        controls.addWidget(runn_btn)
        self.detail_check = QCheckBox("Log détaillé de chaque tour")
        self.detail_check.setChecked(True)
        controls.addWidget(self.detail_check)
        controls.addStretch(1)
        root.addLayout(controls)

        # -------------------------------------------------------------- log
        self.log_view = QPlainTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setMaximumBlockCount(20000)
        root.addWidget(self.log_view, stretch=1)

        self._bind_battle()

    # ----------------------------------------------------------- bataille

    def _bind_battle(self) -> None:
        self.attacker_panel.battle = self.battle
        self.defender_panel.battle = self.battle
        self.attacker_panel.refresh_divisions()
        self.defender_panel.refresh_divisions()
        self._refresh_status()

    def new_battle(self) -> None:
        self.battle = Battle(BattleParams())
        self.params_panel.apply_to(self.battle.params)
        self.log_view.clear()
        self.log_view.appendPlainText("=== Nouvelle bataille ===")
        self._bind_battle()

    def run_turns(self, n: int) -> None:
        if not self.battle.attacker.divisions or not self.battle.defender.divisions:
            QMessageBox.information(self, "Camps incomplets",
                                    "Ajoutez au moins une division dans chaque camp.")
            return
        if self.battle.is_over:
            QMessageBox.information(self, "Bataille terminée",
                                    "La bataille est terminée — lancez une nouvelle bataille.")
            return
        # Les paramètres et leaders sont relus à chaque tour : on synchronise.
        self.params_panel.apply_to(self.battle.params)
        self.attacker_panel.sync_leader()
        self.defender_panel.sync_leader()

        logs = self.battle.run_rounds(n)
        detailed = self.detail_check.isChecked()
        for log in logs:
            if detailed:
                self._print_round(log)
        if not detailed and logs:
            self._print_summary(logs)
        self._refresh_status()

    def _print_round(self, log) -> None:
        self.log_view.appendPlainText(f"— Tour {log.round} —")
        for event in log.events:
            self.log_view.appendPlainText(f"  • {event}")
        for attack in log.attacks:
            self.log_view.appendPlainText(f"  {attack.summary()}")

    def _print_summary(self, logs) -> None:
        first, last = logs[0].round, logs[-1].round
        hp_a = sum(l.total_damage('attacker')[0] for l in logs)
        org_a = sum(l.total_damage('attacker')[1] for l in logs)
        hp_d = sum(l.total_damage('defender')[0] for l in logs)
        org_d = sum(l.total_damage('defender')[1] for l in logs)
        self.log_view.appendPlainText(
            f"=== Tours {first} à {last} (résumé) ===\n"
            f"  Attaquant : PV infligés {hp_a:.1f}, ORG infligée {org_a:.1f}\n"
            f"  Défenseur : PV infligés {hp_d:.1f}, ORG infligée {org_d:.1f}")
        for log in logs:
            for event in log.events:
                self.log_view.appendPlainText(f"  • [T{log.round}] {event}")

    def _refresh_status(self) -> None:
        self.round_label.setText(f"Tour : {self.battle.round}")
        self.balance_bar.setValue(round(self.battle.victory_balance() * 100))
        self.attacker_panel.refresh_divisions()
        self.defender_panel.refresh_divisions()
        if self.battle.is_over:
            winner = "ATTAQUANT" if self.battle.result == "attacker" else "DÉFENSEUR"
            report = self.battle.casualty_report()
            self.log_view.appendPlainText(
                f"\n=== FIN DE BATAILLE — victoire du camp {winner} ===")
            for side, label in (("attacker", "Attaquant"), ("defender", "Défenseur")):
                r = report[side]
                self.log_view.appendPlainText(
                    f"  {label} : PV perdus {r['pv_perdus']}, pertes estimées "
                    f"{r['pertes_estimees']} (×70 %), détruites {r['divisions_detruites']}, "
                    f"repliées {r['divisions_repliees']}")

    def _toggle_theme(self) -> None:
        if self.theme_manager is not None:
            self.theme_manager.toggle()
