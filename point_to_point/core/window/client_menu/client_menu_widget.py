import threading
import socket

from PySide6.QtCore import QObject

from core.window.client_menu.client_menu_widget_ui import ClientMenuWidgetUI


class ClientMenuWidget(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.ui: ClientMenuWidgetUI = ClientMenuWidgetUI()

        self.ui.connect_to_server_button.clicked.connect(self.connectToServer)
        self.ui.disconnect_from_server_button.clicked.connect(self.disconnectFromServer)
        
        self.host: str = socket.gethostbyname(socket.gethostname())
        self.port: int = 5050
        self.header: int = 64
        self.format: str = "utf-8"
        self.disconnection_message: str = "disconnect"

        self.connected_to_server: bool = False

        self.ui.show()

    def connectToServer(self) -> None:
        if self.connected_to_server:
            return

        print("Open connection...")

        self.connected_to_server = True

        self.client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client.connect((self.ui.host_line_edit.text(), int(self.ui.port_line_edit.text())))

    def disconnectFromServer(self) -> None:
        if not self.connected_to_server:
            return

        print("Close connection...")

        self.connected_to_server = False

        self.sendMessage(self.disconnection_message)

    def sendMessage(self, message: str) -> None:
        message_length: int = len(message.encode(self.format))
        send_length: bytes = str(message_length).encode(self.format)
        send_length += b" " * (self.header - len(send_length))
        self.client.send(send_length)
        self.client.send(message.encode(self.format))
