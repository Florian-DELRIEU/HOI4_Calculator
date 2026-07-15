"""Système de tactiques (CDC §9).

- Tactiques définies en JSON (``data/tactics.json`` + tactiques personnalisées),
  clé unique ``(nom, camp, phase)``.
- Re-sélection toutes les 12 heures par tirage pondéré, avec Initiative
  **déterministe** (§9.2) : comparaison des compétences des généraux,
  +5 niveaux pour le camp ayant l'avantage de reconnaissance, égalité en
  faveur du défenseur. Le perdant choisit en premier ; le gagnant reçoit
  +35 % de poids par point d'avantage sur les tactiques qui contrent le
  choix adverse.
- Override manuel possible par camp (§9.3).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from engine.gamedata import DATA_DIR

if TYPE_CHECKING:
    from engine.battle import Battle, Camp
    from engine.logs import RoundLog

RESELECT_INTERVAL = 12          # heures entre deux sélections (§9.1)
PREFERRED_TACTIC_BONUS = 1.5    # +50 % de poids (§5)
COUNTER_BONUS_PER_SKILL = 0.35  # +35 % par point d'avantage (§9.2)
RECON_SKILL_BONUS = 5           # bonus d'initiative si meilleure recon (§9.2)

PHASE_LABELS = {
    "default": "Défaut",
    "close_combat": "Combat rapproché",
    "tactical_withdrawal": "Repli tactique",
    "seize_bridge": "Prise de pont",
    "hold_bridge": "Défense de pont",
    "street_fighting": "Combat de rue",
}


@dataclass
class TacticDef:
    name: str
    side: str                       # "attacker" | "defender"
    phase: str = "default"
    weight: float = 4.0
    trigger: dict | None = None
    countered_by: list[str] = field(default_factory=list)
    attacker_damage: float = 0.0    # modifie les dégâts infligés par l'attaquant
    defender_damage: float = 0.0    # modifie les dégâts infligés par le défenseur
    width: float = 0.0              # modifie la largeur de combat de base
    movement: float = 0.0           # modifie la vitesse (affichage)
    begins_phase: str | None = None
    weight_rules: list[dict] = field(default_factory=list)
    custom: bool = False            # tactique personnalisée (éditeur)

    @property
    def key(self) -> tuple[str, str, str]:
        return (self.name, self.side, self.phase)

    def to_dict(self) -> dict:
        data = {
            "name": self.name, "side": self.side, "phase": self.phase,
            "weight": self.weight,
        }
        if self.trigger:
            data["trigger"] = self.trigger
        if self.countered_by:
            data["countered_by"] = self.countered_by
        for attr in ("attacker_damage", "defender_damage", "width", "movement"):
            if getattr(self, attr):
                data[attr] = getattr(self, attr)
        if self.begins_phase:
            data["begins_phase"] = self.begins_phase
        if self.weight_rules:
            data["weight_rules"] = self.weight_rules
        return data

    @classmethod
    def from_dict(cls, data: dict, custom: bool = False) -> "TacticDef":
        fields_ = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(custom=custom, **fields_)


@dataclass
class ActiveTactic:
    """Tactique active d'un camp pour les 12 prochaines heures."""

    tactic: TacticDef
    countered: bool = False
    forced: bool = False            # choisie manuellement par le joueur

    @property
    def name(self) -> str:
        return self.tactic.name

    def damage_factor_for(self, striker_side: str) -> float:
        """Facteur de dégâts appliqué aux coups du camp ``striker_side``."""
        if self.countered:
            return 1.0
        bonus = (self.tactic.attacker_damage if striker_side == "attacker"
                 else self.tactic.defender_damage)
        return 1.0 + bonus

    @property
    def effective_width_factor(self) -> float:
        return 1.0 if self.countered else 1.0 + self.tactic.width

    def describe(self) -> str:
        label = self.name
        if self.forced:
            label += " (forcée)"
        if self.countered:
            label += " [CONTRÉE]"
        return label


# ------------------------------------------------------------- déclencheurs

class TacticContext:
    """Contexte d'évaluation des déclencheurs pour un camp donné."""

    def __init__(self, camp: "Camp", battle: "Battle"):
        self.camp = camp
        self.battle = battle
        self.enemy = battle.enemy_of(camp)

    @property
    def skill(self) -> int:
        return self.camp.leader.skill

    @property
    def skill_advantage(self) -> int:
        return self.camp.leader.skill - self.enemy.leader.skill

    @property
    def side_params(self):
        return (self.battle.params.attacker if self.camp.is_attacker
                else self.battle.params.defender)

    @property
    def average_hardness(self) -> float:
        divisions = self.camp.frontline or self.camp.active_divisions
        if not divisions:
            return 0.0
        return sum(d.stats.hardness for d in divisions) / len(divisions)

    @property
    def artillery_ratio(self) -> float:
        computed = 0.0
        divisions = self.camp.active_divisions
        if divisions:
            ratios = [d.template.artillery_ratio() for d in divisions]
            computed = sum(ratios) / len(ratios)
        return max(computed, self.side_params.artillery_ratio)

    def has_flag(self, flag: str) -> bool:
        return bool(getattr(self.side_params, flag, False))


