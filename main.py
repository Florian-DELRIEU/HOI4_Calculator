"""Point d'entrée du simulateur de bataille HOI4."""
import sys

from PySide6.QtWidgets import QApplication

from gui.battle_window import BattleWindow
from gui.theme import ThemeManager


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Simulateur de bataille HOI4")
    theme = ThemeManager(app)
    window = BattleWindow(theme_manager=theme)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
