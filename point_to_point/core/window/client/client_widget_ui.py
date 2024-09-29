from PySide6.QtWidgets import QWidget, QStackedLayout

from core.window.client.client_menu_widget import ClientMenuWidget
from core.window.game_layout.game_layout_widget import GameLayoutWidget


class ClientWidgetUI(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setGeometry(0, 0, 1000, 600)
        self.setMinimumSize(400, 300)

        self.client_menu: ClientMenuWidget = ClientMenuWidget()
        self.game_layout: GameLayoutWidget = GameLayoutWidget()

        self.main_layout: QStackedLayout = QStackedLayout()
        self.main_layout.addWidget(self.client_menu.ui)
        self.main_layout.addWidget(self.game_layout.ui)

        self.main_layout.setCurrentIndex(0)

        self.setLayout(self.main_layout)
