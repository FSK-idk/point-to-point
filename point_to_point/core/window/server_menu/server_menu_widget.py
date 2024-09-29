import threading
import socket
import time

from PySide6.QtCore import QObject

from core.config.config import config
from core.connection.messages import Messages
from core.window.server_menu.server_menu_widget_ui import ServerMenuWidgetUI


class ServerMenuWidget(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.ui: ServerMenuWidgetUI = ServerMenuWidgetUI()

        self.ui.open_connection_button.clicked.connect(self.openConnection)
        self.ui.disconnect_client_button.clicked.connect(self.disconnectClient)
        self.ui.close_connection_button.clicked.connect(self.closeConnection)
        
        self.host: str = socket.gethostbyname(socket.gethostname())
        self.port: int = 5050
        self.header: int = 64
        self.format: str = "utf-8"

        self.listeing_for_clients: bool = False
        self.client_connected: bool = False

        self.message_list: list[str] = []

        self.ui.show()

    def openConnection(self) -> None:
        if self.listeing_for_clients:
            return

        self.server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))

        self.listening_thread = threading.Thread(target=self.listenConnections)
        self.listening_thread.start()

    def disconnectClient(self) -> None:
        if not self.client_connected:
            return
        self.message_list.append(Messages.disconnect)
        self.client_connected = False

    def closeConnection(self) -> None:
        if not self.listeing_for_clients:
            return

        self.disconnectClient()

        print("[SERVER] Close connection...")
        config["Connection"]["Connection"] = "None"
        self.listeing_for_clients = False

        fake_client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fake_client.connect((self.host, self.port))
        self.listening_thread.join()
        fake_client.close()
        self.server.close()

    def listenConnections(self) -> None:
        print("Open connection...")
        print(f"Host: {self.host}")
        print(f"Port: {self.port}")
        config["Connection"]["Connection"] = "Server"
        self.listeing_for_clients = True

        self.server.listen()
        while self.listeing_for_clients:
            if self.client_connected:
                time.sleep(1)
                continue

            client, address = self.server.accept()
            if not self.listeing_for_clients:
                break

            thread = threading.Thread(target=self.handleClient, args=(client, address))
            thread.start()

    def sendMessage(self, message: str) -> None:
        self.message_list.append(message)

    def handleClient(self, client: socket.socket, address: str) -> None:
        print(f"[SERVER] Client connection: {address}")
        config["Connection"]["Connected"] = "True"
        self.client_connected = True
        self.message_list = []

        while self.client_connected:
            # receive
            message_length = client.recv(self.header).decode(self.format)
            if not message_length:
                continue
            message_length = int(message_length)
            message = client.recv(message_length).decode(self.format)

            print(f"[SERVER] Message received \"{message}\"")

            if message == Messages.disconnect:
                message = Messages.disconnect
                print(f"[SERVER] Message sent \"{message}\"")
                message = message.encode(self.format)
                message_length = len(message)
                send_length: bytes = str(message_length).encode(self.format)
                send_length += b" " * (self.header - len(send_length))
                client.send(send_length)
                client.send(message)
                self.client_connected = False
                break

            # sending
            if not self.message_list:
                self.message_list.append(Messages.nothing)

            message = self.message_list[0]
            self.message_list = self.message_list[1::]

            print(f"[SERVER] Message sent \"{message}\"")

            message = message.encode(self.format)
            message_length = len(message)
            send_length: bytes = str(message_length).encode(self.format)
            send_length += b" " * (self.header - len(send_length))
            client.send(send_length)
            client.send(message)


        print("[SERVER] Client disconnection...")
        config["Connection"]["Connected"] = "False"
        self.client_connected = False

        client.close()
