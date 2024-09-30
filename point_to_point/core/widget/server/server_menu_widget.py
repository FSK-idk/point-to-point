from PySide6.QtCore import QObject

from core.widget.server.server_menu_widget_ui import ServerMenuWidgetUI


class ServerMenuWidget(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.ui: ServerMenuWidgetUI = ServerMenuWidgetUI()

        self.ui.show()

