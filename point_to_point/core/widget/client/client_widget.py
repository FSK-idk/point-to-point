from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtWidgets import QWidget

from core.connection.message import MessageType, Message
from core.connection.client import Client
from core.widget.client.client_widget_ui import ClientWidgetUI


class ClientWidget(QObject):
    backToMainMenu: Signal = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__()

        self.client: Client = Client()

        self.client.connected.connect(self.onConnected)
        self.client.disconnected.connect(self.onDisconnected)

        self.client.receivedReady.connect(self.onReceivedReady)
        self.client.receivedNotReady.connect(self.onReceivedNotReady)
        self.client.receivedStartGame.connect(self.onReceivedStartGame)
        self.client.receivedSetupText.connect(self.onReceivedSetupText)
        self.client.receivedTextChanged.connect(self.onReceivedTextChanged)
        self.client.receivedFinishGame.connect(self.onReceivedFinishGame)
        self.client.receivedInterruptGame.connect(self.onReceivedInterruptGame)


        self.ui: ClientWidgetUI = ClientWidgetUI(parent)

        self.ui.main_layout.setCurrentIndex(self.ui.CLIENT_MENU_INDEX)

        self.ui.closeUI.connect(self.onCloseUI)

        self.ui.client_menu.ui.connect_to_server_button.clicked.connect(self.onConnectClicked)
        self.ui.client_menu.ui.disconnect_from_server_button.clicked.connect(self.client.disconnectFromServer)
        self.ui.client_menu.ui.play_button.clicked.connect(self.openWaiting)
        self.ui.client_menu.ui.back_button.clicked.connect(self.onClientMenuBack)

        self.ui.waiting.ui.back_button.clicked.connect(self.openClientMenu)

        self.ui.game.ui.back_button.clicked.connect(self.openClientMenu)
        self.ui.game.textChanged.connect(self.onTextChanged)

        self.ui.score.ui.back_button.clicked.connect(self.openClientMenu)

        self.server_is_ready: bool = False
        self.client_is_ready: bool = False

        self.ui.show()

    @Slot()
    def openClientMenu(self) -> None:
        self.client_is_ready = False
        self.client.sendMessage(MessageType.NOT_READY)

        match self.ui.main_layout.currentIndex():
            case self.ui.GAME_INDEX:
                self.client.sendMessage(MessageType.INTERRUPT_GAME)

        self.ui.main_layout.setCurrentIndex(self.ui.CLIENT_MENU_INDEX)

    @Slot()
    def openWaiting(self) -> None:
        if not self.client.connected_to_server:
            return

        self.client.sendMessage(MessageType.READY)

        self.ui.main_layout.setCurrentIndex(self.ui.WAITING_INDEX)

        if self.server_is_ready:
            self.client.sendMessage(MessageType.START_GAME)
            self.openGame()

    @Slot()
    def openGame(self) -> None:
        self.ui.game.ui.this_input_line.setFocus()
        self.ui.main_layout.setCurrentIndex(self.ui.GAME_INDEX)

    @Slot()
    def openScore(self) -> None:
        self.client_is_ready = False
        self.client.sendMessage(MessageType.NOT_READY)

        self.ui.main_layout.setCurrentIndex(self.ui.SCORE_INDEX)

    @Slot()
    def onConnectClicked(self) -> None:
        self.client.connectToServer(self.ui.client_menu.ui.host_line_edit.text(), self.ui.client_menu.ui.port_line_edit.text())

    @Slot()
    def onClientMenuBack(self) -> None:
        self.client_is_ready = False
        self.client.sendMessage(MessageType.NOT_READY)

        if self.client.connected_to_server:
            self.client.disconnectFromServer()
        self.backToMainMenu.emit()

    @Slot()
    def onTextChanged(self, text: str) -> None:
        self.client.sendMessage(MessageType.TEXT_CHANGED, text.encode(Message.FORMAT))
        if not text:
            self.ui.score.setScoreText("You won")
            self.client.sendMessage(MessageType.FINISH_GAME)
            self.openScore()

    @Slot()
    def onCloseUI(self) -> None:
        self.client.disconnectFromServer()

    # client signals

    @Slot()
    def onConnected(self) -> None:
        self.ui.client_menu.ui.connection_label.setText("Connection is open")

    @Slot()
    def onDisconnected(self) -> None:
        # threre are an exception when client close application while connection is open in menu
        try:
            self.ui.client_menu.ui.connection_label.setText("Connection is closed")
        except:
            pass

    @Slot()
    def onReceivedReady(self) -> None:
        self.server_is_ready = True
        if self.client_is_ready:
            self.openGame()
            self.client.sendMessage(MessageType.START_GAME)

    @Slot()
    def onReceivedNotReady(self) -> None:
        self.server_is_ready = False

    @Slot()
    def onReceivedStartGame(self) -> None:
        self.openGame()

    @Slot()
    def onReceivedSetupText(self, text: str) -> None:
        self.ui.game.ui.this_input_line.setText(text)
        self.ui.game.ui.other_input_line.setText(text)

    @Slot()
    def onReceivedTextChanged(self, text: str) -> None:
        self.ui.game.ui.other_input_line.setText(text)

    @Slot()
    def onReceivedFinishGame(self) -> None:
        self.ui.score.setScoreText("Opponent won")
        self.openScore()

    @Slot()
    def onReceivedInterruptGame(self) -> None:
        self.ui.score.setScoreText("Opponent interrupted the game")
        self.openScore()

