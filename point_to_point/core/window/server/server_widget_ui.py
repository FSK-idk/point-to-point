from PySide6.QtWidgets import QWidget, QStackedLayout

from core.window.server.server_menu_widget import ServerMenuWidget
from core.window.game_layout.waiting_widget import WaitingWidget
from core.window.game_layout.game_layout_widget import GameLayoutWidget


class ServerWidgetUI(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setGeometry(0, 0, 1000, 600)
        self.setMinimumSize(400, 300)

        self.server_menu: ServerMenuWidget = ServerMenuWidget()
        self.waiting: WaitingWidget = WaitingWidget()
        self.game_layout: GameLayoutWidget = GameLayoutWidget()

        self.main_layout: QStackedLayout = QStackedLayout()
        self.main_layout.addWidget(self.server_menu.ui)
        self.main_layout.addWidget(self.waiting.ui)
        self.main_layout.addWidget(self.game_layout.ui)

        self.current_widget: str = "server_menu"
        self.main_layout.setCurrentIndex(0)

        self.setLayout(self.main_layout)
