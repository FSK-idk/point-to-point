from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QStackedLayout
from PySide6.QtGui import QCloseEvent

from core.widget.main.main_menu_widget import MainMenuWidget
from core.widget.server.server_widget import ServerWidget
from core.widget.client.client_widget import ClientWidget


class MainWindowUI(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setGeometry(0, 0, 1000, 600)
        self.setMinimumSize(400, 300)
        self.setWindowTitle("Point to Point")

        self.main_menu: MainMenuWidget = MainMenuWidget(self)
        self.server: ServerWidget = ServerWidget(self)
        self.client: ClientWidget = ClientWidget(self)

        self.main_layout: QStackedLayout = QStackedLayout()
        self.main_layout.addWidget(self.main_menu.ui)
        self.main_layout.addWidget(self.server.ui)
        self.main_layout.addWidget(self.client.ui)

        self.main_layout.setCurrentIndex(0)

        self.widget = QWidget(self)
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)

    def closeEvent(self, event: QCloseEvent) -> None:
        for children in self.findChildren(QWidget):
            children.close()
        super().closeEvent(event)
