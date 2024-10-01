from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget

from core.widget.game.waiting_widget_ui import WaitingWidgetUI


class WaitingWidget(QObject):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__()

        self.ui: WaitingWidgetUI = WaitingWidgetUI(parent)

        self.ui.show()
