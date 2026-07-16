"""Orchestration d'une bataille : camps, ligne de front, réserves, tours."""
from __future__ import annotations

from engine import combat
from engine.division import Division
from engine.gamedata import WEATHER, WEATHER_TRANSITIONS
from engine.leader import Leader, LeaderAbility
from engine.logs import AttackReport, RoundLog
from engine.params import BattleParams
from engine.rng import CombatRNG
from engine.settings import SETTINGS
from engine.tactics import ActiveTactic, TacticManager, TacticRegistry

FORT_INTEGRITY_PER_LEVEL = 500.0   # jauge d'intégrité d'un niveau de fort (§8.6)
NAVAL_INVASION_DECAY_ROUNDS = 24   # extra optionnel (§7.2) : durée assumée de résorption (1 jour)
MAX_OVERWIDTH_RATIO = 1.33     # entrée en ligne refusée au-delà (§8.1)
MAX_WIDTH_PENALTY = -33.0      # plafond de pénalité de dépassement
STACKING_BASE_LIMIT = 5
STACKING_PER_DIRECTION = 3
STACKING_PENALTY_PER_DIV = -2.0
# Cycle jour/nuit : 12 h de jour, 12 h de nuit (wiki + CDC §7.3).
# La nuit court de DAY_END (18 h) à DAY_START (6 h).
DAY_START_HOUR = 6
DAY_END_HOUR = 18


