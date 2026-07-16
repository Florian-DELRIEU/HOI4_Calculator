"""Point d'entrée du simulateur de bataille HOI4."""
import sys

from PySide6.QtWidgets import QApplication

from gui.battle_window import BattleWindow
from gui.theme import ThemeManager

DEFAULT_TEMPLATES = [
    {"Nom de Template": "Infanterie 36", "PV": 176.2, "Organisation": 46.6,
     "Soft Attack": 97.0, "Hard Attack": 11.0, "Defense": 181.7, "Attaque": 34.1,
     "Piercing": 4.5, "Armor": 0.0, "Hardness": 0.0, "Width": 40,
     "Initiative": 0.05, "Experience": "regular"},
    {"Nom de Template": "Blindes 36", "PV": 107.2, "Organisation": 30.0,
     "Soft Attack": 127.0, "Hard Attack": 26.0, "Defense": 127.4, "Attaque": 132.6,
     "Piercing": 19.7, "Armor": 8.0, "Hardness": 0.3, "Width": 40,
     "Initiative": 0.05, "Experience": "regular"},
]


def ensure_default_templates() -> None:
    """Au premier lancement (exécutable vierge), crée deux templates d'exemple."""
    from persistence.divisions import DivisionStore, template_from_dict
    store = DivisionStore()
    if not store.list_templates():
        for entry in DEFAULT_TEMPLATES:
            store.save(template_from_dict(entry))


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Simulateur de bataille HOI4")
    ensure_default_templates()
    theme = ThemeManager(app)
    window = BattleWindow(theme_manager=theme)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
