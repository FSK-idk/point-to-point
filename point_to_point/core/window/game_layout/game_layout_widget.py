from PySide6.QtCore import QObject, Signal

from core.window.game_layout.game_layout_widget_ui import GameLayoutWidgetUI


class GameLayoutWidget(QObject):
    text_changed: Signal = Signal(str)

    def __init__(self) -> None:
        super().__init__()

        self.ui: GameLayoutWidgetUI = GameLayoutWidgetUI()
        
        self.ui.this_input_line.textChanged.connect(self.text_changed)

        self.ui.show()

