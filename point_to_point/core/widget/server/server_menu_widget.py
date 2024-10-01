from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget

from core.widget.server.server_menu_widget_ui import ServerMenuWidgetUI


class ServerMenuWidget(QObject):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__()

        self.ui: ServerMenuWidgetUI = ServerMenuWidgetUI(parent)

        self.ui.show()

