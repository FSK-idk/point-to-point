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

        self.ui.client_menu.ui.play_button.clicked.connect(self.openGameLayout)
        self.ui.client_menu.ui.back_button.clicked.connect(self.backToMainMenu)
        self.ui.game_layout.ui.back_button.clicked.connect(self.openClientMenu)

        self.ui.client_menu.ui.connect_to_server_button.clicked.connect(self.connectToServer)
        self.ui.client_menu.ui.disconnect_from_server_button.clicked.connect(self.disconnectFromServer)

        self.connected_to_server: bool = False

        self.message_list: list[str] = []

        self.ui.show()

    @Slot()
    def openClientMenu(self) -> None:
        self.ui.main_layout.setCurrentIndex(0)

    @Slot()
    def openGameLayout(self) -> None:
        if not self.connected_to_server:
            return
        self.ui.main_layout.setCurrentIndex(1)

    @Slot()
    def sendMessage(self, message: str) -> None:
        self.message_list.append(message)

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
        self.message_list.append(Messages.disconnect)

    @Slot()
    def handleServer(self) -> None:
        print("[CLIENT] Connected")
        self.connected_to_server = True
        self.message_list = []

        while self.connected_to_server:
            # sending
            if not self.message_list:
                self.message_list.append(Messages.nothing)

            message = self.message_list[0]
            self.message_list = self.message_list[1::]

            print(f"[CLIENT] Message sent \"{message}\"")

            message = message.encode(Messages.format)
            message_length = len(message)
            send_length: bytes = str(message_length).encode(Messages.format)
            send_length += b" " * (Messages.header - len(send_length))
            self.client.send(send_length)
            self.client.send(message)

            # receiving
            message_length = self.client.recv(Messages.header).decode(Messages.format)
            if not message_length:
                continue
            message_length = int(message_length)

            message = self.client.recv(message_length).decode(Messages.format)
            if message == Messages.disconnect:
                self.connected_to_server = False

            print(f"[CLIENT] Message received \"{message}\"")

        print("[CLIENT] Close connection...")
        self.connected_to_server = False

    def backToMainMenu(self) -> None:
        if self.connected_to_server:
            self.disconnectFromServer()
        self.back_to_main_menu.emit()
