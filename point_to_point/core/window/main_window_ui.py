from PySide6.QtWidgets import QMainWindow, QWidget, QStackedLayout

from core.window.main_menu.main_menu_widget import MainMenuWidget
from core.window.server_menu.server_menu_widget import ServerMenuWidget
from core.window.client_menu.client_menu_widget import ClientMenuWidget


class MainWindowUI(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setGeometry(0, 0, 1000, 600)
        self.setMinimumSize(400, 300)
        self.setWindowTitle("Point to Point")

        self.main_menu: MainMenuWidget = MainMenuWidget()
        self.server_menu: ServerMenuWidget = ServerMenuWidget()
        self.client_menu: ClientMenuWidget = ClientMenuWidget()

        self.main_layout: QStackedLayout = QStackedLayout()
        self.main_layout.addWidget(self.main_menu.ui)
        self.main_layout.addWidget(self.server_menu.ui)
        self.main_layout.addWidget(self.client_menu.ui)

        self.main_layout.setCurrentIndex(0)

        self.widget = QWidget()
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)

