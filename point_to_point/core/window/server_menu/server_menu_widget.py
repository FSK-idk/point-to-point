import threading
import socket
import time

from PySide6.QtCore import QObject

from core.window.server_menu.server_menu_widget_ui import ServerMenuWidgetUI


class ServerMenuWidget(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.ui: ServerMenuWidgetUI = ServerMenuWidgetUI()

        self.ui.open_connection_button.clicked.connect(self.openConnection)
        self.ui.close_connection_button.clicked.connect(self.closeConnection)
        
        self.host: str = socket.gethostbyname(socket.gethostname())
        self.port: int = 5050
        self.header: int = 64
        self.format: str = "utf-8"
        self.disconnection_message: str = "disconnect"

        self.listeing_for_clients: bool = False
        self.client_connected: bool = False

        self.ui.show()

    def openConnection(self) -> None:
        if self.listeing_for_clients:
            return

        print("Open connection...")
        print(f"Host: {self.host}")
        print(f"Port: {self.port}")

        self.server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))

        self.listeing_for_clients = True

        self.listening_thread = threading.Thread(target=self.listenConnections)
        self.listening_thread.start()

    def disconnectClient(self) -> None:
        if not self.client_connected:
            return

        print("Disconnect client...")
        self.client_connected = False

    def closeConnection(self) -> None:
        if not self.listeing_for_clients:
            return

        self.disconnectClient()

        print("Close connection...")

        self.listeing_for_clients = False
        fake_client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fake_client.connect((self.host, self.port))
        self.listening_thread.join()
        fake_client.close()
        self.server.close()

    def listenConnections(self) -> None:
        self.server.listen()
        while self.listeing_for_clients:
            if self.client_connected:
                time.sleep(1)
                continue

            client, address = self.server.accept()
            if not self.listeing_for_clients:
                break

            self.client_connected = True
            thread = threading.Thread(target=self.handleClient, args=(client, address))
            thread.start()

    def handleClient(self, client: socket.socket, address: str) -> None:
        print(f"Client connection: {address}")
        while self.client_connected:
            message_length = client.recv(self.header).decode(self.format)
            if not message_length:
                continue

            message_length = int(message_length)

            message: str = client.recv(message_length).decode(self.format)
            if message == self.disconnection_message:
                self.client_connected = False

            print(f"{address}: {message} {self.disconnection_message} {message == self.disconnection_message}")

        self.client_connected = False
        print("Client disconnection...")
        client.close()
