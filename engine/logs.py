"""Structures de log de combat — exploitées par la GUI (résumé + tooltip
détaillé) et l'export CSV."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AttackReport:
    round: int
    striker_side: str          # "attacker" | "defender"
    striker: str
    target: str
    tactic: str = ""
    n_attacks: int = 0
    defenses_before: int = 0
    hits: int = 0
    hp_damage: float = 0.0
    org_damage: float = 0.0
    attack_factor: float = 1.0
    attack_detail: list = field(default_factory=list)    # [(libellé, %), …]
    damage_factor: float = 1.0
    damage_detail: list = field(default_factory=list)    # [(libellé, facteur), …]

    @property
    def side_label(self) -> str:
        return "Attaquant" if self.striker_side == "attacker" else "Défenseur"

    def summary(self) -> str:
        return (f"[{self.side_label}] {self.striker} attaque {self.target} — "
                f"{self.hits}/{self.n_attacks} coups, "
                f"PV −{self.hp_damage:.2f}, ORG −{self.org_damage:.2f}")

    def details(self) -> str:
        lines = [
            f"Tour {self.round} — {self.striker} ({self.side_label}) → {self.target}",
            f"Tactique active : {self.tactic or '—'}",
            f"Attaques : {self.n_attacks} | Défenses de la cible : {self.defenses_before}",
            f"Coups au but : {self.hits}",
            f"Dégâts PV : {self.hp_damage:.3f} | Dégâts organisation : {self.org_damage:.3f}",
            f"Facteur d'attaque cumulé : ×{self.attack_factor:.3f}",
        ]
        lines.extend(f"    {label} : {pct:+.1f} %" for label, pct in self.attack_detail)
        lines.append(f"Facteur de dégâts cumulé : ×{self.damage_factor:.3f}")
        lines.extend(f"    {label} : ×{value:.2f}" for label, value in self.damage_detail)
        return "\n".join(lines)


@dataclass
class RoundLog:
    round: int
    events: list[str] = field(default_factory=list)      # renforts, retraites…
    attacks: list[AttackReport] = field(default_factory=list)
    attacker_tactic: str = ""
    defender_tactic: str = ""
    phase: str = ""
    environment: str = ""      # état complet (terrain/météo/nuit/fort/débarquement…), mode « Tout »

    def total_damage(self, side: str) -> tuple[float, float]:
        """(PV, ORG) infligés par le camp donné pendant ce tour."""
        hp = sum(a.hp_damage for a in self.attacks if a.striker_side == side)
        org = sum(a.org_damage for a in self.attacks if a.striker_side == side)
        return hp, org
