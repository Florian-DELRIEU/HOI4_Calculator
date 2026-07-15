"""Thème clair/sombre basculable en un clic (style Fusion + palettes)."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication


def _dark_palette() -> QPalette:
    p = QPalette()
    base = QColor(35, 35, 38)
    panel = QColor(45, 45, 48)
    text = QColor(230, 230, 230)
    accent = QColor(42, 130, 218)
    p.setColor(QPalette.Window, panel)
    p.setColor(QPalette.WindowText, text)
    p.setColor(QPalette.Base, base)
    p.setColor(QPalette.AlternateBase, panel)
    p.setColor(QPalette.ToolTipBase, QColor(60, 60, 63))
    p.setColor(QPalette.ToolTipText, text)
    p.setColor(QPalette.Text, text)
    p.setColor(QPalette.Button, panel)
    p.setColor(QPalette.ButtonText, text)
    p.setColor(QPalette.BrightText, Qt.red)
    p.setColor(QPalette.Link, accent)
    p.setColor(QPalette.Highlight, accent)
    p.setColor(QPalette.HighlightedText, Qt.white)
    p.setColor(QPalette.PlaceholderText, QColor(140, 140, 140))
    for group in (QPalette.Disabled,):
        p.setColor(group, QPalette.Text, QColor(120, 120, 120))
        p.setColor(group, QPalette.ButtonText, QColor(120, 120, 120))
        p.setColor(group, QPalette.WindowText, QColor(120, 120, 120))
    return p


class ThemeManager:
    """Applique et bascule le thème de l'application."""

    def __init__(self, app: QApplication):
        self.app = app
        self.dark = True
        self._light_palette = app.style().standardPalette()
        app.setStyle("Fusion")
        self.apply()

    def apply(self) -> None:
        self.app.setPalette(_dark_palette() if self.dark else self._light_palette)

    def toggle(self) -> bool:
        self.dark = not self.dark
        self.apply()
        return self.dark
