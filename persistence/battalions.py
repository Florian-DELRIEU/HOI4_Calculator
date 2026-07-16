"""Persistance des bataillons personnalisés (saves/battalions_custom.json).

Coexistent avec les bataillons officiels de ``data/battalions.json`` :
après toute modification, ``engine.composition.reload()`` est appelé pour
que les nouveaux bataillons soient immédiatement disponibles dans l'éditeur
de division et le moteur d'agrégation.
"""
from __future__ import annotations

import json

from engine import composition
from engine.composition import CUSTOM_BATTALIONS_PATH, BattalionDef


class CustomBattalionStore:
    def __init__(self, path=CUSTOM_BATTALIONS_PATH):
        self.path = path

    # ------------------------------------------------------------- lecture

    def list_custom(self) -> list[BattalionDef]:
        return sorted(composition.load_custom().values(), key=lambda b: b.nom)

    def get(self, battalion_id: str) -> BattalionDef | None:
        return composition.load_custom().get(battalion_id)

    def _raw_entries(self) -> list[dict]:
        if not self.path.exists():
            return []
        try:
            with open(self.path, encoding="utf-8") as f:
                payload = json.load(f)
        except (OSError, json.JSONDecodeError):
            return []
        return [e for e in payload if isinstance(e, dict) and e.get("id")]

    # ------------------------------------------------------------ écriture

    def _write(self, entries: list[dict]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=4)
        composition.reload()

    def upsert(self, battalion: BattalionDef) -> None:
        data = battalion.to_dict()
        entries = [e for e in self._raw_entries() if e.get("id") != data["id"]]
        entries.append(data)
        self._write(entries)

    def delete(self, battalion_id: str) -> bool:
        entries = self._raw_entries()
        remaining = [e for e in entries if e.get("id") != battalion_id]
        if len(remaining) == len(entries):
            return False
        self._write(remaining)
        return True
