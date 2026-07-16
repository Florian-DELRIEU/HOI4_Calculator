"""Export CSV des logs de combat (CDC §11)."""
from __future__ import annotations

import csv
from pathlib import Path

from engine.battle import Battle

COLUMNS = [
    "tour", "phase", "camp", "division_attaquante", "division_cible",
    "tactique", "nb_attaques", "defenses_cible", "coups_au_but",
    "degats_pv", "degats_organisation", "facteur_attaque", "facteur_degats",
    "bonus_cumules",
]


def export_battle_csv(battle: Battle, path: Path | str) -> int:
    """Écrit les logs de la bataille en CSV. Renvoie le nombre de lignes."""
    rows = 0
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(COLUMNS)
        for round_log in battle.logs:
            for attack in round_log.attacks:
                bonus = " | ".join(f"{label}: {pct:+.1f}%"
                                   for label, pct in attack.attack_detail)
                writer.writerow([
                    attack.round,
                    round_log.phase,
                    "Attaquant" if attack.striker_side == "attacker" else "Défenseur",
                    attack.striker,
                    attack.target,
                    attack.tactic,
                    attack.n_attacks,
                    attack.defenses_before,
                    attack.hits,
                    f"{attack.hp_damage:.3f}",
                    f"{attack.org_damage:.3f}",
                    f"{attack.attack_factor:.3f}",
                    f"{attack.damage_factor:.3f}",
                    bonus,
                ])
                rows += 1
    return rows
