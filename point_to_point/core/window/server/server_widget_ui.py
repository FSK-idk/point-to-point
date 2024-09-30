from PySide6.QtWidgets import QWidget, QStackedLayout

from core.window.server.server_menu_widget import ServerMenuWidget
from core.window.server.settings_widget import SettingsWidget
from core.window.game.waiting_widget import WaitingWidget
from core.window.game.game_widget import GameWidget
from core.window.game.score_widget import ScoreWidget


class ServerWidgetUI(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setGeometry(0, 0, 1000, 600)
        self.setMinimumSize(400, 300)

        self.server_menu: ServerMenuWidget = ServerMenuWidget()
        self.settings: SettingsWidget = SettingsWidget()
        self.waiting: WaitingWidget = WaitingWidget()
        self.game: GameWidget = GameWidget()
        self.score: ScoreWidget = ScoreWidget()

        self.main_layout: QStackedLayout = QStackedLayout()
        self.main_layout.addWidget(self.server_menu.ui)
        self.SERVER_MENU_INDEX = 0
        self.main_layout.addWidget(self.settings.ui)
        self.SETTINGS_MENU_INDEX = 1
        self.main_layout.addWidget(self.waiting.ui)
        self.WAITING_INDEX = 2
        self.main_layout.addWidget(self.game.ui)
        self.GAME_INDEX = 3
        self.main_layout.addWidget(self.score.ui)
        self.SCORE_INDEX = 4

        self.setLayout(self.main_layout)
