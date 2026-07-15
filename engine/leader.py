"""Modèle de leader / commandant (CDC §5)."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LeaderAbility:
    """Capacité de maréchal simplifiée : activation manuelle, bonus temporaire.

    ``attack_bonus``/``defense_bonus`` en pourcentage relatif (+10 = +10 %),
    ``org_restore`` en points d'organisation rendus immédiatement à toutes
    les divisions du camp.
    """

    name: str
    attack_bonus: float = 0.0
    defense_bonus: float = 0.0
    org_restore: float = 0.0
    duration_rounds: int = 24
    uses_per_battle: int = 1


@dataclass
class Leader:
    name: str = "Sans leader"
    attack_level: int = 0      # +2,5 % d'attaque par point
    defense_level: int = 0     # +2,5 % de défense par point
    traits: list[str] = field(default_factory=list)
    preferred_tactic: str = "" # +50 % de poids de sélection (§5)
    abilities: list[LeaderAbility] = field(default_factory=list)

    @property
    def skill(self) -> int:
        """Niveau de compétence global utilisé pour l'Initiative (§9.2)."""
        return self.attack_level + self.defense_level

    def has_trait(self, trait: str) -> bool:
        return trait in self.traits

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "attack_level": self.attack_level,
            "defense_level": self.defense_level,
            "traits": list(self.traits),
            "preferred_tactic": self.preferred_tactic,
            "abilities": [vars(a) for a in self.abilities],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Leader":
        abilities = [LeaderAbility(**a) for a in data.get("abilities", [])]
        return cls(
            name=data.get("name", "Sans leader"),
            attack_level=int(data.get("attack_level", 0)),
            defense_level=int(data.get("defense_level", 0)),
            traits=list(data.get("traits", [])),
            preferred_tactic=data.get("preferred_tactic", ""),
            abilities=abilities,
        )
