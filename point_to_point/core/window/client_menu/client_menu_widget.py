import threading
import socket

from PySide6.QtCore import QObject

from core.config.config import config
from core.connection.messages import Messages
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

        self.connected_to_server: bool = False

        self.message_list: list[str] = []

        self.ui.show()

    def connectToServer(self) -> None:
        if self.connected_to_server:
            return

        try:
            print("[CLIENT] Open connection...")
            config["Connection"]["Connection"] = "Client"
            self.client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.settimeout(2)
            self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.client.connect((self.ui.host_line_edit.text(), int(self.ui.port_line_edit.text())))

        except:
            print("[CLIENT] Failed connection")
            config["Connection"]["Connection"] = "None"
            self.client.close()
            return

        self.sending_thread = threading.Thread(target=self.handleServer)
        self.sending_thread.start()


    def disconnectFromServer(self) -> None:
        if not self.connected_to_server:
            return

        print("[CLIENT] Close connection...")
        config["Connection"]["Connection"] = "None"
        self.message_list.append(Messages.disconnect)

    def sendMessage(self, message: str) -> None:
        self.message_list.append(message)

    def handleServer(self) -> None:
        config["Connection"]["Connected"] = "True"
        self.connected_to_server = True
        self.message_list = []

        while self.connected_to_server:
            # sending
            if not self.message_list:
                self.message_list.append(Messages.nothing)

            message = self.message_list[0]
            self.message_list = self.message_list[1::]

            print(f"[CLIENT] Message sent \"{message}\"")

            message = message.encode(self.format)
            message_length = len(message)
            send_length: bytes = str(message_length).encode(self.format)
            send_length += b" " * (self.header - len(send_length))
            self.client.send(send_length)
            self.client.send(message)

            # receiving
            message_length = self.client.recv(self.header).decode(self.format)
            if not message_length:
                continue
            message_length = int(message_length)

            message = self.client.recv(message_length).decode(self.format)
            if message == Messages.disconnect:
                self.connected_to_server = False

            print(f"[CLIENT] Message received \"{message}\"")

        print("[CLIENT] Close connection...")
        config["Connection"]["Connected"] = "False"
        self.connected_to_server = False
