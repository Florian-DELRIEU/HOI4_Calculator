"""Persistance des templates de division.

Format JSON compatible avec le projet de référence (clés françaises :
``Nom de Template``, ``PV``, ``Organisation``, ``Soft Attack``…), étendu
avec l'expérience, la reconnaissance et la composition en bataillons.

Organisation sur disque : un fichier par template dans
``saves/divisions/<dossier>/<nom>.json``. Les anciens fichiers « liste »
(tableau JSON de plusieurs templates) sont également lus.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from engine.division import DivisionStats, DivisionTemplate
from engine.paths import saves_dir

DEFAULT_ROOT = saves_dir() / "divisions"

# Clés héritées du projet de référence — à conserver telles quelles.
_LEGACY_KEYS = {
    "PV": "hp",
    "Organisation": "organisation",
    "Soft Attack": "soft_attack",
    "Hard Attack": "hard_attack",
    "Defense": "defense",
    "Attaque": "breakthrough",     # « Attaque » = percée dans l'ancien format
    "Piercing": "piercing",
    "Armor": "armor",
    "Hardness": "hardness",
    "Width": "width",
    "Initiative": "initiative",
}
_EXTENDED_KEYS = {
    "Attaque Aerienne": "air_attack",
    "Vitesse": "speed",
}


def template_to_dict(template: DivisionTemplate) -> dict:
    data = {"Nom de Template": template.name}
    for key, attr in _LEGACY_KEYS.items():
        data[key] = getattr(template.stats, attr)
    for key, attr in _EXTENDED_KEYS.items():
        data[key] = getattr(template.stats, attr)
    data["Experience"] = template.experience
    data["Recon"] = template.recon
    if template.battalions:
        data["Bataillons"] = list(template.battalions)
    if template.support_companies:
        data["Compagnies de soutien"] = list(template.support_companies)
    return data


def template_from_dict(data: dict) -> DivisionTemplate:
    stats = DivisionStats()
    for key, attr in {**_LEGACY_KEYS, **_EXTENDED_KEYS}.items():
        if key in data:
            setattr(stats, attr, float(data[key]))
    return DivisionTemplate(
        name=data.get("Nom de Template", "Sans nom"),
        stats=stats,
        experience=data.get("Experience", "regular"),
        recon=float(data.get("Recon", 0.0)),
        battalions=list(data.get("Bataillons", [])),
        support_companies=list(data.get("Compagnies de soutien", [])),
    )


def _safe_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', "_", name).strip() or "sans_nom"


class DivisionStore:
    """Gestion des templates : lister, sauver, dupliquer, renommer, ranger."""

    def __init__(self, root: Path | str = DEFAULT_ROOT):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------- lecture

    def list_templates(self) -> list[DivisionTemplate]:
        templates: list[DivisionTemplate] = []
        for path in sorted(self.root.rglob("*.json")):
            folder = str(path.parent.relative_to(self.root))
            folder = "" if folder == "." else folder
            try:
                with open(path, encoding="utf-8") as f:
                    payload = json.load(f)
            except (OSError, json.JSONDecodeError):
                continue
            entries = payload if isinstance(payload, list) else [payload]
            for entry in entries:
                if isinstance(entry, dict) and "Nom de Template" in entry:
                    template = template_from_dict(entry)
                    template.folder = folder
                    templates.append(template)
        return templates

    def get(self, name: str) -> DivisionTemplate | None:
        return next((t for t in self.list_templates() if t.name == name), None)

    def folders(self) -> list[str]:
        found = {t.folder for t in self.list_templates()}
        found.update(str(p.relative_to(self.root))
                     for p in self.root.rglob("*") if p.is_dir())
        return sorted(f for f in found if f)

    # ------------------------------------------------------------ écriture

    def _path_for(self, template: DivisionTemplate) -> Path:
        directory = self.root / template.folder if template.folder else self.root
        directory.mkdir(parents=True, exist_ok=True)
        return directory / f"{_safe_filename(template.name)}.json"

    def save(self, template: DivisionTemplate) -> Path:
        path = self._path_for(template)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(template_to_dict(template), f, ensure_ascii=False, indent=4)
        return path

    def delete(self, name: str) -> bool:
        deleted = False
        for path in list(self.root.rglob("*.json")):
            try:
                with open(path, encoding="utf-8") as f:
                    payload = json.load(f)
            except (OSError, json.JSONDecodeError):
                continue
            if isinstance(payload, dict) and payload.get("Nom de Template") == name:
                path.unlink()
                deleted = True
            elif isinstance(payload, list):
                remaining = [e for e in payload if e.get("Nom de Template") != name]
                if len(remaining) != len(payload):
                    deleted = True
                    if remaining:
                        with open(path, "w", encoding="utf-8") as f:
                            json.dump(remaining, f, ensure_ascii=False, indent=4)
                    else:
                        path.unlink()
        return deleted

    def rename(self, old_name: str, new_name: str) -> bool:
        template = self.get(old_name)
        if template is None:
            return False
        self.delete(old_name)
        template.name = new_name
        self.save(template)
        return True

    def duplicate(self, name: str, copy_name: str | None = None) -> DivisionTemplate | None:
        template = self.get(name)
        if template is None:
            return None
        copy = template_from_dict(template_to_dict(template))
        copy.folder = template.folder
        copy.name = copy_name or f"{template.name} (copie)"
        self.save(copy)
        return copy

    def import_legacy_file(self, path: Path | str) -> int:
        """Importe un ancien fichier « liste » (ex. divisions.json du projet
        de référence) : chaque entrée devient un fichier individuel."""
        with open(path, encoding="utf-8") as f:
            payload = json.load(f)
        entries = payload if isinstance(payload, list) else [payload]
        count = 0
        for entry in entries:
            if isinstance(entry, dict) and "Nom de Template" in entry:
                self.save(template_from_dict(entry))
                count += 1
        return count
