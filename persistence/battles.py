"""Sauvegarde/chargement de batailles en cours (CDC §12).

Chaque sauvegarde nommée est un fichier ``saves/battles/<nom>.json``
contenant l'état complet : paramètres, tour, phase, tactiques actives,
divisions des deux camps avec PV/organisation et position, leaders,
état du générateur aléatoire (pour rejouer à l'identique) et un extrait
de log optionnel.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from engine.battle import Battle, Camp
from engine.division import Division
from engine.leader import Leader
from engine.params import BattleParams
from engine.tactics import ActiveTactic, TacticRegistry
from persistence.divisions import template_from_dict, template_to_dict

DEFAULT_ROOT = Path(__file__).resolve().parent.parent / "saves" / "battles"
MAX_LOG_CHARS = 200_000


def _safe_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', "_", name).strip() or "sans_nom"


# --------------------------------------------------------------- sérialiser

def _division_to_dict(division: Division, camp: Camp) -> dict:
    if division in camp.frontline:
        position = "frontline"
    elif division in camp.reserves:
        position = "reserve"
    elif division in camp.retreated:
        position = "retreated"
    elif division in camp.destroyed:
        position = "destroyed"
    else:
        position = "waiting"
    return {
        "template": template_to_dict(division.template),
        "nom": division.name,
        "pv": division.current_hp,
        "organisation": division.current_org,
        "parachutage_restant": division.paradropped_rounds_left,
        "position": position,
    }


def _camp_to_dict(camp: Camp) -> dict:
    return {
        "leader": camp.leader.to_dict(),
        "tactique_manuelle": camp.manual_tactic,
        "capacites_utilisees": camp.ability_uses,
        "capacites_actives": [
            {"capacite": vars(ability), "tours_restants": rounds}
            for ability, rounds in camp.active_abilities
        ],
        "divisions": [_division_to_dict(d, camp) for d in camp.divisions],
    }


def _tactic_to_dict(tactic: ActiveTactic | None) -> dict | None:
    if tactic is None:
        return None
    return {
        "name": tactic.tactic.name,
        "side": tactic.tactic.side,
        "phase": tactic.tactic.phase,
        "countered": tactic.countered,
        "forced": tactic.forced,
    }


def battle_to_dict(battle: Battle, log_text: str = "") -> dict:
    return {
        "version": 1,
        "params": battle.params.to_dict(),
        "round": battle.round,
        "phase": battle.battle_phase,
        "result": battle.result,
        "fort_integrity": battle.fort_integrity,
        "rng_seed": battle.rng.seed,
        "rng_state": _state_to_json(battle.rng.random.getstate()),
        "tactiques": {side: _tactic_to_dict(t)
                      for side, t in battle.active_tactics.items()},
        "attaquant": _camp_to_dict(battle.attacker),
        "defenseur": _camp_to_dict(battle.defender),
        "log_text": log_text[-MAX_LOG_CHARS:],
    }


def _state_to_json(state) -> list:
    version, internal, gauss = state
    return [version, list(internal), gauss]


def _state_from_json(data) -> tuple:
    version, internal, gauss = data
    return (version, tuple(internal), gauss)


# ---------------------------------------------------------------- restaurer

def _camp_from_dict(camp: Camp, data: dict) -> None:
    from engine.leader import LeaderAbility
    camp.leader = Leader.from_dict(data.get("leader", {}))
    camp.manual_tactic = data.get("tactique_manuelle")
    camp.ability_uses = dict(data.get("capacites_utilisees", {}))
    camp.active_abilities = [
        [LeaderAbility(**entry["capacite"]), entry["tours_restants"]]
        for entry in data.get("capacites_actives", [])
    ]
    for div_data in data.get("divisions", []):
        template = template_from_dict(div_data["template"])
        division = Division(template, custom_name=div_data.get("nom", ""))
        division.current_hp = float(div_data.get("pv", division.current_hp))
        division.current_org = float(div_data.get("organisation", division.current_org))
        division.paradropped_rounds_left = int(div_data.get("parachutage_restant", 0))
        camp.divisions.append(division)
        position = div_data.get("position", "waiting")
        if position == "frontline":
            camp.frontline.append(division)
            division.in_frontline = True
        elif position == "reserve":
            camp.reserves.append(division)
        elif position == "retreated":
            camp.retreated.append(division)
        elif position == "destroyed":
            camp.destroyed.append(division)


def battle_from_dict(data: dict,
                     registry: TacticRegistry | None = None) -> tuple[Battle, str]:
    """Reconstruit une bataille. Renvoie ``(bataille, texte_de_log)``."""
    params = BattleParams.from_dict(data.get("params", {}))
    battle = Battle(params, seed=data.get("rng_seed"), tactic_registry=registry)
    battle.round = int(data.get("round", 0))
    battle.battle_phase = data.get("phase", "default")
    battle.result = data.get("result")
    battle.fort_integrity = float(data.get("fort_integrity", 0.0))
    if data.get("rng_state"):
        try:
            battle.rng.random.setstate(_state_from_json(data["rng_state"]))
        except (TypeError, ValueError):
            pass  # état illisible : on garde la graine

    _camp_from_dict(battle.attacker, data.get("attaquant", {}))
    _camp_from_dict(battle.defender, data.get("defenseur", {}))

    reg = battle.tactic_manager.registry if battle.tactic_manager else None
    for side, t_data in (data.get("tactiques") or {}).items():
        if not t_data or reg is None:
            continue
        tactic = reg.tactics.get((t_data["name"], t_data["side"], t_data["phase"]))
        if tactic is not None:
            battle.active_tactics[side] = ActiveTactic(
                tactic, countered=t_data.get("countered", False),
                forced=t_data.get("forced", False))
    return battle, data.get("log_text", "")


# ------------------------------------------------------------------- store

class BattleSaveStore:
    def __init__(self, root: Path | str = DEFAULT_ROOT):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, name: str) -> Path:
        return self.root / f"{_safe_filename(name)}.json"

    def list_saves(self) -> list[dict]:
        """Liste [{nom, round, resultat}] triée par nom."""
        saves = []
        for path in sorted(self.root.glob("*.json")):
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
            except (OSError, json.JSONDecodeError):
                continue
            saves.append({
                "nom": path.stem,
                "round": data.get("round", 0),
                "resultat": data.get("result"),
                "phase": data.get("phase", "default"),
            })
        return saves

    def save(self, name: str, battle: Battle, log_text: str = "") -> Path:
        path = self._path(name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(battle_to_dict(battle, log_text), f, ensure_ascii=False, indent=2)
        return path

    def load(self, name: str,
             registry: TacticRegistry | None = None) -> tuple[Battle, str]:
        with open(self._path(name), encoding="utf-8") as f:
            data = json.load(f)
        return battle_from_dict(data, registry)

    def delete(self, name: str) -> bool:
        path = self._path(name)
        if path.exists():
            path.unlink()
            return True
        return False

    def rename(self, old: str, new: str) -> bool:
        src, dst = self._path(old), self._path(new)
        if not src.exists() or dst.exists():
            return False
        src.rename(dst)
        return True
