from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QStackedLayout
from PySide6.QtGui import QCloseEvent

from core.widget.client.client_menu_widget import ClientMenuWidget
from core.widget.game.waiting_widget import WaitingWidget
from core.widget.game.game_widget import GameWidget
from core.widget.game.score_widget import ScoreWidget


class ClientWidgetUI(QWidget):
    closeUI: Signal = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setGeometry(0, 0, 1000, 600)
        self.setMinimumSize(400, 300)

        self.client_menu: ClientMenuWidget = ClientMenuWidget(self)
        self.waiting: WaitingWidget = WaitingWidget(self)
        self.game: GameWidget = GameWidget(self)
        self.score: ScoreWidget = ScoreWidget(self)

        self.main_layout: QStackedLayout = QStackedLayout()
        self.main_layout.addWidget(self.client_menu.ui)
        self.CLIENT_MENU_INDEX = 0
        self.main_layout.addWidget(self.waiting.ui)
        self.WAITING_INDEX = 1
        self.main_layout.addWidget(self.game.ui)
        self.GAME_INDEX = 2
        self.main_layout.addWidget(self.score.ui)
        self.SCORE_INDEX = 3

        self.setLayout(self.main_layout)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.closeUI.emit()
        super().closeEvent(event)
