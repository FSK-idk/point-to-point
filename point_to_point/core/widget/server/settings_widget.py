from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget

from core.widget.server.settings_widget_ui import SettingsWidgetUI


class SettingsWidget(QObject):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__()

        self.ui: SettingsWidgetUI = SettingsWidgetUI(parent)

        self.ui.show()