def eval_condition(cond: dict | None, ctx: TacticContext) -> bool:
    """Évalue un arbre de conditions JSON (déclencheurs de tactique)."""
    if not cond:
        return True
    for key, value in cond.items():
        if key == "all":
            if not all(eval_condition(c, ctx) for c in value):
                return False
        elif key == "any":
            if not any(eval_condition(c, ctx) for c in value):
                return False
        elif key == "not":
            if eval_condition(value, ctx):
                return False
        elif key == "skill_gt":
            if not ctx.skill > value:
                return False
        elif key == "skill_lt":
            if not ctx.skill < value:
                return False
        elif key == "skill_advantage_gt":
            if not ctx.skill_advantage > value:
                return False
        elif key == "trait":
            if not ctx.camp.leader.has_trait(value):
                return False
        elif key == "hardness_gt":
            if not ctx.average_hardness > value:
                return False
        elif key == "river":
            has_river = ctx.battle.params.small_river or ctx.battle.params.large_river
            if has_river != bool(value):
                return False
        elif key == "terrain":
            if ctx.battle.params.terrain_id != value:
                return False
        elif key == "frontage_full":
            full = ctx.camp.frontline_width >= ctx.camp.battle_width(ctx.battle)
            if full != bool(value):
                return False
        elif key == "reserves_available":
            if bool(ctx.camp.reserves) != bool(value):
                return False
        elif key == "artillery_ratio_gt":
            if not ctx.artillery_ratio > value:
                return False
        elif key == "victory_points_gt":
            if not ctx.battle.params.victory_points > value:
                return False
        elif key == "flag":
            if not ctx.has_flag(value):
                return False
        else:
            return False  # condition inconnue : tactique non disponible
    return True


# ---------------------------------------------------------------- registre

DEFAULT_CUSTOM_PATH = Path(__file__).resolve().parent.parent / "saves" / "tactics_custom.json"


class TacticRegistry:
    """Tactiques officielles + personnalisées, indexées par (nom, camp, phase)."""

    def __init__(self, custom_path: Path | str | None = DEFAULT_CUSTOM_PATH):
        self.custom_path = Path(custom_path) if custom_path else None
        self.tactics: dict[tuple[str, str, str], TacticDef] = {}
        self.reload()

    def reload(self) -> None:
        self.tactics.clear()
        with open(DATA_DIR / "tactics.json", encoding="utf-8") as f:
            payload = json.load(f)
        for entry in payload["tactics"]:
            tactic = TacticDef.from_dict(entry)
            self.tactics[tactic.key] = tactic
        if self.custom_path and self.custom_path.exists():
            try:
                with open(self.custom_path, encoding="utf-8") as f:
                    custom = json.load(f)
            except (OSError, json.JSONDecodeError):
                custom = []
            for entry in custom:
                tactic = TacticDef.from_dict(entry, custom=True)
                self.tactics[tactic.key] = tactic

    def save_custom(self) -> None:
        if self.custom_path is None:
            return
        self.custom_path.parent.mkdir(parents=True, exist_ok=True)
        payload = [t.to_dict() for t in self.tactics.values() if t.custom]
        with open(self.custom_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=4)

    def add_custom(self, tactic: TacticDef) -> None:
        tactic.custom = True
        self.tactics[tactic.key] = tactic
        self.save_custom()

    def remove_custom(self, key: tuple[str, str, str]) -> bool:
        tactic = self.tactics.get(key)
        if tactic is None or not tactic.custom:
            return False
        del self.tactics[key]
        self.save_custom()
        # Si une officielle du même nom avait été masquée, la recharger
        self.reload()
        return True

    def for_side_phase(self, side: str, phase: str) -> list[TacticDef]:
        return [t for t in self.tactics.values()
                if t.side == side and t.phase == phase]

    def custom_tactics(self) -> list[TacticDef]:
        return [t for t in self.tactics.values() if t.custom]

    def all_names(self) -> list[str]:
        return sorted({t.name for t in self.tactics.values()})


# ---------------------------------------------------------------- manager

