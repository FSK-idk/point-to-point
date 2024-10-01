from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget

from core.widget.game.game_widget_ui import GameWidgetUI


class GameWidget(QObject):
    textChanged: Signal = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__()

        self.ui: GameWidgetUI = GameWidgetUI(parent)
        
        self.ui.this_input_line.textChanged.connect(self.textChanged)

        self.ui.show()

