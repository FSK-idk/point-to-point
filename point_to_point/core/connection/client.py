import threading
import socket

from PySide6.QtCore import QObject, Slot, Signal

from core.connection.message import MessageType, Message


class Client(QObject):
    connected: Signal = Signal()
    disconnected: Signal = Signal()

    receivedReady: Signal = Signal()
    receivedNotReady: Signal = Signal()
    receivedStartGame: Signal = Signal()
    receivedSetupText: Signal = Signal(str)
    receivedTextChanged: Signal = Signal(str)
    receivedFinishGame: Signal = Signal()
    receivedInterruptGame: Signal = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.connected_to_server: bool = False

        self.message_list: list[Message] = []

    @Slot()
    def sendMessage(self, type: str, data: bytes | None = None) -> None:
        self.message_list.append(Message(type, data))

    @Slot()
    def connectToServer(self, host: str, port: str) -> None:
        if self.connected_to_server:
            return

        try:
            print("[CLIENT] Open connection...")
            self.client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.settimeout(2)
            self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.client.connect((host, int(port)))

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
        self.sendMessage(MessageType.DISCONNECT)

    def handleServer(self) -> None:
        print("[CLIENT] Connected")
        self.connected.emit()
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
                    print("[CLIENT] Close connection...")
                    self.connected_to_server = False
                    self.disconnected.emit()
                    self.client.close()

                case MessageType.READY:
                    self.receivedReady.emit()

                case MessageType.NOT_READY:
                    self.receivedNotReady.emit()

                case MessageType.START_GAME:
                    self.receivedStartGame.emit()

                case MessageType.SETUP_TEXT:
                    data_length = self.client.recv(Message.HEADER).decode(Message.FORMAT)
                    data_length = int(data_length)
                    data = self.client.recv(data_length).decode(Message.FORMAT)
                    self.receivedSetupText.emit(data)

                case MessageType.TEXT_CHANGED:
                    data_length = self.client.recv(Message.HEADER).decode(Message.FORMAT)
                    data_length = int(data_length)
                    data = self.client.recv(data_length).decode(Message.FORMAT)
                    self.receivedTextChanged.emit(data)

                case MessageType.FINISH_GAME:
                    self.receivedFinishGame.emit()

                case MessageType.INTERRUPT_GAME:
                    self.receivedInterruptGame.emit()

            print(f"[CLIENT] Message received \"{type}\"")

