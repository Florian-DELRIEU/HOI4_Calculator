"""Persistance des leaders (saves/leaders.json)."""
from __future__ import annotations

import json
from pathlib import Path

from engine.leader import Leader

DEFAULT_PATH = Path(__file__).resolve().parent.parent / "saves" / "leaders.json"


class LeaderStore:
    def __init__(self, path: Path | str = DEFAULT_PATH):
        self.path = Path(path)

    def list_leaders(self) -> list[Leader]:
        if not self.path.exists():
            return []
        try:
            with open(self.path, encoding="utf-8") as f:
                payload = json.load(f)
        except (OSError, json.JSONDecodeError):
            return []
        return [Leader.from_dict(entry) for entry in payload]

    def save_all(self, leaders: list[Leader]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([l.to_dict() for l in leaders], f, ensure_ascii=False, indent=4)

    def upsert(self, leader: Leader) -> None:
        leaders = [l for l in self.list_leaders() if l.name != leader.name]
        leaders.append(leader)
        self.save_all(sorted(leaders, key=lambda l: l.name))

    def delete(self, name: str) -> bool:
        leaders = self.list_leaders()
        remaining = [l for l in leaders if l.name != name]
        if len(remaining) == len(leaders):
            return False
        self.save_all(remaining)
        return True

    def get(self, name: str) -> Leader | None:
        return next((l for l in self.list_leaders() if l.name == name), None)
