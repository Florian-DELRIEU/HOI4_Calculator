"""Modèle de division : statistiques de template + état en bataille."""
from __future__ import annotations

import itertools
import math
from dataclasses import dataclass, field, asdict

from engine.gamedata import EXPERIENCE

# Niveaux d'expérience (CDC §8.5) — chargés depuis data/experience.json.
EXPERIENCE_BONUS = {k: float(v["bonus"]) for k, v in EXPERIENCE.items()}
EXPERIENCE_LABELS = {k: v["nom"] for k, v in EXPERIENCE.items()}

_id_counter = itertools.count(1)


@dataclass
class DivisionStats:
    """Statistiques finales d'une division (mode manuel ou agrégées)."""

    hp: float = 0.0
    organisation: float = 0.0
    soft_attack: float = 0.0
    hard_attack: float = 0.0
    defense: float = 0.0
    breakthrough: float = 0.0
    armor: float = 0.0
    piercing: float = 0.0
    hardness: float = 0.0          # 0..1
    width: float = 0.0
    initiative: float = 0.0        # 0..1 (apport transmissions)
    air_attack: float = 0.0
    speed: float = 4.0

    def copy(self) -> "DivisionStats":
        return DivisionStats(**asdict(self))


@dataclass
class DivisionTemplate:
    """Template nommé, persistable, éventuellement composé de bataillons."""

    name: str
    stats: DivisionStats = field(default_factory=DivisionStats)
    experience: str = "regular"
    recon: float = 0.0
    # Composition optionnelle : liste de noms de bataillons (jusqu'à 25)
    # et de compagnies de soutien (jusqu'à 5). Vide = mode manuel pur.
    battalions: list[str] = field(default_factory=list)
    support_companies: list[str] = field(default_factory=list)
    folder: str = ""  # sous-dossier de rangement dans saves/divisions

    def spawn(self) -> "Division":
        return Division(self)

    def artillery_ratio(self) -> float:
        """Part de bataillons d'artillerie dans la composition (déclencheur
        des tactiques Assault / Street by Street Barrage)."""
        if not self.battalions:
            return 0.0
        try:
            from engine.composition import is_artillery
        except ImportError:
            return 0.0
        count = sum(1 for b in self.battalions if is_artillery(b))
        return count / len(self.battalions)


class Division:
    """Instance d'une division engagée dans une bataille."""

    def __init__(self, template: DivisionTemplate, custom_name: str = ""):
        self.template = template
        self.name = custom_name or template.name
        self.stats = template.stats.copy()
        self.experience = template.experience
        self.recon = template.recon
        self.id = f"div{next(_id_counter)}"
        # État courant
        self.current_hp = self.stats.hp
        self.current_org = self.stats.organisation
        self.defense_pool = 0          # défenses restantes ce tour (§8.4)
        self.in_frontline = False
        self.paradropped_rounds_left = 0   # pénalité −30 % pendant 48 h (§8.5)
        self.target_list: list["Division"] = []
        self.primary_target: "Division | None" = None

    # ------------------------------------------------------------------ état

    @property
    def strength_ratio(self) -> float:
        return self.current_hp / self.stats.hp if self.stats.hp > 0 else 0.0

    @property
    def strength_step(self) -> float:
        """Force arrondie au palier de 10 % inférieur (§8.4.6).

        Une division entre 90 et 100 % de ses PV inflige ×0,9 ; on plancher
        à 0,1 pour qu'une division encore vivante inflige toujours quelque
        chose.
        """
        if self.stats.hp <= 0:
            return 0.0
        step = math.floor(self.strength_ratio * 10) / 10
        return max(min(step, 1.0), 0.1)

    @property
    def org_ratio(self) -> float:
        if self.stats.organisation <= 0:
            return 0.0
        return self.current_org / self.stats.organisation

    @property
    def is_broken(self) -> bool:
        """Plus d'organisation : la division se replie."""
        return self.current_org <= 0

    @property
    def is_destroyed(self) -> bool:
        return self.current_hp <= 0

    @property
    def can_fight(self) -> bool:
        return not self.is_broken and not self.is_destroyed

    @property
    def experience_bonus(self) -> float:
        return EXPERIENCE_BONUS.get(self.experience, 0.0)

    # ------------------------------------------------------------- combat

    def take_damage(self, hp_damage: float, org_damage: float) -> None:
        self.current_hp = max(round(self.current_hp - hp_damage, 3), 0.0)
        self.current_org = max(round(self.current_org - org_damage, 3), 0.0)

    def __repr__(self):
        return f"<Division {self.name} PV={self.current_hp:.1f} ORG={self.current_org:.1f}>"
