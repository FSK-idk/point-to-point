import threading
import socket
import time

from PySide6.QtCore import QObject, Slot, Signal

from core.config.config import config
from core.connection.messages import Messages
from core.window.server.server_widget_ui import ServerWidgetUI


class ServerWidget(QObject):
    back_to_main_menu: Signal = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.ui: ServerWidgetUI = ServerWidgetUI()

        self.ui.server_menu.ui.play_button.clicked.connect(self.openGameLayout)
        self.ui.server_menu.ui.back_button.clicked.connect(self.backToMainMenu)
        self.ui.game_layout.ui.back_button.clicked.connect(self.openServerMenu)

        self.ui.server_menu.ui.open_connection_button.clicked.connect(self.openConnection)
        self.ui.server_menu.ui.disconnect_client_button.clicked.connect(self.disconnectClient)
        self.ui.server_menu.ui.close_connection_button.clicked.connect(self.closeConnection)

        self.host: str = socket.gethostbyname(socket.gethostname())
        self.port: int = 5050

        self.listeing_for_clients: bool = False
        self.client_connected: bool = False

        self.message_list: list[str] = []

        self.ui.show()

    @Slot()
    def openServerMenu(self) -> None:
        self.ui.main_layout.setCurrentIndex(0)

    @Slot()
    def openGameLayout(self) -> None:
        if not self.client_connected:
            return
        self.ui.main_layout.setCurrentIndex(1)

    @Slot()
    def sendMessage(self, message: str) -> None:
        self.message_list.append(message)

    @Slot()
    def openConnection(self) -> None:
        if self.listeing_for_clients:
            return

        self.server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))

        self.listening_thread = threading.Thread(target=self.listenConnections)
        self.listening_thread.start()

    @Slot()
    def disconnectClient(self) -> None:
        if not self.client_connected:
            return

        print("[SERVER] Client disconnection...")
        self.client_connected = False

        self.message_list.append(Messages.disconnect)

    @Slot()
    def closeConnection(self) -> None:
        if not self.listeing_for_clients:
            return

        self.disconnectClient()

        print("[SERVER] Close connection...")
        self.listeing_for_clients = False

        fake_client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fake_client.connect((self.host, self.port))
        self.listening_thread.join()
        fake_client.close()

        self.server.close()

    @Slot()
    def listenConnections(self) -> None:
        print("Open connection...")
        print(f"Host: {self.host}")
        print(f"Port: {self.port}")
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

    @Slot()
    def handleClient(self, client: socket.socket, address: str) -> None:
        print(f"[SERVER] Client connection: {address}")
        self.client_connected = True
        self.message_list = []

        while self.client_connected:
            # receive
            message_length = client.recv(Messages.header).decode(Messages.format)
            if not message_length:
                continue
            message_length = int(message_length)
            message = client.recv(message_length).decode(Messages.format)

            print(f"[SERVER] Message received \"{message}\"")

            if message == Messages.disconnect:
                self.disconnectClient()

            # sending
            if not self.message_list:
                self.message_list.append(Messages.nothing)

            message = self.message_list[0]
            self.message_list = self.message_list[1::]

            print(f"[SERVER] Message sent \"{message}\"")

            message = message.encode(Messages.format)
            message_length = len(message)
            send_length: bytes = str(message_length).encode(Messages.format)
            send_length += b" " * (Messages.header - len(send_length))
            client.send(send_length)
            client.send(message)

        client.close()

    def backToMainMenu(self) -> None:
        if self.listeing_for_clients:
            self.closeConnection()
        self.back_to_main_menu.emit()
