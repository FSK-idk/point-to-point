from PySide6.QtCore import QObject

from core.window.game.waiting_widget_ui import WaitingWidgetUI


class WaitingWidget(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.ui: WaitingWidgetUI = WaitingWidgetUI()

        self.ui.show()
