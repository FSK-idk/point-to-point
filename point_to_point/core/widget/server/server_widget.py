from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtWidgets import QWidget

from core.config.config import config
from core.connection.message import MessageType, Message
from core.connection.server import Server
from core.widget.server.server_widget_ui import ServerWidgetUI


class ServerWidget(QObject):
    backToMainMenu: Signal = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__()

        self.server: Server = Server()

        self.server.clientDisconnected.connect(self.onClientDisconnected)
        self.server.clientConnected.connect(self.onClientConnected)
        self.server.connectionClosed.connect(self.onConnectionClosed)
        self.server.connectionOpen.connect(self.onConnectionOpen)

        self.server.receivedDisconnect.connect(self.onReceivedDisconnect)
        self.server.receivedReady.connect(self.onReceivedReady)
        self.server.receivedNotReady.connect(self.onReceivedNotReady)
        self.server.receivedStartGame.connect(self.onReceivedStartGame)
        self.server.receivedMessageChanged.connect(self.onReceivedMessageChanged)
        self.server.receivedFinishGame.connect(self.onReceivedFinishGame)
        self.server.receivedInterruptGame.connect(self.onReceivedInterruptGame)

        self.ui: ServerWidgetUI = ServerWidgetUI(parent)

        self.ui.main_layout.setCurrentIndex(self.ui.SERVER_MENU_INDEX)

        self.ui.closeUI.connect(self.onCloseUI)

        self.ui.server_menu.ui.open_connection_button.clicked.connect(self.server.openConnection)
        self.ui.server_menu.ui.disconnect_client_button.clicked.connect(self.server.disconnectClient)
        self.ui.server_menu.ui.close_connection_button.clicked.connect(self.server.closeConnection)
        self.ui.server_menu.ui.settings_button.clicked.connect(self.openSettings)
        self.ui.server_menu.ui.play_button.clicked.connect(self.openWaiting)
        self.ui.server_menu.ui.back_button.clicked.connect(self.onServerMenuBack)

        self.ui.settings.ui.back_button.clicked.connect(self.openServerMenu)

        self.ui.waiting.ui.back_button.clicked.connect(self.openServerMenu)

        self.ui.game.ui.back_button.clicked.connect(self.openServerMenu)
        self.ui.game.textChanged.connect(self.onTextChanged)

        self.ui.score.ui.back_button.clicked.connect(self.openServerMenu)

        self.ui.server_menu.ui.host_label.setText(f"host: {self.server.host}, port: {self.server.port}")

        self.server_is_ready: bool = False
        self.client_is_ready: bool = False

        self.ui.show()

    @Slot()
    def openServerMenu(self) -> None:
        self.server_is_ready = False
        self.server.sendMessage(MessageType.NOT_READY)

        match self.ui.main_layout.currentIndex():
            case self.ui.SETTINGS_MENU_INDEX:
                config["Settings"]["text"] = self.ui.settings.ui.text_edit.toPlainText()
                config.write()

            case self.ui.GAME_INDEX:
                self.server.sendMessage(MessageType.INTERRUPT_GAME)

        self.ui.main_layout.setCurrentIndex(self.ui.SERVER_MENU_INDEX)

    @Slot()
    def openSettings(self) -> None:
        self.ui.settings.ui.text_edit.setText(config["Settings"]["text"])
        self.ui.main_layout.setCurrentIndex(self.ui.SETTINGS_MENU_INDEX)

    @Slot()
    def openWaiting(self) -> None:
        if not self.server.listeing_to_clients:
            return

        self.server_is_ready = True
        self.server.sendMessage(MessageType.READY)

        if self.client_is_ready:
            self.server.sendMessage(MessageType.START_GAME)
            self.openGame()
        else:
            self.ui.main_layout.setCurrentIndex(self.ui.WAITING_INDEX)

    @Slot()
    def openGame(self) -> None:
        text = config["Settings"]["text"]
        self.ui.game.ui.this_input_line.setText(text)
        self.ui.game.ui.other_input_line.setText(text)
        self.server.sendMessage(MessageType.SETUP_TEXT, text.encode(Message.FORMAT))
        self.ui.game.ui.this_input_line.setFocus()
        self.ui.main_layout.setCurrentIndex(self.ui.GAME_INDEX)

    @Slot()
    def openScore(self) -> None:
        self.server_is_ready = False
        self.server.sendMessage(MessageType.NOT_READY)

        self.ui.main_layout.setCurrentIndex(self.ui.SCORE_INDEX)

    @Slot()
    def onServerMenuBack(self) -> None:
        self.server_is_ready = False
        self.server.sendMessage(MessageType.NOT_READY)

        if self.server.listeing_to_clients:
            self.server.closeConnection()
        self.backToMainMenu.emit()

    @Slot()
    def onTextChanged(self, text: str) -> None:
        self.server.sendMessage(MessageType.TEXT_CHANGED, text.encode(Message.FORMAT))
        if not text:
            self.ui.score.setScoreText("You won")
            self.server.sendMessage(MessageType.FINISH_GAME)
            self.openScore()

    @Slot()
    def onCloseUI(self) -> None:
        self.server.closeConnection()

    # server signals

    @Slot()
    def onClientDisconnected(self) -> None:
        self.ui.server_menu.ui.client_label.setText("Client is disconnected")

    @Slot()
    def onClientConnected(self) -> None:
        self.ui.server_menu.ui.client_label.setText("Client is connected")

    @Slot()
    def onConnectionClosed(self) -> None:
        self.ui.server_menu.ui.connection_label.setText("Connection is closed")
        
    @Slot()
    def onConnectionOpen(self) -> None:
        self.ui.server_menu.ui.connection_label.setText("Connection is open")

    @Slot()
    def onReceivedDisconnect(self) -> None:
        self.server.disconnectClient()

    @Slot()
    def onReceivedReady(self) -> None:
        self.client_is_ready = True
        if self.server_is_ready:
            self.openGame()
            self.server.sendMessage(MessageType.START_GAME)

    @Slot()
    def onReceivedNotReady(self) -> None:
        self.client_is_ready = False

    @Slot()
    def onReceivedStartGame(self) -> None:
        self.openGame()

    @Slot()
    def onReceivedMessageChanged(self, text: str) -> None:
        self.ui.game.ui.other_input_line.setText(text)

    @Slot()
    def onReceivedFinishGame(self) -> None:
        self.ui.score.setScoreText("Opponent won")
        self.openScore()

    @Slot()
    def onReceivedInterruptGame(self) -> None:
        self.ui.score.setScoreText("Opponent interrupted the game")
        self.openScore()

