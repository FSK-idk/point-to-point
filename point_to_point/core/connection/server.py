import threading
import socket
import time

from PySide6.QtCore import QObject, Slot, Signal

from core.connection.message import MessageType, Message


class Server(QObject):
    clientDisconnected: Signal = Signal()
    clientConnected: Signal = Signal()
    connectionClosed: Signal = Signal()
    connectionOpen: Signal = Signal()

    receivedDisconnect: Signal = Signal()
    receivedReady: Signal = Signal()
    receivedNotReady: Signal = Signal()
    receivedStartGame: Signal = Signal()
    receivedMessageChanged: Signal = Signal(str)
    receivedFinishGame: Signal = Signal()
    receivedInterruptGame: Signal = Signal()


    def __init__(self) -> None:
        super().__init__()

        self.host: str = socket.gethostbyname(socket.gethostname() + ".")
        self.port: int = 5050

        self.listeing_to_clients: bool = False
        self.client_is_connected: bool = False

        self.message_list: list[Message] = []

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
        if not self.client_is_connected:
            return

        self.sendMessage(MessageType.DISCONNECT)

        while self.client_is_connected:
            continue

    @Slot()
    def closeConnection(self) -> None:
        if not self.listeing_to_clients:
            return

        self.disconnectClient()

        print("[SERVER] Close connection...")
        self.connectionClosed.emit()
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
        self.connectionOpen.emit()
        self.listeing_to_clients = True

        self.server.listen()
        while self.listeing_to_clients:
            if self.client_is_connected:
                continue

            self.client, self.address = self.server.accept()
            if not self.listeing_to_clients:
                break

            thread = threading.Thread(target=self.handleClient)
            thread.start()

    def handleClient(self) -> None:
        print(f"[SERVER] Client connection: {self.address}")
        self.clientConnected.emit()
        self.client_is_connected = True
        self.message_list = []

        while self.client_is_connected:
            # receive
            type_length = self.client.recv(Message.HEADER).decode(Message.FORMAT)
            if not type_length:
                continue
            type_length = int(type_length)
            type = self.client.recv(type_length).decode(Message.FORMAT)

            match type:
                case MessageType.DISCONNECT:
                    self.sendMessage(MessageType.DISCONNECT)
                    self.receivedDisconnect.emit()

                case MessageType.READY:
                    self.receivedReady.emit()

                case MessageType.NOT_READY:
                    self.receivedNotReady.emit()

                case MessageType.START_GAME:
                    self.receivedStartGame.emit()

                case MessageType.TEXT_CHANGED:
                    data_length = self.client.recv(Message.HEADER).decode(Message.FORMAT)
                    data_length = int(data_length)
                    data = self.client.recv(data_length).decode(Message.FORMAT)
                    self.receivedMessageChanged.emit(data)

                case MessageType.FINISH_GAME:
                    self.receivedFinishGame.emit()

                case MessageType.INTERRUPT_GAME:
                    self.receivedInterruptGame.emit()

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
            self.client.send(send_length)
            self.client.send(type_encoded)

            if message.type in [MessageType.SETUP_TEXT, MessageType.TEXT_CHANGED]:
                data_length = len(message.data)
                send_length: bytes = str(data_length).encode(Message.FORMAT)
                send_length += b" " * (Message.HEADER - len(send_length))
                self.client.send(send_length)
                self.client.send(message.data)
            if message.type == MessageType.DISCONNECT:
                print("[SERVER] Client disconnection...")
                self.clientDisconnected.emit()
                self.client_is_connected = False

            print(f"[SERVER] Message sent \"{message.type}\"")