class TacticManager:
    def __init__(self, registry: TacticRegistry | None = None):
        self.registry = registry or TacticRegistry()

    # ------------------------------------------------------------ sélection

    def maybe_reselect(self, battle: "Battle", log: "RoundLog") -> None:
        if (battle.round - 1) % RESELECT_INTERVAL == 0:
            self.reselect(battle, log)

    def reselect(self, battle: "Battle", log: "RoundLog") -> None:
        attacker, defender = battle.attacker, battle.defender

        # Initiative déterministe (§9.2)
        atk_eff = attacker.leader.skill
        def_eff = defender.leader.skill
        atk_recon, def_recon = attacker.total_recon, defender.total_recon
        if atk_recon > def_recon:
            atk_eff += RECON_SKILL_BONUS
        elif def_recon > atk_recon:
            def_eff += RECON_SKILL_BONUS
        if atk_eff > def_eff:
            winner, loser = attacker, defender
            advantage = atk_eff - def_eff
        else:  # égalité → avantage au défenseur
            winner, loser = defender, attacker
            advantage = def_eff - atk_eff

        loser_choice = self._pick(battle, loser, enemy_choice=None, advantage=0)
        winner_choice = self._pick(battle, winner, enemy_choice=loser_choice,
                                   advantage=advantage)

        active: dict[str, ActiveTactic | None] = {"attacker": None, "defender": None}
        for camp, choice in ((loser, loser_choice), (winner, winner_choice)):
            active[camp.side] = choice

        # Contres : une tactique perd tous ses effets si l'adversaire a
        # choisi une tactique listée dans son « contré par ».
        atk_t, def_t = active["attacker"], active["defender"]
        if atk_t and def_t:
            if def_t.name in atk_t.tactic.countered_by:
                atk_t.countered = True
            if atk_t.name in def_t.tactic.countered_by:
                def_t.countered = True

        battle.active_tactics = active

        # Changement de phase (tactique non contrée uniquement),
        # choix du perdant d'abord, celui du gagnant en dernier.
        for camp in (loser, winner):
            choice = active[camp.side]
            if choice and not choice.countered and choice.tactic.begins_phase:
                new_phase = choice.tactic.begins_phase
                if new_phase != battle.battle_phase:
                    battle.battle_phase = new_phase
                    log.events.append(
                        f"Phase de bataille : {PHASE_LABELS.get(new_phase, new_phase)} "
                        f"(déclenchée par {choice.name})")

        initiative_label = winner.label
        log.events.append(f"Initiative : {initiative_label} "
                          f"(compétence effective {max(atk_eff, def_eff)} vs {min(atk_eff, def_eff)})")
        for side, label in (("attacker", "Attaquant"), ("defender", "Défenseur")):
            choice = active[side]
            log.events.append(f"Tactique {label} : "
                              f"{choice.describe() if choice else '—'}")

    def _pick(self, battle: "Battle", camp: "Camp",
              enemy_choice: ActiveTactic | None, advantage: int) -> ActiveTactic | None:
        phase = battle.battle_phase
        pool = self.registry.for_side_phase(camp.side, phase)
        if not pool:
            return None

        # Override manuel (§9.3) : court-circuite le tirage pondéré.
        if camp.manual_tactic:
            forced = next((t for t in pool if t.name == camp.manual_tactic), None)
            if forced is not None:
                return ActiveTactic(forced, forced=True)

        ctx = TacticContext(camp, battle)
        available = [t for t in pool if eval_condition(t.trigger, ctx)]
        if not available:
            available = [t for t in pool if not t.trigger]
        if not available:
            return None

        weights = []
        for tactic in available:
            weight = self._weight(tactic, ctx, camp)
            # Bonus de contre : +35 % par point d'avantage si cette tactique
            # contre le choix déjà annoncé de l'adversaire (§9.2).
            if (enemy_choice is not None
                    and tactic.name in enemy_choice.tactic.countered_by):
                weight *= 1.0 + COUNTER_BONUS_PER_SKILL * max(advantage, 0)
            weights.append(weight)

        if all(w <= 0 for w in weights):
            return None
        # Écarte les poids nuls/négatifs
        pairs = [(t, w) for t, w in zip(available, weights) if w > 0]
        tactics, weights = zip(*pairs)
        chosen = battle.rng.weighted_choice(list(tactics), list(weights))
        return ActiveTactic(chosen)

    @staticmethod
    def _weight(tactic: TacticDef, ctx: TacticContext, camp: "Camp") -> float:
        weight = tactic.weight
        for rule in tactic.weight_rules:
            if eval_condition(rule.get("if"), ctx):
                if "set" in rule:
                    weight = rule["set"]
                if "mult" in rule:
                    weight *= rule["mult"]
        if camp.leader.preferred_tactic == tactic.name:
            weight *= PREFERRED_TACTIC_BONUS
        return weight
