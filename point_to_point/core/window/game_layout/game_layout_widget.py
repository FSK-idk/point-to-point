from PySide6.QtCore import QObject

from core.window.game_layout.game_layout_widget_ui import GameLayoutWidgetUI


class GameLayoutWidget(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.ui: GameLayoutWidgetUI = GameLayoutWidgetUI()

        self.ui.show()

