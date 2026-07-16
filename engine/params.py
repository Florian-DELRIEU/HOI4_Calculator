"""Paramètres d'une bataille : terrain, météo, fortifications et les
curseurs manuels du CDC §9.5 (ravitaillement, aviation, renseignement…)."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict

from engine.gamedata import (TEMPERATURE, TERRAINS, WEATHER, Terrain,
                             TemperatureLevel, WeatherCondition)


@dataclass
class SideParams:
    """Curseurs manuels par camp (CDC §9.5)."""

    coordination: float = 0.0          # stat de camp (radio/RADAR), 0..~0.5
    supply_shortage: float = 0.0       # 0 = ravitaillé, 1 = pénurie totale
    enemy_air_superiority: float = 0.0 # 0..0.35 (pénalité subie)
    air_support_bonus: float = 0.0     # bonus manuel d'appui aérien (+%)
    nation_attack_bonus: float = 0.0   # bonus de nation (attaque, ±)
    nation_defense_bonus: float = 0.0  # bonus de nation (défense, ±)
    intel_advantage: float = 0.0       # 0..0.15 (réglé directement en %)
    night_attack_bonus: float = 0.0    # atténuation de la pénalité de nuit, 0..1
    # Drapeaux utilisés par les déclencheurs de tactiques (§9.5)
    artillery_ratio: float = 0.0       # override manuel du ratio d'artillerie
    is_japan: bool = False             # Banzai Charge
    masterful_blitz: bool = False      # focus soviétique (Masterful Blitz)
    has_flame_tanks: bool = False      # Armour Supported Urban Assault
    has_engineers: bool = False        # Mouse Holing

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SideParams":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class BattleParams:
    terrain_id: str = "plains"
    weather_id: str = "clear"
    temperature_id: str = "normal"      # extra optionnel (§7.3), voir data/temperature.json
    is_night: bool = False
    small_river: bool = False
    large_river: bool = False
    naval_invasion: bool = False
    naval_invasion_advanced: bool = False  # extra optionnel (§7.2) : pénalité progressive
    fort_level: int = 0
    extra_directions: int = 0          # directions d'attaque supplémentaires
    encirclement: bool = False         # défenseur encerclé (−30 %)
    entrenchment: int = 0              # retranchement du défenseur (+2 %/pt)
    planning_bonus: float = 0.0        # attaquant, 0..0.30
    victory_points: int = 0            # valeur du point de victoire (Urban Defense)
    attacker: SideParams = field(default_factory=SideParams)
    defender: SideParams = field(default_factory=SideParams)

    @property
    def terrain(self) -> Terrain:
        return TERRAINS[self.terrain_id]

    @property
    def weather(self) -> WeatherCondition:
        return WEATHER[self.weather_id]

    @property
    def temperature(self) -> TemperatureLevel:
        return TEMPERATURE[self.temperature_id]

    @property
    def base_combat_width(self) -> float:
        """Largeur de bataille : terrain + bonus par direction supplémentaire
        (§7.1/§8.1 — on utilise le bonus propre au terrain, plus précis que
        le « +40 » générique du §8.1)."""
        t = self.terrain
        return t.combat_width + self.extra_directions * t.extra_width_per_direction

    @property
    def effective_fort_level(self) -> int:
        """Chaque direction d'attaque supplémentaire annule un niveau de fort,
        mais jamais le dernier (§7.2 — mécanique `extra_side` conservée)."""
        if self.fort_level <= 0:
            return 0
        return max(self.fort_level - self.extra_directions, 1)

    def to_dict(self) -> dict:
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "BattleParams":
        data = dict(data)
        atk = SideParams.from_dict(data.pop("attacker", {}))
        deff = SideParams.from_dict(data.pop("defender", {}))
        fields = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        fields.pop("attacker", None)
        fields.pop("defender", None)
        return cls(attacker=atk, defender=deff, **fields)
