"""Fenêtre principale de bataille (CDC §10.1)."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QDoubleSpinBox, QFormLayout, QGroupBox, QHBoxLayout,
    QInputDialog, QLabel, QListWidget, QListWidgetItem, QMainWindow,
    QMessageBox, QPlainTextEdit, QProgressBar, QPushButton, QSpinBox,
    QSplitter, QVBoxLayout, QWidget,
)

from engine.battle import Battle
from engine.gamedata import TERRAINS, WEATHER
from engine.leader import Leader
from engine.params import BattleParams
from engine.tactics import PHASE_LABELS, TacticRegistry
from gui.leader_editor import LeaderEditor
from gui.tactic_editor import TacticEditor
from persistence.divisions import DivisionStore
from persistence.leaders import LeaderStore


class CampPanel(QGroupBox):
    """Panneau d'un camp : divisions engagées, leader, tactique."""

    def __init__(self, title: str, is_attacker: bool, store: DivisionStore,
                 leader_store: LeaderStore, registry: TacticRegistry,
                 log_callback, parent=None):
        super().__init__(title, parent)
        self.is_attacker = is_attacker
        self.store = store
        self.leader_store = leader_store
        self.registry = registry
        self.log_callback = log_callback

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

        div_btns = QHBoxLayout()
        remove_btn = QPushButton("Retirer la division")
        remove_btn.clicked.connect(self._on_remove)
        div_btns.addWidget(remove_btn)
        paradrop_btn = QPushButton("Parachutée (−30 %, 48 h)")
        paradrop_btn.clicked.connect(self._on_paradrop)
        div_btns.addWidget(paradrop_btn)
        layout.addLayout(div_btns)

        # Modificateurs manuels du camp (§9.5), repliés par défaut
        self.mods_box = QGroupBox("Modificateurs du camp (§9.5)")
        self.mods_box.setCheckable(True)
        self.mods_box.setChecked(False)
        mods_form = QFormLayout(self.mods_box)

        def pct(minimum, maximum, suffix=" %"):
            s = QDoubleSpinBox()
            s.setRange(minimum, maximum)
            s.setSuffix(suffix)
            return s

        self.coordination_spin = pct(0, 100)
        mods_form.addRow("Coordination (radio/RADAR)", self.coordination_spin)
        self.supply_spin = pct(0, 100)
        mods_form.addRow("Pénurie de ravitaillement", self.supply_spin)
        self.enemy_air_spin = pct(0, 35)
        mods_form.addRow("Sup. aérienne ennemie subie", self.enemy_air_spin)
        self.air_support_spin = pct(0, 100)
        mods_form.addRow("Soutien aérien", self.air_support_spin)
        self.nation_atk_spin = pct(-100, 100)
        mods_form.addRow("Bonus de nation (attaque)", self.nation_atk_spin)
        self.nation_def_spin = pct(-100, 100)
        mods_form.addRow("Bonus de nation (défense)", self.nation_def_spin)
        self.intel_spin = pct(0, 15)
        mods_form.addRow("Avantage de renseignement", self.intel_spin)
        self.night_bonus_spin = pct(0, 100)
        mods_form.addRow("Bonus d'attaque de nuit", self.night_bonus_spin)
        self.artillery_spin = pct(0, 100)
        mods_form.addRow("Ratio d'artillerie (override)", self.artillery_spin)
        self.japan_check = QCheckBox("Japon (Banzai Charge)")
        mods_form.addRow(self.japan_check)
        self.masterful_check = QCheckBox("Blitz magistral débloqué")
        mods_form.addRow(self.masterful_check)
        self.flame_check = QCheckBox("Chars lance-flammes (urbain)")
        mods_form.addRow(self.flame_check)
        self.engineers_check = QCheckBox("Génie présent (Mouse Holing)")
        mods_form.addRow(self.engineers_check)
        self.mods_box.toggled.connect(self._on_mods_toggled)
        layout.addWidget(self.mods_box)
        self._on_mods_toggled(False)

        # Leader + tactique
        bottom = QFormLayout()
        self.leader_combo = QComboBox()
        bottom.addRow("Leader", self.leader_combo)
        self.ability_btn = QPushButton("Activer une capacité…")
        self.ability_btn.clicked.connect(self._on_ability)
        bottom.addRow(self.ability_btn)
        self.tactic_combo = QComboBox()
        bottom.addRow("Tactique (§9.3)", self.tactic_combo)
        self.tactic_label = QLabel("—")
        bottom.addRow("Tactique active", self.tactic_label)
        layout.addLayout(bottom)

        self.battle: Battle | None = None
        self.refresh_templates()
        self.refresh_leaders()

    @property
    def camp(self):
        if self.battle is None:
            return None
        return self.battle.attacker if self.is_attacker else self.battle.defender

    @property
    def side(self) -> str:
        return "attacker" if self.is_attacker else "defender"

    # -------------------------------------------------------------- listes

    def refresh_templates(self) -> None:
        current = self.template_combo.currentText()
        self.template_combo.clear()
        for template in self.store.list_templates():
            label = f"{template.folder}/{template.name}" if template.folder else template.name
            self.template_combo.addItem(label, template)
        index = self.template_combo.findText(current)
        if index >= 0:
            self.template_combo.setCurrentIndex(index)

    def refresh_leaders(self) -> None:
        current = self.leader_combo.currentText()
        self.leader_combo.clear()
        self.leader_combo.addItem("— Sans leader —", None)
        for leader in self.leader_store.list_leaders():
            self.leader_combo.addItem(
                f"{leader.name} (A{leader.attack_level}/D{leader.defense_level})", leader)
        index = self.leader_combo.findText(current)
        if index >= 0:
            self.leader_combo.setCurrentIndex(index)

    def refresh_tactic_combo(self) -> None:
        """Liste des tactiques forçables pour la phase en cours."""
        if self.battle is None:
            return
        current = self.tactic_combo.currentData()
        self.tactic_combo.blockSignals(True)
        self.tactic_combo.clear()
        self.tactic_combo.addItem("— Automatique (fidèle au jeu) —", None)
        for tactic in sorted(self.registry.for_side_phase(self.side, self.battle.battle_phase),
                             key=lambda t: t.name):
            self.tactic_combo.addItem(tactic.name, tactic.name)
        index = self.tactic_combo.findData(current)
        self.tactic_combo.setCurrentIndex(max(index, 0))
        self.tactic_combo.blockSignals(False)

    def sync_to_battle(self) -> None:
        """Reporte leader, override de tactique et curseurs §9.5 sur le camp."""
        if self.camp is None:
            return
        leader = self.leader_combo.currentData()
        self.camp.leader = leader if leader is not None else Leader()
        self.camp.manual_tactic = self.tactic_combo.currentData()
        sp = (self.battle.params.attacker if self.is_attacker
              else self.battle.params.defender)
        sp.coordination = self.coordination_spin.value() / 100.0
        sp.supply_shortage = self.supply_spin.value() / 100.0
        sp.enemy_air_superiority = self.enemy_air_spin.value() / 100.0
        sp.air_support_bonus = self.air_support_spin.value() / 100.0
        sp.nation_attack_bonus = self.nation_atk_spin.value() / 100.0
        sp.nation_defense_bonus = self.nation_def_spin.value() / 100.0
        sp.intel_advantage = self.intel_spin.value() / 100.0
        sp.night_attack_bonus = self.night_bonus_spin.value() / 100.0
        sp.artillery_ratio = self.artillery_spin.value() / 100.0
        sp.is_japan = self.japan_check.isChecked()
        sp.masterful_blitz = self.masterful_check.isChecked()
        sp.has_flame_tanks = self.flame_check.isChecked()
        sp.has_engineers = self.engineers_check.isChecked()

    def _on_mods_toggled(self, visible: bool) -> None:
        for widget in self.mods_box.findChildren(QWidget):
            widget.setVisible(visible)

    def _on_paradrop(self) -> None:
        row = self.division_list.currentRow()
        if self.camp is None or row < 0:
            return
        division = self.division_list.item(row).data(Qt.UserRole)
        division.paradropped_rounds_left = 48
        self.log_callback(f"  • {self.camp.label} : {division.name} marquée "
                          f"parachutée (−30 % pendant 48 tours).")

    # -------------------------------------------------------------- slots

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

    def _on_ability(self) -> None:
        if self.camp is None:
            return
        self.sync_to_battle()
        leader = self.camp.leader
        available = [a for a in leader.abilities
                     if self.camp.ability_uses.get(a.name, 0) < a.uses_per_battle]
        if not available:
            QMessageBox.information(self, "Aucune capacité",
                                    "Ce leader n'a plus de capacité disponible.")
            return
        names = [a.name for a in available]
        name, ok = QInputDialog.getItem(self, "Activer une capacité",
                                        "Capacité :", names, 0, False)
        if not ok:
            return
        ability = next(a for a in available if a.name == name)
        events: list[str] = []
        if self.camp.activate_ability(ability, events):
            for event in events:
                self.log_callback(f"  • {event}")

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

    def refresh_tactic_label(self) -> None:
        if self.battle is None:
            return
        tactic = self.battle.active_tactics.get(self.side)
        self.tactic_label.setText(tactic.describe() if tactic else "—")


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

        self.vp_spin = QSpinBox()
        self.vp_spin.setRange(0, 50)
        form.addRow("Points de victoire (urbain)", self.vp_spin)

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
        params.victory_points = self.vp_spin.value()


