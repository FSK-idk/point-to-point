from PySide6.QtCore import QObject, Signal

from core.window.game.game_widget_ui import GameWidgetUI


class GameWidget(QObject):
    textChanged: Signal = Signal(str)

    def __init__(self) -> None:
        super().__init__()

        self.ui: GameWidgetUI = GameWidgetUI()
        
        self.ui.this_input_line.textChanged.connect(self.textChanged)

        self.ui.show()

