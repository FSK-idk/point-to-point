from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget

from core.widget.main.main_menu_widget_ui import MainMenuWidgetUI


class MainMenuWidget(QObject):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__()

        self.ui: MainMenuWidgetUI = MainMenuWidgetUI(parent)

        self.ui.show()

