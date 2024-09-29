from PySide6.QtCore import QObject, Slot

from core.window.main_window_ui import MainWindowUI


class MainWindow(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.ui: MainWindowUI = MainWindowUI()

        self.ui.main_menu.ui.server_button.clicked.connect(self.openServerMenu)
        self.ui.main_menu.ui.client_button.clicked.connect(self.openClientMenu)
        self.ui.main_menu.ui.settings_button.clicked.connect(self.openSettings)
        self.ui.server.back_to_main_menu.connect(self.openMainMenu)
        self.ui.client.back_to_main_menu.connect(self.openMainMenu)
        self.ui.settings.ui.back_button.clicked.connect(self.openMainMenu)

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
