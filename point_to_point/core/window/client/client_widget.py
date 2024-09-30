import threading
import socket

from PySide6.QtCore import QObject, Slot, Signal

from core.connection.messages import MessageType, Message
from core.window.client.client_widget_ui import ClientWidgetUI


class ClientWidget(QObject):
    backToMainMenu: Signal = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.ui: ClientWidgetUI = ClientWidgetUI()

        self.ui.main_layout.setCurrentIndex(self.ui.CLIENT_MENU_INDEX)

        self.ui.client_menu.ui.connect_to_server_button.clicked.connect(self.connectToServer)
        self.ui.client_menu.ui.disconnect_from_server_button.clicked.connect(self.disconnectFromServer)
        self.ui.client_menu.ui.play_button.clicked.connect(self.openWaiting)
        self.ui.client_menu.ui.back_button.clicked.connect(self.onClientMenuBack)

        self.ui.waiting.ui.back_button.clicked.connect(self.openClientMenu)

        self.ui.game.ui.back_button.clicked.connect(self.openClientMenu)
        self.ui.game.textChanged.connect(self.onTextChanged)

        self.ui.score.ui.back_button.clicked.connect(self.openClientMenu)

        self.connected_to_server: bool = False

        self.server_is_ready: bool = False
        self.client_is_ready: bool = False

        self.message_list: list[Message] = []

        self.ui.show()

    @Slot()
    def openClientMenu(self) -> None:
        self.client_is_ready = False
        self.sendMessage(MessageType.NOT_READY)

        match self.ui.main_layout.currentIndex():
            case self.ui.GAME_INDEX:
                self.sendMessage(MessageType.INTERRUPT_GAME)

        self.ui.main_layout.setCurrentIndex(self.ui.CLIENT_MENU_INDEX)

    @Slot()
    def openWaiting(self) -> None:
        if not self.connected_to_server:
            return

        self.client_is_ready = True
        self.sendMessage(MessageType.READY)

        if self.server_is_ready:
            self.sendMessage(MessageType.START_GAME)
            self.openGame()

        self.ui.main_layout.setCurrentIndex(self.ui.WAITING_INDEX)

    @Slot()
    def openGame(self) -> None:
        self.ui.main_layout.setCurrentIndex(self.ui.GAME_INDEX)

    @Slot()
    def openScore(self) -> None:
        self.client_is_ready = False
        self.sendMessage(MessageType.NOT_READY)

        self.ui.main_layout.setCurrentIndex(self.ui.SCORE_INDEX)

    @Slot()
    def sendMessage(self, type: str, data: bytes | None = None) -> None:
        self.message_list.append(Message(type, data))

    @Slot()
    def connectToServer(self) -> None:
        if self.connected_to_server:
            return

        try:
            print("[CLIENT] Open connection...")
            self.client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.settimeout(2)
            self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.client.connect((self.ui.client_menu.ui.host_line_edit.text(), int(self.ui.client_menu.ui.port_line_edit.text())))

        except:
            print("[CLIENT] Failed connection")
            self.client.close()
            return

        self.sending_thread = threading.Thread(target=self.handleServer)
        self.sending_thread.start()

    @Slot()
    def disconnectFromServer(self) -> None:
        if not self.connected_to_server:
            return

        print("[CLIENT] Close connection...")
        self.sendMessage(MessageType.DISCONNECT)

    def handleServer(self) -> None:
        print("[CLIENT] Connected")
        self.ui.client_menu.ui.connection_label.setText("Connection is open")
        self.connected_to_server = True
        self.message_list = []

        while self.connected_to_server:
            # sending
            if not self.message_list:
                self.sendMessage(MessageType.NOTHING)

            message = self.message_list[0]
            self.message_list = self.message_list[1::]

            type_encoded = message.type.encode(Message.FORMAT)
            type_length = len(type_encoded)
            send_length: bytes = str(type_length).encode(Message.FORMAT)
            send_length += b" " * (Message.HEADER - len(send_length))
            self.client.send(send_length)
            self.client.send(type_encoded)

            if message.type in [MessageType.TEXT_CHANGED]:
                data_length = len(message.data)
                send_length: bytes = str(data_length).encode(Message.FORMAT)
                send_length += b" " * (Message.HEADER - len(send_length))
                self.client.send(send_length)
                self.client.send(message.data)

            print(f"[CLIENT] Message sent \"{message.type}\"")

            # receiving
            type_length = self.client.recv(Message.HEADER).decode(Message.FORMAT)
            if not type_length:
                continue
            type_length = int(type_length)
            type = self.client.recv(type_length).decode(Message.FORMAT)

            match type:
                case MessageType.DISCONNECT:
                    self.connected_to_server = False

                case MessageType.READY:
                    self.server_is_ready = True
                    if self.client_is_ready:
                        self.openGame()
                        self.sendMessage(MessageType.START_GAME)

                case MessageType.NOT_READY:
                    self.server_is_ready = False

                case MessageType.START_GAME:
                    self.openGame()

                case MessageType.SETUP_TEXT:
                    data_length = self.client.recv(Message.HEADER).decode(Message.FORMAT)
                    data_length = int(data_length)
                    data = self.client.recv(data_length).decode(Message.FORMAT)
                    self.ui.game.ui.this_input_line.setText(data)
                    self.ui.game.ui.other_input_line.setText(data)

                case MessageType.TEXT_CHANGED:
                    data_length = self.client.recv(Message.HEADER).decode(Message.FORMAT)
                    data_length = int(data_length)
                    data = self.client.recv(data_length).decode(Message.FORMAT)
                    self.ui.game.ui.other_input_line.setText(data)

                case MessageType.FINISH_GAME:
                    self.ui.score.setScoreText("Opponent won")
                    self.openScore()

                case MessageType.INTERRUPT_GAME:
                    self.ui.score.setScoreText("Opponent interrupted the game")
                    self.openScore()

            print(f"[CLIENT] Message received \"{type}\"")

        print("[CLIENT] Close connection...")
        self.ui.client_menu.ui.connection_label.setText("Connection is closed")

    @Slot()
    def onClientMenuBack(self) -> None:
        if self.connected_to_server:
            self.disconnectFromServer()
        self.backToMainMenu.emit()

    @Slot()
    def onTextChanged(self, text: str) -> None:
        self.sendMessage(MessageType.TEXT_CHANGED, text.encode(Message.FORMAT))
        if not text:
            self.ui.score.setScoreText("You won")
            self.sendMessage(MessageType.FINISH_GAME)
            self.openScore()
