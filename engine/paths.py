"""Résolution des chemins data/ et saves/ — compatible exécutable PyInstaller.

- ``data/`` (tables de référence, lecture seule) est embarqué dans
  l'exécutable (``--add-data``) et résolu via ``sys._MEIPASS`` en mode gelé.
- ``saves/`` (données utilisateur, lecture/écriture) vit à côté de
  l'exécutable en mode gelé, à la racine du projet en mode développement.
"""
from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def data_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent)) / "data"
    return _PROJECT_ROOT / "data"


def saves_dir() -> Path:
    if getattr(sys, "frozen", False):
        root = Path(sys.executable).parent / "saves"
    else:
        root = _PROJECT_ROOT / "saves"
    root.mkdir(parents=True, exist_ok=True)
    return root