class BattleWindow(QMainWindow):
    def __init__(self, theme_manager=None):
        super().__init__()
        self.setWindowTitle("Simulateur de bataille HOI4")
        self.resize(1360, 860)
        self.theme_manager = theme_manager
        self.store = DivisionStore()
        self.leader_store = LeaderStore()
        self.registry = TacticRegistry()
        self.battle = Battle(BattleParams(), tactic_registry=self.registry)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        # ------------------------------------------------ barre supérieure
        top = QHBoxLayout()
        new_btn = QPushButton("Nouvelle bataille")
        new_btn.clicked.connect(self.new_battle)
        top.addWidget(new_btn)
        divisions_btn = QPushButton("Éditeur de divisions…")
        divisions_btn.clicked.connect(self._open_division_editor)
        top.addWidget(divisions_btn)
        leaders_btn = QPushButton("Éditeur de leaders…")
        leaders_btn.clicked.connect(self._open_leader_editor)
        top.addWidget(leaders_btn)
        tactics_btn = QPushButton("Éditeur de tactiques…")
        tactics_btn.clicked.connect(self._open_tactic_editor)
        top.addWidget(tactics_btn)
        top.addStretch(1)
        self.round_label = QLabel("Tour : 0")
        top.addWidget(self.round_label)
        self.phase_label = QLabel("Phase : Défaut")
        top.addWidget(self.phase_label)
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

        self.attacker_panel = CampPanel("Attaquant", True, self.store,
                                        self.leader_store, self.registry,
                                        self._append_log)
        self.defender_panel = CampPanel("Défenseur", False, self.store,
                                        self.leader_store, self.registry,
                                        self._append_log)
        splitter.addWidget(self.attacker_panel)
        splitter.addWidget(self.defender_panel)
        splitter.setSizes([300, 500, 500])

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

    def _append_log(self, text: str) -> None:
        self.log_view.appendPlainText(text)

    def _bind_battle(self) -> None:
        for panel in (self.attacker_panel, self.defender_panel):
            panel.battle = self.battle
            panel.refresh_divisions()
            panel.refresh_tactic_combo()
            panel.refresh_tactic_label()
        self._refresh_status()

    def new_battle(self) -> None:
        self.battle = Battle(BattleParams(), tactic_registry=self.registry)
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
        # Les paramètres, leaders et overrides sont relus à chaque tour.
        self.params_panel.apply_to(self.battle.params)
        self.attacker_panel.sync_to_battle()
        self.defender_panel.sync_to_battle()

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
        self.phase_label.setText(
            f"Phase : {PHASE_LABELS.get(self.battle.battle_phase, self.battle.battle_phase)}")
        self.balance_bar.setValue(round(self.battle.victory_balance() * 100))
        for panel in (self.attacker_panel, self.defender_panel):
            panel.refresh_divisions()
            panel.refresh_tactic_combo()
            panel.refresh_tactic_label()
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

    # ------------------------------------------------------------ éditeurs

    def _open_division_editor(self) -> None:
        from gui.division_editor import DivisionEditor
        editor = DivisionEditor(self.store, parent=self)
        editor.exec()
        self.attacker_panel.refresh_templates()
        self.defender_panel.refresh_templates()

    def _open_leader_editor(self) -> None:
        editor = LeaderEditor(self.leader_store, self.registry, parent=self)
        editor.exec()
        self.attacker_panel.refresh_leaders()
        self.defender_panel.refresh_leaders()

    def _open_tactic_editor(self) -> None:
        editor = TacticEditor(self.registry, parent=self)
        editor.exec()
        self.attacker_panel.refresh_tactic_combo()
        self.defender_panel.refresh_tactic_combo()

    def _toggle_theme(self) -> None:
        if self.theme_manager is not None:
            self.theme_manager.toggle()
