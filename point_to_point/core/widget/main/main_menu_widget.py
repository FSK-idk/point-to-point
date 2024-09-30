from PySide6.QtCore import QObject

from core.widget.main.main_menu_widget_ui import MainMenuWidgetUI


class MainMenuWidget(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.ui: MainMenuWidgetUI = MainMenuWidgetUI()

        self.ui.show()

