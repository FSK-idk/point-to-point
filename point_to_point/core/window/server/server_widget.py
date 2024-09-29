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

        self.ui.server_menu.ui.play_button.clicked.connect(self.openWaiting)
        self.ui.server_menu.ui.back_button.clicked.connect(self.backToMainMenu)
        self.ui.waiting.ui.back_button.clicked.connect(self.openServerMenu)
        self.ui.game_layout.ui.back_button.clicked.connect(self.openServerMenu)

        self.ui.game_layout.text_changed.connect(self.onTextChanged)

        self.ui.server_menu.ui.open_connection_button.clicked.connect(self.openConnection)
        self.ui.server_menu.ui.disconnect_client_button.clicked.connect(self.disconnectClient)
        self.ui.server_menu.ui.close_connection_button.clicked.connect(self.closeConnection)

        self.host: str = socket.gethostbyname(socket.gethostname())
        self.port: int = 5050

        self.listeing_to_clients: bool = False
        self.client_connected: bool = False

        self.server_is_ready: bool = False
        self.client_is_ready: bool = False

        self.message_list: list[tuple[str, bytes | None]] = []

        self.ui.show()

    @Slot()
    def openServerMenu(self) -> None:
        self.server_is_ready = False
        self.sendMessage(Messages.not_ready)
        self.ui.current_widget = "server_menu"
        self.ui.main_layout.setCurrentIndex(0)

    @Slot()
    def openWaiting(self) -> None:
        if not self.listeing_to_clients:
            return
        self.server_is_ready = True
        self.sendMessage(Messages.ready)
        if self.client_is_ready:
            self.openGameLayout()
            self.sendMessage(Messages.start)
        self.ui.current_widget = "waiting"
        self.ui.main_layout.setCurrentIndex(1)

    @Slot()
    def openGameLayout(self) -> None:
        self.ui.current_widget = "game_layout"
        self.ui.main_layout.setCurrentIndex(2)

    @Slot()
    def sendMessage(self, message: str, data: bytes | None = None) -> None:
        self.message_list.append((message, data))

    @Slot()
    def openConnection(self) -> None:
        if self.listeing_to_clients:
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

        self.message_list.append((Messages.disconnect, None))

    @Slot()
    def closeConnection(self) -> None:
        if not self.listeing_to_clients:
            return

        self.disconnectClient()

        print("[SERVER] Close connection...")
        self.listeing_to_clients = False

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
        self.listeing_to_clients = True

        self.server.listen()
        while self.listeing_to_clients:
            if self.client_connected:
                time.sleep(1)
                continue

            client, address = self.server.accept()
            if not self.listeing_to_clients:
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
            if message == Messages.ready:
                self.client_is_ready = True
                if self.server_is_ready:
                    self.openGameLayout()
                    self.sendMessage(Messages.start)
            if message == Messages.not_ready:
                self.client_is_ready = False
                if self.ui.current_widget == "game_layout":
                    self.openServerMenu()
                    self.sendMessage(Messages.not_ready)
            if message == Messages.start:
                self.openGameLayout()
            if message == Messages.text_changed:
                data_length = client.recv(Messages.header).decode(Messages.format)
                data_length = int(data_length)
                data = client.recv(data_length).decode(Messages.format)
                self.ui.game_layout.ui.other_input_line.setText(data)
            # if message == Messages.finished:
            #     self.client_is_ready = False
            #     self.openServerMenu()

            # sending
            if not self.message_list:
                self.message_list.append((Messages.nothing, None))

            message, data = self.message_list[0]
            self.message_list = self.message_list[1::]

            print(f"[SERVER] Message sent \"{message}\"")

            message_encoded = message.encode(Messages.format)
            message_length = len(message_encoded)
            send_length: bytes = str(message_length).encode(Messages.format)
            send_length += b" " * (Messages.header - len(send_length))
            client.send(send_length)
            client.send(message_encoded)
            if message == Messages.text_changed:
                if data is None:
                    data = "None".encode(Messages.format)
                data_length = len(data)
                send_length: bytes = str(data_length).encode(Messages.format)
                send_length += b" " * (Messages.header - len(send_length))
                client.send(send_length)
                client.send(data)

        client.close()

    def backToMainMenu(self) -> None:
        if self.listeing_to_clients:
            self.closeConnection()
        self.back_to_main_menu.emit()

    def onTextChanged(self, text: str) -> None:
        self.sendMessage(Messages.text_changed, text.encode(Messages.format))