class Camp:
    """Un des deux camps de la bataille."""

    def __init__(self, is_attacker: bool, leader: Leader | None = None):
        self.is_attacker = is_attacker
        self.leader = leader or Leader()
        self.divisions: list[Division] = []
        self.frontline: list[Division] = []
        self.reserves: list[Division] = []
        self.retreated: list[Division] = []
        self.destroyed: list[Division] = []
        self.width_penalty = 0.0      # % ≤ 0
        self.stacking_penalty = 0.0   # % ≤ 0
        self.manual_tactic: str | None = None   # override joueur (§9.3)
        # Capacités de leader activées : [(capacité, tours restants), …]
        self.active_abilities: list[list] = []
        self.ability_uses: dict[str, int] = {}

    @property
    def side(self) -> str:
        return "attacker" if self.is_attacker else "defender"

    @property
    def label(self) -> str:
        return "Attaquant" if self.is_attacker else "Défenseur"

    def add_division(self, division: Division) -> None:
        self.divisions.append(division)

    @property
    def active_divisions(self) -> list[Division]:
        return [d for d in self.divisions if d.can_fight]

    @property
    def frontline_width(self) -> float:
        return sum(d.stats.width for d in self.frontline)

    @property
    def total_recon(self) -> float:
        """Meilleure valeur de reconnaissance du camp (réserves incluses, §9.2)."""
        return max((d.recon for d in self.active_divisions), default=0.0)

    # ------------------------------------------------------ ligne de front

    def battle_width(self, battle: "Battle") -> float:
        return battle.effective_combat_width

    # ------------------------------------------------------- capacités

    def activate_ability(self, ability: LeaderAbility, events: list[str]) -> bool:
        """Active une capacité de maréchal (§5) si des usages restent."""
        used = self.ability_uses.get(ability.name, 0)
        if used >= ability.uses_per_battle:
            return False
        self.ability_uses[ability.name] = used + 1
        if ability.attack_bonus or ability.defense_bonus:
            self.active_abilities.append([ability, ability.duration_rounds])
        if ability.org_restore:
            for division in self.active_divisions:
                division.current_org = min(
                    division.current_org + ability.org_restore,
                    division.stats.organisation)
        events.append(f"{self.label} : capacité « {ability.name} » activée.")
        return True

    def tick_abilities(self) -> None:
        for entry in list(self.active_abilities):
            entry[1] -= 1
            if entry[1] <= 0:
                self.active_abilities.remove(entry)

    def deploy(self, battle: "Battle", events: list[str]) -> None:
        """Place en ligne les divisions qui rentrent, le reste en réserve."""
        width_limit = MAX_OVERWIDTH_RATIO * self.battle_width(battle)
        for division in self.divisions:
            if division in self.frontline or division in self.reserves:
                continue
            if not division.can_fight:
                continue
            if self.frontline_width + division.stats.width <= width_limit or not self.frontline:
                self.frontline.append(division)
                division.in_frontline = True
                events.append(f"{self.label} : {division.name} rejoint la ligne de front.")
            else:
                self.reserves.append(division)
                events.append(f"{self.label} : {division.name} placée en réserve.")

    def try_reinforce(self, battle: "Battle", rng: CombatRNG, events: list[str]) -> None:
        """Chaque division en réserve a 2 %/tour de rejoindre le front (§8.2)."""
        width_limit = MAX_OVERWIDTH_RATIO * self.battle_width(battle)
        for division in list(self.reserves):
            if not division.can_fight:
                continue
            fits = self.frontline_width + division.stats.width <= width_limit
            if (rng.chance(SETTINGS.reinforce_chance) and fits) or not self.frontline:
                self.reserves.remove(division)
                self.frontline.append(division)
                division.in_frontline = True
                events.append(f"{self.label} : {division.name} renforce la ligne de front.")

    def compute_penalties(self, battle: "Battle") -> None:
        """Pénalités de dépassement de largeur et d'empilement (§8.1)."""
        width = self.battle_width(battle)
        total = self.frontline_width
        if width > 0 and total > width:
            self.width_penalty = max(-100.0 * (total - width) / width, MAX_WIDTH_PENALTY)
        else:
            self.width_penalty = 0.0

        limit = STACKING_BASE_LIMIT + STACKING_PER_DIRECTION * battle.params.extra_directions
        excess = len(self.frontline) - limit
        self.stacking_penalty = STACKING_PENALTY_PER_DIV * excess if excess > 0 else 0.0

    def force_to_reserve(self, division: Division) -> bool:
        """Retire manuellement une division du front vers la réserve
        (décision du joueur, indépendamment de son état) — clic droit
        « Mettre en réserve » dans la fenêtre de bataille."""
        if division not in self.frontline:
            return False
        self.frontline.remove(division)
        self.reserves.append(division)
        division.in_frontline = False
        return True

    def cleanup(self, events: list[str]) -> None:
        """Retire les divisions détruites ou en déroute en fin de tour."""
        for division in list(self.frontline):
            if division.is_destroyed:
                self.frontline.remove(division)
                self.destroyed.append(division)
                events.append(f"{self.label} : {division.name} est DÉTRUITE.")
            elif division.is_broken:
                self.frontline.remove(division)
                self.retreated.append(division)
                events.append(f"{self.label} : {division.name} se replie (organisation épuisée).")
        for division in list(self.reserves):
            if division.is_destroyed:
                self.reserves.remove(division)
                self.destroyed.append(division)

    # ---------------------------------------------------------- rapports

    def hp_pool(self) -> tuple[float, float]:
        """PV courants/max de TOUTE la composition (y compris repliées et
        détruites) — utilisé pour le rapport de pertes de fin de bataille."""
        cur = sum(d.current_hp for d in self.divisions)
        tot = sum(d.stats.hp for d in self.divisions)
        return cur, tot

    def active_hp_pool(self) -> tuple[float, float]:
        """PV courants des divisions encore actives (front + réserve)
        rapportés au total de la composition — pour la barre d'équilibre.
        Une division repliée ne compte plus, même si elle a encore des PV :
        elle ne participe plus au combat."""
        active = self.frontline + self.reserves
        cur = sum(d.current_hp for d in active)
        tot = sum(d.stats.hp for d in self.divisions)
        return cur, tot

    def org_pool(self) -> tuple[float, float]:
        active = self.frontline + self.reserves
        cur = sum(d.current_org for d in active)
        tot = sum(d.stats.organisation for d in self.divisions)
        return cur, tot


