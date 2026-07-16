"""Chargement des tables de référence depuis le dossier data/.

Les tables (terrains, météo, expérience, bataillons, tactiques) vivent dans
des fichiers JSON séparés du code métier (exigence CDC §3) ; ce module les
charge une fois et les expose sous forme d'objets simples.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from engine.paths import data_dir

DATA_DIR = data_dir()


def _load(name: str) -> dict:
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return json.load(f)


@dataclass(frozen=True)
class Terrain:
    id: str
    nom: str
    combat_width: float
    extra_width_per_direction: float
    movement_cost: float
    attrition: float
    attack_modifier: float        # pénalité d'attaque pour l'attaquant (§7.1)
    enemy_air_mitigation: float   # atténuation de la sup. aérienne ennemie
    max_fort: int

    def __str__(self):
        return self.nom


@dataclass(frozen=True)
class WeatherCondition:
    id: str
    nom: str
    attack: float
    breakthrough: float
    defense: float
    attacker_speed: float

    def __str__(self):
        return self.nom


def _load_terrains() -> dict[str, Terrain]:
    return {t["id"]: Terrain(**t) for t in _load("terrains.json")["terrains"]}


def _load_weather() -> dict[str, WeatherCondition]:
    return {w["id"]: WeatherCondition(**w) for w in _load("weather.json")["conditions"]}


def _load_experience() -> dict[str, dict]:
    return {lvl["id"]: lvl for lvl in _load("experience.json")["levels"]}


TERRAINS: dict[str, Terrain] = _load_terrains()
WEATHER: dict[str, WeatherCondition] = _load_weather()
EXPERIENCE: dict[str, dict] = _load_experience()
