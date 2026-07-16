"""Fenêtre principale de bataille (CDC §10.1)."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QDoubleSpinBox, QFileDialog, QFormLayout, QGroupBox,
    QHBoxLayout, QInputDialog, QLabel, QListWidget, QListWidgetItem,
    QMainWindow, QMenu, QMessageBox, QProgressBar, QPushButton, QSpinBox,
    QSplitter, QVBoxLayout, QWidget,
)

from engine.battle import Battle
from engine.gamedata import TEMPERATURE, TERRAINS, WEATHER
from engine.leader import Leader
from engine.params import BattleParams, SideParams
from engine.settings import SETTINGS
from engine.tactics import PHASE_LABELS, TacticRegistry
from gui.division_instance_editor import DivisionInstanceDialog
from gui.leader_editor import LeaderEditor
from gui.save_manager import SaveManager
from gui.settings_dialog import SettingsDialog
from gui.tactic_editor import TacticEditor
from persistence.battles import BattleSaveStore
from persistence.csv_export import export_battle_csv
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
        self.division_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.division_list.customContextMenuRequested.connect(self._on_division_context_menu)
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

    def load_from_battle(self) -> None:
        """Restaure les widgets depuis l'état du camp (chargement de sauvegarde)."""
        if self.camp is None:
            return
        sp = (self.battle.params.attacker if self.is_attacker
              else self.battle.params.defender)
        self.coordination_spin.setValue(sp.coordination * 100)
        self.supply_spin.setValue(sp.supply_shortage * 100)
        self.enemy_air_spin.setValue(sp.enemy_air_superiority * 100)
        self.air_support_spin.setValue(sp.air_support_bonus * 100)
        self.nation_atk_spin.setValue(sp.nation_attack_bonus * 100)
        self.nation_def_spin.setValue(sp.nation_defense_bonus * 100)
        self.intel_spin.setValue(sp.intel_advantage * 100)
        self.night_bonus_spin.setValue(sp.night_attack_bonus * 100)
        self.artillery_spin.setValue(sp.artillery_ratio * 100)
        self.japan_check.setChecked(sp.is_japan)
        self.masterful_check.setChecked(sp.masterful_blitz)
        self.flame_check.setChecked(sp.has_flame_tanks)
        self.engineers_check.setChecked(sp.has_engineers)
        # Leader chargé depuis la sauvegarde : proposé tel quel dans le combo
        leader = self.camp.leader
        if leader and leader.name != "Sans leader":
            label = f"{leader.name} (sauvegarde, A{leader.attack_level}/D{leader.defense_level})"
            self.leader_combo.insertItem(1, label, leader)
            self.leader_combo.setCurrentIndex(1)
        # Override de tactique
        self.refresh_tactic_combo()
        if self.camp.manual_tactic:
            idx = self.tactic_combo.findData(self.camp.manual_tactic)
            if idx >= 0:
                self.tactic_combo.setCurrentIndex(idx)

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

    # ------------------------------------------------------ menu contextuel

    def _on_division_context_menu(self, pos) -> None:
        item = self.division_list.itemAt(pos)
        if item is None or self.camp is None:
            return
        division = item.data(Qt.UserRole)

        menu = QMenu(self)
        rename_action = menu.addAction("Renommer…")
        stats_action = menu.addAction("Modifier les statistiques…")
        menu.addSeparator()
        reserve_action = menu.addAction("Mettre en réserve")
        reserve_action.setEnabled(division in self.camp.frontline)

        chosen = menu.exec(self.division_list.viewport().mapToGlobal(pos))
        if chosen is rename_action:
            self._rename_division(division)
        elif chosen is stats_action:
            self._edit_division_stats(division)
        elif chosen is reserve_action:
            self._force_division_to_reserve(division)

    def _rename_division(self, division) -> None:
        new_name, ok = QInputDialog.getText(self, "Renommer la division",
                                            "Nouveau nom :", text=division.name)
        if ok and new_name.strip():
            division.name = new_name.strip()
            self.refresh_divisions()

    def _edit_division_stats(self, division) -> None:
        dialog = DivisionInstanceDialog(division, parent=self)
        if dialog.exec():
            dialog.apply()
            self.refresh_divisions()

    def _force_division_to_reserve(self, division) -> None:
        if self.camp.force_to_reserve(division):
            self.log_callback(f"  • {self.camp.label} : {division.name} "
                              f"retirée manuellement en réserve.")
            self.refresh_divisions()

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

        self.temperature_combo = QComboBox()
        for tid, temperature in TEMPERATURE.items():
            self.temperature_combo.addItem(temperature.nom, tid)
        form.addRow("Température (extra, approximatif)", self.temperature_combo)

        self.night_check = QCheckBox("Nuit (−50 % attaque)")
        form.addRow(self.night_check)

        self.river_combo = QComboBox()
        self.river_combo.addItems(["Aucune rivière", "Petite rivière (−30 %)",
                                   "Grande rivière (−60 %)"])
        form.addRow("Rivière", self.river_combo)

        self.naval_check = QCheckBox("Débarquement amphibie (−50 %)")
        form.addRow(self.naval_check)
        self.naval_advanced_check = QCheckBox("Version progressive (−80 % → 0 % sur 24 tours, extra)")
        form.addRow(self.naval_advanced_check)

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

    def load_from(self, params: BattleParams) -> None:
        """Restaure les widgets depuis des paramètres (chargement)."""
        self.terrain_combo.setCurrentIndex(max(self.terrain_combo.findData(params.terrain_id), 0))
        self.weather_combo.setCurrentIndex(max(self.weather_combo.findData(params.weather_id), 0))
        self.temperature_combo.setCurrentIndex(
            max(self.temperature_combo.findData(params.temperature_id), 0))
        self.night_check.setChecked(params.is_night)
        self.river_combo.setCurrentIndex(2 if params.large_river
                                         else 1 if params.small_river else 0)
        self.naval_check.setChecked(params.naval_invasion)
        self.naval_advanced_check.setChecked(params.naval_invasion_advanced)
        self.fort_spin.setValue(params.fort_level)
        self.directions_spin.setValue(params.extra_directions)
        self.encirclement_check.setChecked(params.encirclement)
        self.entrenchment_spin.setValue(params.entrenchment)
        self.planning_spin.setValue(params.planning_bonus * 100)
        self.vp_spin.setValue(params.victory_points)

    def apply_to(self, params: BattleParams) -> None:
        params.terrain_id = self.terrain_combo.currentData()
        params.weather_id = self.weather_combo.currentData()
        params.temperature_id = self.temperature_combo.currentData()
        params.is_night = self.night_check.isChecked()
        params.small_river = self.river_combo.currentIndex() == 1
        params.large_river = self.river_combo.currentIndex() == 2
        params.naval_invasion = self.naval_check.isChecked()
        params.naval_invasion_advanced = self.naval_advanced_check.isChecked()
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
        self.battle_store = BattleSaveStore()
        self.battle = self._make_battle()

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
        saves_btn = QPushButton("Sauvegardes…")
        saves_btn.clicked.connect(self._open_save_manager)
        top.addWidget(saves_btn)
        settings_btn = QPushButton("Paramètres…")
        settings_btn.clicked.connect(self._open_settings)
        top.addWidget(settings_btn)
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
        controls.addWidget(QLabel("Logs :"))
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItem("Résumé", "summary")
        self.log_level_combo.addItem("Détaillé", "detailed")
        self.log_level_combo.addItem("Tout afficher", "full")
        self.log_level_combo.setCurrentIndex(1)   # « Détaillé » par défaut
        controls.addWidget(self.log_level_combo)
        csv_btn = QPushButton("Exporter les logs en CSV…")
        csv_btn.clicked.connect(self._export_csv)
        controls.addWidget(csv_btn)
        controls.addStretch(1)
        root.addLayout(controls)

        # ------------------------------------------------------------- log
        # Chaque ligne d'attaque porte un tooltip avec le détail complet
        # (attaques/défenses, dés, bonus appliqués) — CDC §11.
        self.log_view = QListWidget()
        self.log_view.setSelectionMode(QListWidget.NoSelection)
        self.log_view.setUniformItemSizes(True)
        root.addWidget(self.log_view, stretch=1)

        self._bind_battle()

    # ----------------------------------------------------------- bataille

    def _append_log(self, text: str, tooltip: str | None = None) -> None:
        item = QListWidgetItem(text)
        if tooltip:
            item.setToolTip(tooltip)
        self.log_view.addItem(item)
        if self.log_view.count() > 20000:
            self.log_view.takeItem(0)
        self.log_view.scrollToBottom()

    def _log_text(self) -> str:
        return "\n".join(self.log_view.item(i).text()
                         for i in range(self.log_view.count()))

    def _bind_battle(self) -> None:
        for panel in (self.attacker_panel, self.defender_panel):
            panel.battle = self.battle
            panel.refresh_divisions()
            panel.refresh_tactic_combo()
            panel.refresh_tactic_label()
        self._refresh_status()

    def _make_battle(self) -> Battle:
        """Crée une bataille en respectant la graine fixe. Le gestionnaire de
        tactiques est toujours instancié : l'activation/désactivation des
        tactiques est ensuite gérée en temps réel par le paramètre
        (SETTINGS.tactics_enabled), pour qu'un changement s'applique aussi à
        la bataille en cours."""
        seed = SETTINGS.fixed_seed if SETTINGS.use_fixed_seed else None
        return Battle(BattleParams(), tactic_registry=self.registry,
                      seed=seed, use_tactics=True)

    def new_battle(self) -> None:
        self.battle = self._make_battle()
        self.params_panel.apply_to(self.battle.params)
        self.log_view.clear()
        self._append_log("=== Nouvelle bataille ===")
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

        logs = self.battle.run_rounds(n, stop_on_end=SETTINGS.auto_stop_on_victory)
        level = self.log_level_combo.currentData()
        if level == "summary":
            if logs:
                self._print_summary(logs)
        else:
            for log in logs:
                self._print_round(log, full=(level == "full"))
        self._refresh_status()

    def _print_round(self, log, full: bool = False) -> None:
        self._append_log(f"— Tour {log.round} —")
        if full and log.environment:
            self._append_log(f"  ⚙ État : {log.environment}")
        for event in log.events:
            self._append_log(f"  • {event}")
        for attack in log.attacks:
            # Résumé en ligne, détail complet au survol (§11)
            self._append_log(f"  {attack.summary()}", tooltip=attack.details())

    def _print_summary(self, logs) -> None:
        first, last = logs[0].round, logs[-1].round
        hp_a = sum(l.total_damage('attacker')[0] for l in logs)
        org_a = sum(l.total_damage('attacker')[1] for l in logs)
        hp_d = sum(l.total_damage('defender')[0] for l in logs)
        org_d = sum(l.total_damage('defender')[1] for l in logs)
        self._append_log(f"=== Tours {first} à {last} (résumé) ===")
        self._append_log(f"  Attaquant : PV infligés {hp_a:.1f}, ORG infligée {org_a:.1f}")
        self._append_log(f"  Défenseur : PV infligés {hp_d:.1f}, ORG infligée {org_d:.1f}")
        for log in logs:
            for event in log.events:
                self._append_log(f"  • [T{log.round}] {event}")

    def _refresh_status(self) -> None:
        round_text = f"Tour : {self.battle.round}"
        if SETTINGS.day_night_cycle_enabled:
            hour = self.battle.current_hour
            round_text += f" — {hour} h ({'Nuit' if self.battle.params.is_night else 'Jour'})"
        if SETTINGS.dynamic_weather_enabled:
            round_text += f" — {self.battle.params.weather.nom}"
        self.round_label.setText(round_text)
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
            self._append_log(f"=== FIN DE BATAILLE — victoire du camp {winner} ===")
            for side, label in (("attacker", "Attaquant"), ("defender", "Défenseur")):
                r = report[side]
                self._append_log(
                    f"  {label} : PV perdus {r['pv_perdus']}, pertes estimées "
                    f"{r['pertes_estimees']} (×70 %), détruites {r['divisions_detruites']}, "
                    f"repliées {r['divisions_repliees']}")

    # ------------------------------------------------------------ éditeurs

    def _open_save_manager(self) -> None:
        manager = SaveManager(self.battle_store,
                              get_battle=lambda: self.battle,
                              get_log_text=self._log_text,
                              on_loaded=self._on_battle_loaded,
                              registry=self.registry,
                              parent=self)
        manager.exec()

    def _on_battle_loaded(self, battle: Battle, log_text: str) -> None:
        """Restaure une bataille chargée : moteur + widgets."""
        self.battle = battle
        self.log_view.clear()
        for line in log_text.splitlines():
            self._append_log(line)
        self._append_log("=== Bataille chargée ===")
        self.params_panel.load_from(battle.params)
        for panel in (self.attacker_panel, self.defender_panel):
            panel.battle = battle
            panel.load_from_battle()
        self._bind_battle()

    def _export_csv(self) -> None:
        if not self.battle.logs:
            QMessageBox.information(self, "Aucun log",
                                    "Lancez d'abord au moins un tour de combat.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exporter les logs en CSV", "logs_bataille.csv",
            "Fichiers CSV (*.csv)")
        if not path:
            return
        rows = export_battle_csv(self.battle, path)
        QMessageBox.information(self, "Export terminé",
                                f"{rows} lignes exportées vers :\n{path}")

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

    def _open_settings(self) -> None:
        SettingsDialog(parent=self).exec()

    def _toggle_theme(self) -> None:
        if self.theme_manager is not None:
            self.theme_manager.toggle()