class Battle:
    """Une bataille : deux camps, des paramètres, un déroulé tour par tour."""

    def __init__(self, params: BattleParams | None = None,
                 attacker_leader: Leader | None = None,
                 defender_leader: Leader | None = None,
                 seed: int | None = None,
                 tactic_registry: TacticRegistry | None = None,
                 use_tactics: bool = True):
        self.params = params or BattleParams()
        self.rng = CombatRNG(seed)
        self.attacker = Camp(True, attacker_leader)
        self.defender = Camp(False, defender_leader)
        self.round = 0
        self.logs: list[RoundLog] = []
        self.result: str | None = None   # None | "attacker" | "defender"
        self.active_tactics: dict[str, ActiveTactic | None] = {"attacker": None, "defender": None}
        self.battle_phase = "default"
        self.tactic_manager = TacticManager(tactic_registry) if use_tactics else None
        # Jauge d'intégrité du niveau de fort courant (§8.6)
        self.fort_integrity = FORT_INTEGRITY_PER_LEVEL
        self._pending_events: list[str] = []
        # Extra optionnel (§7.2) : tours écoulés depuis le début du
        # débarquement, pour la pénalité progressive −80 % → 0 %.
        self.naval_invasion_round = 0

    def environment_snapshot(self) -> str:
        """Résumé complet de l'état de la bataille pour le mode de log
        « Tout afficher » : terrain, météo, cycle jour/nuit, fortifications,
        encerclement, retranchement, débarquement amphibie — y compris les
        paramètres statiques qui ne génèrent pas d'événement discret."""
        p = self.params
        parts = [f"Terrain : {p.terrain.nom}", f"Météo : {p.weather.nom}"]
        if p.temperature_id != "normal":
            parts.append(f"Température : {p.temperature.nom}")
        if SETTINGS.day_night_cycle_enabled:
            parts.append(f"Heure : {self.current_hour} h "
                         f"({'Nuit' if p.is_night else 'Jour'})")
        else:
            parts.append(f"Nuit : {'Oui' if p.is_night else 'Non'}")
        if p.large_river:
            parts.append("Grande rivière")
        elif p.small_river:
            parts.append("Petite rivière")
        if p.fort_level > 0:
            parts.append(f"Fort : niveau {p.fort_level} "
                         f"(intégrité {self.fort_integrity:.0f}/{FORT_INTEGRITY_PER_LEVEL:.0f})")
        if p.encirclement:
            parts.append("Défenseur encerclé")
        if p.entrenchment:
            parts.append(f"Retranchement : {p.entrenchment}")
        if p.naval_invasion:
            if p.naval_invasion_advanced:
                parts.append(f"Débarquement amphibie : progressif "
                            f"({self.naval_invasion_factor:+.1f} %, tour "
                            f"{min(self.naval_invasion_round, NAVAL_INVASION_DECAY_ROUNDS)}/"
                            f"{NAVAL_INVASION_DECAY_ROUNDS})")
            else:
                parts.append("Débarquement amphibie : actif (−50 % fixe)")
        return " | ".join(parts)

    @property
    def naval_invasion_factor(self) -> float:
        """Facteur multiplicatif du débarquement amphibie progressif
        (extra optionnel §7.2). Démarre à −80 % et se résorbe linéairement
        sur ``NAVAL_INVASION_DECAY_ROUNDS`` tours (durée assumée, non
        spécifiée par le CDC), jusqu'à un effet nul."""
        progress = min(self.naval_invasion_round / NAVAL_INVASION_DECAY_ROUNDS, 1.0)
        return -80.0 * (1.0 - progress)

    def apply_fort_damage(self, amount: float) -> None:
        """Érosion progressive du fort par dégâts collatéraux (§8.6)."""
        if self.params.fort_level <= 0:
            return
        self.fort_integrity -= amount
        while self.fort_integrity <= 0 and self.params.fort_level > 0:
            self.params.fort_level -= 1
            self.fort_integrity += FORT_INTEGRITY_PER_LEVEL
            self._pending_events.append(
                f"Les fortifications cèdent : niveau de fort réduit à {self.params.fort_level}.")
        if self.params.fort_level <= 0:
            self.fort_integrity = 0.0

    @property
    def effective_combat_width(self) -> float:
        """Largeur de combat de base modifiée par les tactiques actives (§9.1)."""
        width = self.params.base_combat_width
        for tactic in self.active_tactics.values():
            if tactic is not None:
                width *= tactic.effective_width_factor
        return width

    # ------------------------------------------------------------ camps

    def camp(self, side: str) -> Camp:
        return self.attacker if side == "attacker" else self.defender

    def enemy_of(self, camp: Camp) -> Camp:
        return self.defender if camp.is_attacker else self.attacker

    def damage_factor_for(self, camp: Camp) -> tuple[float, str]:
        """Facteur de dégâts des tactiques actives pour le camp qui frappe.

        Les deux tactiques actives (attaquant ET défenseur) modifient chacune
        les dégâts des deux camps (§9.5 : colonnes « Dégâts ATK/DEF »).
        """
        factor = 1.0
        names = []
        for side in ("attacker", "defender"):
            tactic = self.active_tactics.get(side)
            if tactic is None:
                continue
            f = tactic.damage_factor_for(camp.side)
            if f != 1.0:
                factor *= f
            names.append(tactic.name)
        return factor, " / ".join(names)

    # ------------------------------------------------------------- tours

    @property
    def is_over(self) -> bool:
        return self.result is not None

    # ------------------------------------------------ environnement dynamique

    @property
    def current_hour(self) -> int:
        """Heure de jeu (0-23) du tour courant, dérivée de l'heure de départ."""
        elapsed = max(self.round - 1, 0)
        return (SETTINGS.battle_start_hour + elapsed) % 24

    @staticmethod
    def _is_night_at(hour: int) -> bool:
        """Nuit de 18 h à 6 h (12 h de jour, 12 h de nuit)."""
        return not (DAY_START_HOUR <= hour < DAY_END_HOUR)

    def _roll_weather(self) -> str:
        """Tire la météo suivante selon la table de transitions pondérée."""
        weights = WEATHER_TRANSITIONS.get(self.params.weather_id)
        if not weights:
            return self.params.weather_id
        options = [w for w in weights if w in WEATHER]
        if not options:
            return self.params.weather_id
        return self.rng.weighted_choice(options, [weights[w] for w in options])

    def _advance_environment(self, log: RoundLog) -> None:
        # Cycle jour/nuit : recalcule is_night depuis l'heure courante.
        if SETTINGS.day_night_cycle_enabled:
            night = self._is_night_at(self.current_hour)
            if night != self.params.is_night:
                self.params.is_night = night
                if night:
                    log.events.append(f"La nuit tombe ({self.current_hour} h) — "
                                      f"−50 % à l'attaque des deux camps.")
                else:
                    log.events.append(f"Le jour se lève ({self.current_hour} h).")

        # Météo dynamique : re-tirage à chaque période (après le tour 1).
        if SETTINGS.dynamic_weather_enabled:
            period = max(1, SETTINGS.weather_change_period)
            if self.round > 1 and (self.round - 1) % period == 0:
                new_weather = self._roll_weather()
                if new_weather != self.params.weather_id:
                    log.events.append(
                        f"La météo change : {self.params.weather.nom} → "
                        f"{WEATHER[new_weather].nom}.")
                    self.params.weather_id = new_weather

    def run_round(self) -> RoundLog:
        """Exécute un tour de combat (1 heure de jeu)."""
        if self.is_over:
            return RoundLog(round=self.round, events=["La bataille est terminée."])

        self.round += 1
        log = RoundLog(round=self.round, phase=self.battle_phase)

        # Environnement dynamique : cycle jour/nuit et météo évolutive
        self._advance_environment(log)

        # Débarquement amphibie progressif (extra optionnel §7.2)
        if self.params.naval_invasion and self.params.naval_invasion_advanced:
            self.naval_invasion_round += 1

        # 1. Re-sélection des tactiques toutes les 12 h (jalon 2)
        if self.tactic_manager is not None:
            self.tactic_manager.maybe_reselect(self, log)

        # 2. Déploiement initial + renforts depuis la réserve
        for camp in (self.attacker, self.defender):
            if self.round == 1:
                camp.deploy(self, log.events)
            else:
                camp.deploy(self, log.events)   # nouvelles divisions ajoutées en cours de bataille
                camp.try_reinforce(self, self.rng, log.events)
            camp.compute_penalties(self)

        # 3. Pools de défense du tour
        for camp in (self.attacker, self.defender):
            for division in camp.frontline:
                combat.compute_defense_pool(division, camp, self, self.rng)

        # 4. Ciblage
        for camp in (self.attacker, self.defender):
            enemy = self.enemy_of(camp)
            for division in camp.frontline:
                combat.build_target_list(division, enemy.frontline, self.rng)

        # 5. Résolution des attaques (attaquant puis défenseur ; les
        #    éliminations ne prennent effet qu'en fin de tour)
        for camp in (self.attacker, self.defender):
            for division in camp.frontline:
                log.attacks.extend(combat.resolve_attacks(division, camp, self, self.rng))

        # 6. Événements différés (érosion de fort…)
        if self._pending_events:
            log.events.extend(self._pending_events)
            self._pending_events.clear()

        # 7. Décompte parachutage/capacités, nettoyage, fin de bataille
        for camp in (self.attacker, self.defender):
            for division in camp.divisions:
                if division.paradropped_rounds_left > 0:
                    division.paradropped_rounds_left -= 1
            camp.tick_abilities()
            camp.cleanup(log.events)

        atk_t = self.active_tactics.get("attacker")
        def_t = self.active_tactics.get("defender")
        log.attacker_tactic = atk_t.name if atk_t else ""
        log.defender_tactic = def_t.name if def_t else ""
        log.environment = self.environment_snapshot()

        self._check_end(log)
        self.logs.append(log)
        return log

    def run_rounds(self, n: int, stop_on_end: bool = True) -> list[RoundLog]:
        results = []
        for _ in range(n):
            if stop_on_end and self.is_over:
                break
            results.append(self.run_round())
        return results

    def _check_end(self, log: RoundLog) -> None:
        defender_alive = self.defender.frontline or self.defender.reserves
        attacker_alive = self.attacker.frontline or self.attacker.reserves
        if not defender_alive:
            self.result = "attacker"
            log.events.append("VICTOIRE DE L'ATTAQUANT — le défenseur n'a plus de division en état de combattre.")
        elif not attacker_alive:
            self.result = "defender"
            log.events.append("VICTOIRE DU DÉFENSEUR — l'attaquant n'a plus de division en état de combattre.")

    # --------------------------------------------------------- indicateurs

    def victory_balance(self) -> float:
        """Équilibre des forces 0..1 (part de l'attaquant), basé sur
        l'organisation et les PV restants des deux camps."""
        def score(camp: Camp) -> float:
            org_cur, org_tot = camp.org_pool()
            hp_cur, hp_tot = camp.active_hp_pool()
            org_part = org_cur / org_tot if org_tot else 0.0
            hp_part = hp_cur / hp_tot if hp_tot else 0.0
            return 0.7 * org_part + 0.3 * hp_part

        a, d = score(self.attacker), score(self.defender)
        return a / (a + d) if (a + d) > 0 else 0.5

    def casualty_report(self) -> dict:
        """Rapport de fin de bataille simplifié : PV perdus × 70 % (§8.7)."""
        report = {}
        for camp in (self.attacker, self.defender):
            hp_cur, hp_tot = camp.hp_pool()
            lost = hp_tot - hp_cur
            report[camp.side] = {
                "pv_perdus": round(lost, 2),
                "pertes_estimees": round(lost * 0.70, 2),
                "divisions_detruites": len(camp.destroyed),
                "divisions_repliees": len(camp.retreated),
            }
        return report
