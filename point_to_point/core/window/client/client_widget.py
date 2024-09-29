import threading
import socket

from PySide6.QtCore import QObject, Slot, Signal

from core.config.config import config
from core.connection.messages import Messages
from core.window.client.client_widget_ui import ClientWidgetUI


class ClientWidget(QObject):
    back_to_main_menu: Signal = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.ui: ClientWidgetUI = ClientWidgetUI()

        self.ui.client_menu.ui.play_button.clicked.connect(self.openWaiting)
        self.ui.client_menu.ui.back_button.clicked.connect(self.backToMainMenu)
        self.ui.waiting.ui.back_button.clicked.connect(self.openClientMenu)
        self.ui.game_layout.ui.back_button.clicked.connect(self.openClientMenu)

        self.ui.game_layout.text_changed.connect(self.onTextChanged)

        self.ui.client_menu.ui.connect_to_server_button.clicked.connect(self.connectToServer)
        self.ui.client_menu.ui.disconnect_from_server_button.clicked.connect(self.disconnectFromServer)

        self.connected_to_server: bool = False

        self.server_is_ready: bool = False
        self.client_is_ready: bool = False

        self.message_list: list[tuple[str, bytes | None]] = []

        self.ui.show()

    @Slot()
    def openClientMenu(self) -> None:
        self.client_is_ready = False
        self.sendMessage(Messages.not_ready)
        self.ui.current_widget = "client_menu"
        self.ui.main_layout.setCurrentIndex(0)

    @Slot()
    def openWaiting(self) -> None:
        if not self.connected_to_server:
            return
        self.client_is_ready = True
        self.sendMessage(Messages.ready)
        if self.server_is_ready:
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
        self.message_list.append((Messages.disconnect, None))

    @Slot()
    def handleServer(self) -> None:
        print("[CLIENT] Connected")
        self.connected_to_server = True
        self.message_list = []

        while self.connected_to_server:
            # sending
            if not self.message_list:
                self.message_list.append((Messages.nothing, None))

            message, data = self.message_list[0]
            self.message_list = self.message_list[1::]

            print(f"[CLIENT] Message sent \"{message}\"")

            message_encoded = message.encode(Messages.format)
            message_length = len(message_encoded)
            send_length: bytes = str(message_length).encode(Messages.format)
            send_length += b" " * (Messages.header - len(send_length))
            self.client.send(send_length)
            self.client.send(message_encoded)
            if message == Messages.text_changed:
                if data is None:
                    data = "None".encode(Messages.format)
                data_length = len(data)
                send_length: bytes = str(data_length).encode(Messages.format)
                send_length += b" " * (Messages.header - len(send_length))
                self.client.send(send_length)
                self.client.send(data)

            # receiving
            message_length = self.client.recv(Messages.header).decode(Messages.format)
            if not message_length:
                continue
            message_length = int(message_length)

            message = self.client.recv(message_length).decode(Messages.format)
            if message == Messages.disconnect:
                self.connected_to_server = False
            if message == Messages.ready:
                self.server_is_ready = True
                if self.client_is_ready:
                    self.openGameLayout()
                    self.sendMessage(Messages.start)
            if message == Messages.not_ready:
                self.server_is_ready = False
                if self.ui.current_widget == "game_layout":
                    self.openClientMenu()
                    self.sendMessage(Messages.not_ready)
            if message == Messages.start:
                self.openGameLayout()
            if message == Messages.text_changed:
                data_length = self.client.recv(Messages.header).decode(Messages.format)
                data_length = int(data_length)
                data = self.client.recv(data_length).decode(Messages.format)
                self.ui.game_layout.ui.other_input_line.setText(data)
            # if message == Messages.finished:
            #     self.server_is_ready = False
            #     self.openClientMenu()

            print(f"[CLIENT] Message received \"{message}\"")

        print("[CLIENT] Close connection...")
        self.connected_to_server = False

    def backToMainMenu(self) -> None:
        if self.connected_to_server:
            self.disconnectFromServer()
        self.back_to_main_menu.emit()

    def onTextChanged(self, text: str) -> None:
        self.sendMessage(Messages.text_changed, text.encode(Messages.format))

