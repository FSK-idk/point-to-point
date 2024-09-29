from PySide6.QtCore import QObject

from core.config.config import config
from core.window.settings.settings_widget_ui import SettingsWidgetUI


class SettingsWidget(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.ui: SettingsWidgetUI = SettingsWidgetUI()

        self.ui.text_edit.textChanged.connect(self.onTextChanged)

        self.ui.show()

    def onTextChanged(self) -> None:
        config["Settings"]["text"] = self.ui.text_edit.toPlainText()

