from PySide6.QtCore import QObject

from core.widget.server.settings_widget_ui import SettingsWidgetUI


class SettingsWidget(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.ui: SettingsWidgetUI = SettingsWidgetUI()

        self.ui.show()
