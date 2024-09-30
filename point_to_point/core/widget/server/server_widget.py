import threading
import socket

from PySide6.QtCore import QObject, Slot, Signal

from core.config.config import config
from core.connection.message import MessageType, Message
from core.widget.server.server_widget_ui import ServerWidgetUI


class ServerWidget(QObject):
    backToMainMenu: Signal = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.ui: ServerWidgetUI = ServerWidgetUI()

        self.ui.main_layout.setCurrentIndex(self.ui.SERVER_MENU_INDEX)

        self.ui.server_menu.ui.open_connection_button.clicked.connect(self.openConnection)
        self.ui.server_menu.ui.disconnect_client_button.clicked.connect(self.disconnectClient)
        self.ui.server_menu.ui.close_connection_button.clicked.connect(self.closeConnection)
        self.ui.server_menu.ui.settings_button.clicked.connect(self.openSettings)
        self.ui.server_menu.ui.play_button.clicked.connect(self.openWaiting)
        self.ui.server_menu.ui.back_button.clicked.connect(self.onServerMenuBack)

        self.ui.settings.ui.back_button.clicked.connect(self.openServerMenu)

        self.ui.waiting.ui.back_button.clicked.connect(self.openServerMenu)

        self.ui.game.ui.back_button.clicked.connect(self.openServerMenu)
        self.ui.game.textChanged.connect(self.onTextChanged)

        self.ui.score.ui.back_button.clicked.connect(self.openServerMenu)

        self.host: str = socket.gethostbyname(socket.gethostname() + ".")
        self.port: int = 5050

        self.ui.server_menu.ui.host_label.setText(f"host: {self.host}, port: {self.port}")

        self.listeing_to_clients: bool = False
        self.client_connected: bool = False

        self.server_is_ready: bool = False
        self.client_is_ready: bool = False

        self.message_list: list[Message] = []

        self.ui.show()

    @Slot()
    def openServerMenu(self) -> None:
        self.server_is_ready = False
        self.sendMessage(MessageType.NOT_READY)

        match self.ui.main_layout.currentIndex():
            case self.ui.SETTINGS_MENU_INDEX:
                config["Settings"]["text"] = self.ui.settings.ui.text_edit.toPlainText()

            case self.ui.GAME_INDEX:
                self.sendMessage(MessageType.INTERRUPT_GAME)

        self.ui.main_layout.setCurrentIndex(self.ui.SERVER_MENU_INDEX)

    @Slot()
    def openSettings(self) -> None:
        self.ui.settings.ui.text_edit.setText(config["Settings"]["text"])
        self.ui.main_layout.setCurrentIndex(self.ui.SETTINGS_MENU_INDEX)

    @Slot()
    def openWaiting(self) -> None:
        if not self.listeing_to_clients:
            return

        self.server_is_ready = True
        self.sendMessage(MessageType.READY)

        if self.client_is_ready:
            self.sendMessage(MessageType.START_GAME)
            self.openGame()

        self.ui.main_layout.setCurrentIndex(self.ui.WAITING_INDEX)

    @Slot()
    def openGame(self) -> None:
        text = config["Settings"]["text"]
        self.ui.game.ui.this_input_line.setText(text)
        self.ui.game.ui.other_input_line.setText(text)
        self.sendMessage(MessageType.SETUP_TEXT, text.encode(Message.FORMAT))
        self.ui.game.ui.this_input_line.setFocus()
        self.ui.main_layout.setCurrentIndex(self.ui.GAME_INDEX)

    @Slot()
    def openScore(self) -> None:
        self.server_is_ready = False
        self.sendMessage(MessageType.NOT_READY)

        self.ui.main_layout.setCurrentIndex(self.ui.SCORE_INDEX)

    @Slot()
    def sendMessage(self, type: str, data: bytes | None = None) -> None:
        self.message_list.append(Message(type, data))

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
        self.ui.server_menu.ui.client_label.setText("Client is disconnected")
        self.client_connected = False

        self.sendMessage(MessageType.DISCONNECT)

    @Slot()
    def closeConnection(self) -> None:
        if not self.listeing_to_clients:
            return

        self.disconnectClient()

        print("[SERVER] Close connection...")
        self.ui.server_menu.ui.connection_label.setText("Connection is closed")
        self.listeing_to_clients = False

        fake_client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fake_client.connect((self.host, self.port))
        self.listening_thread.join()
        fake_client.close()

        self.server.close()

    def listenConnections(self) -> None:
        print("Open connection...")
        print(f"Host: {self.host}")
        print(f"Port: {self.port}")
        self.ui.server_menu.ui.connection_label.setText("Connection is open")
        self.listeing_to_clients = True

        self.server.listen()
        while self.listeing_to_clients:
            if self.client_connected:
                continue

            client, address = self.server.accept()
            if not self.listeing_to_clients:
                break

            thread = threading.Thread(target=self.handleClient, args=(client, address))
            thread.start()

    def handleClient(self, client: socket.socket, address: str) -> None:
        print(f"[SERVER] Client connection: {address}")
        self.ui.server_menu.ui.client_label.setText("Client is connected")
        self.client_connected = True
        self.message_list = []

        while self.client_connected:
            # receive
            type_length = client.recv(Message.HEADER).decode(Message.FORMAT)
            if not type_length:
                continue
            type_length = int(type_length)
            type = client.recv(type_length).decode(Message.FORMAT)

            match type:
                case MessageType.DISCONNECT:
                    self.disconnectClient()

                case MessageType.READY:
                    self.client_is_ready = True
                    if self.server_is_ready:
                        self.openGame()
                        self.sendMessage(MessageType.START_GAME)

                case MessageType.NOT_READY:
                    self.client_is_ready = False

                case MessageType.START_GAME:
                    self.openGame()

                case MessageType.TEXT_CHANGED:
                    data_length = client.recv(Message.HEADER).decode(Message.FORMAT)
                    data_length = int(data_length)
                    data = client.recv(data_length).decode(Message.FORMAT)
                    self.ui.game.ui.other_input_line.setText(data)

                case MessageType.FINISH_GAME:
                    self.ui.score.setScoreText("Opponent won")
                    self.openScore()

                case MessageType.INTERRUPT_GAME:
                    self.ui.score.setScoreText("Opponent interrupted the game")
                    self.openScore()

            print(f"[SERVER] Message received \"{type}\"")

            # sending
            if not self.message_list:
                self.sendMessage(MessageType.NOTHING)

            message = self.message_list[0]
            self.message_list = self.message_list[1::]

            type_encoded = message.type.encode(Message.FORMAT)
            type_length = len(type_encoded)
            send_length: bytes = str(type_length).encode(Message.FORMAT)
            send_length += b" " * (Message.HEADER - len(send_length))
            client.send(send_length)
            client.send(type_encoded)

            if message.type in [MessageType.SETUP_TEXT, MessageType.TEXT_CHANGED]:
                data_length = len(message.data)
                send_length: bytes = str(data_length).encode(Message.FORMAT)
                send_length += b" " * (Message.HEADER - len(send_length))
                client.send(send_length)
                client.send(message.data)

            print(f"[SERVER] Message sent \"{message.type}\"")

        client.close()

    @Slot()
    def onServerMenuBack(self) -> None:
        if self.listeing_to_clients:
            self.closeConnection()
        self.backToMainMenu.emit()

    @Slot()
    def onTextChanged(self, text: str) -> None:
        self.sendMessage(MessageType.TEXT_CHANGED, text.encode(Message.FORMAT))
        if not text:
            self.ui.score.setScoreText("You won")
            self.sendMessage(MessageType.FINISH_GAME)
            self.openScore()

