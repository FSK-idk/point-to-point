from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QWidget

from core.window.main_window_ui import MainWindowUI


class MainWindow(QObject):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__()

        self.ui: MainWindowUI = MainWindowUI(parent)

        self.ui.main_menu.ui.server_button.clicked.connect(self.openServerMenu)
        self.ui.main_menu.ui.client_button.clicked.connect(self.openClientMenu)
        self.ui.server.backToMainMenu.connect(self.openMainMenu)
        self.ui.client.backToMainMenu.connect(self.openMainMenu)

        self.ui.show()

    @Slot()
    def openMainMenu(self) -> None:
        self.ui.main_layout.setCurrentIndex(0)

    @Slot()
    def openServerMenu(self) -> None:
        self.ui.main_layout.setCurrentIndex(1)

    @Slot()
    def openClientMenu(self) -> None:
        self.ui.main_layout.setCurrentIndex(2)

    @Slot()
    def openSettings(self) -> None:
        self.ui.main_layout.setCurrentIndex(3)
