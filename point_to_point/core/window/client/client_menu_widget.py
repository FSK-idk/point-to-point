import threading
import socket

from PySide6.QtCore import QObject

from core.config.config import config
from core.connection.messages import Messages
from core.window.client.client_menu_widget_ui import ClientMenuWidgetUI


class ClientMenuWidget(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.ui: ClientMenuWidgetUI = ClientMenuWidgetUI()

        self.ui.show()
