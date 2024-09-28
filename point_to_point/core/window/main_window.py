from PySide6.QtCore import QObject, Slot

from core.window.main_window_ui import MainWindowUI


class MainWindow(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.ui: MainWindowUI = MainWindowUI()

        self.ui.main_menu.ui.server_button.clicked.connect(self.openServerMenu)
        self.ui.main_menu.ui.client_button.clicked.connect(self.openClientMenu)
        self.ui.server_menu.ui.back_button.clicked.connect(self.openMainMenu)
        self.ui.client_menu.ui.back_button.clicked.connect(self.openMainMenu)

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
