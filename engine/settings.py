"""Paramètres configurables du simulateur (bouton « Paramètres »).

Un unique objet :data:`SETTINGS` est partagé par tout le moteur. Il est
modifié **en place** (jamais rebindé) afin que toutes les références déjà
importées (``from engine.settings import SETTINGS``) voient immédiatement les
changements. La persistance est un JSON dans ``saves/settings.json``.

Les valeurs par défaut correspondent aux constantes officielles du moteur ;
elles ne sont PAS chargées automatiquement à l'import (pour que les tests
restent déterministes) — c'est ``main.py`` qui appelle :func:`load` au
démarrage de l'application.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, fields
from pathlib import Path

from engine.paths import saves_dir


@dataclass
class Settings:
    # --- Combat (leviers directs sur la durée des batailles) ---
    hp_damage_coef: float = 0.06        # dégâts PV par coup
    org_damage_coef: float = 0.053      # dégâts organisation par coup
    hit_chance_defended: float = 0.10   # chance de toucher une cible avec défenses
    hit_chance_undefended: float = 0.40 # chance de toucher une cible sans défense
    reinforce_chance: float = 0.02      # chance/tour qu'une réserve rejoigne le front
    # --- Tactiques ---
    tactics_enabled: bool = True
    tactic_reselect_interval: int = 12  # heures entre deux re-sélections
    # --- Fortifications ---
    fort_erosion_enabled: bool = True   # les combats érodent le niveau de fort
    # --- Déroulement de la bataille ---
    auto_stop_on_victory: bool = True   # « Lancer N tours » s'arrête à la victoire
    use_fixed_seed: bool = False        # batailles reproductibles
    fixed_seed: int = 0

    def to_dict(self) -> dict:
        return asdict(self)

    def update_from(self, data: dict) -> None:
        """Applique en place les clés reconnues (ignore les inconnues)."""
        valid = {f.name for f in fields(self)}
        for key, value in data.items():
            if key in valid:
                setattr(self, key, value)

    def reset(self) -> None:
        """Rétablit toutes les valeurs par défaut, en place."""
        self.update_from(asdict(Settings()))


# Métadonnées pour construire automatiquement le dialogue de paramètres.
# (clé, libellé, type, min, max, pas, groupe, aide)
FIELD_META = [
    ("hp_damage_coef", "Dégâts PV par coup (coefficient)", "float", 0.0, 5.0, 0.01, "Combat",
     "Plus élevé = les PV chutent plus vite = batailles plus courtes. Officiel : 0,06."),
    ("org_damage_coef", "Dégâts organisation par coup (coefficient)", "float", 0.0, 5.0, 0.001, "Combat",
     "Plus élevé = l'organisation chute plus vite = replis plus rapides. Officiel : 0,053."),
    ("hit_chance_defended", "Chance de toucher (cible avec défenses)", "float", 0.0, 1.0, 0.01, "Combat",
     "Probabilité qu'un coup porte tant que la cible a des défenses. Officiel : 0,10."),
    ("hit_chance_undefended", "Chance de toucher (cible sans défense)", "float", 0.0, 1.0, 0.01, "Combat",
     "Probabilité qu'un coup porte quand la cible n'a plus de défense. Officiel : 0,40."),
    ("reinforce_chance", "Chance de renfort depuis la réserve (par tour)", "float", 0.0, 1.0, 0.01, "Combat",
     "Chance/heure qu'une division en réserve rejoigne le front. Officiel : 0,02."),

    ("tactics_enabled", "Activer le système de tactiques", "bool", 0, 0, 0, "Tactiques",
     "Si désactivé, aucune tactique n'est sélectionnée (combat neutre)."),
    ("tactic_reselect_interval", "Intervalle de re-sélection des tactiques (heures)", "int", 1, 72, 1, "Tactiques",
     "Nombre de tours entre deux re-tirages de tactique. Officiel : 12."),

    ("fort_erosion_enabled", "Érosion des forts par les combats", "bool", 0, 0, 0, "Fortifications",
     "Si activé, les attaques dégradent progressivement le niveau de fort (§8.6)."),

    ("auto_stop_on_victory", "Arrêt automatique des « N tours » à la victoire", "bool", 0, 0, 0, "Déroulement",
     "Interrompt un lot de N tours dès qu'un camp est vaincu."),
    ("use_fixed_seed", "Graine aléatoire fixe (batailles reproductibles)", "bool", 0, 0, 0, "Déroulement",
     "Si activé, chaque nouvelle bataille utilise la graine ci-dessous."),
    ("fixed_seed", "Graine aléatoire", "int", 0, 2_000_000_000, 1, "Déroulement",
     "Valeur de la graine utilisée quand la graine fixe est activée."),
]

GROUP_ORDER = ["Combat", "Tactiques", "Fortifications", "Déroulement"]

DEFAULTS = Settings()
SETTINGS = Settings()

SETTINGS_PATH = saves_dir() / "settings.json"


def load(path=None) -> None:
    """Charge les paramètres depuis le disque dans SETTINGS (en place)."""
    target = Path(path or SETTINGS_PATH)
    try:
        with open(target, encoding="utf-8") as f:
            SETTINGS.update_from(json.load(f))
    except (OSError, json.JSONDecodeError):
        pass


def save(path=None) -> None:
    """Écrit SETTINGS sur le disque."""
    target = Path(path or SETTINGS_PATH)
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        json.dump(SETTINGS.to_dict(), f, ensure_ascii=False, indent=4)


def reset_to_defaults() -> None:
    """Rétablit les valeurs par défaut en mémoire (sans écrire sur le disque)."""
    SETTINGS.reset()
