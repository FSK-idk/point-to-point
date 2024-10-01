from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from PySide6.QtGui import QFont


class ServerMenuWidgetUI(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.resize(650, 400)

        font18: QFont = QFont()
        font18.setPointSize(18)

        self.open_connection_button: QPushButton = QPushButton(self)
        self.open_connection_button.setFixedWidth(300)
        self.open_connection_button.setText("Open connection")
        self.open_connection_button.setFont(font18)

        self.disconnect_client_button: QPushButton = QPushButton(self)
        self.disconnect_client_button.setFixedWidth(300)
        self.disconnect_client_button.setText("Disconnect client")
        self.disconnect_client_button.setFont(font18)

        self.close_connection_button: QPushButton = QPushButton(self)
        self.close_connection_button.setFixedWidth(300)
        self.close_connection_button.setText("Close connection")
        self.close_connection_button.setFont(font18)

        self.play_button: QPushButton = QPushButton(self)
        self.play_button.setFixedWidth(300)
        self.play_button.setText("Play")
        self.play_button.setFont(font18)

        self.settings_button: QPushButton = QPushButton(self)
        self.settings_button.setFixedWidth(300)
        self.settings_button.setText("Settings")
        self.settings_button.setFont(font18)

        self.back_button: QPushButton = QPushButton(self)
        self.back_button.setFixedWidth(300)
        self.back_button.setText("Back")
        self.back_button.setFont(font18)

        self.host_label: QLabel = QLabel(self)
        self.host_label.setText("host: unknown, port: unknown")
        self.connection_label: QLabel = QLabel(self)
        self.connection_label.setText("Connection is closed")
        self.client_label: QLabel = QLabel(self)
        self.client_label.setText("Client is disconnected")

        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.open_connection_button)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.disconnect_client_button)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.close_connection_button)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.play_button)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.settings_button)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.back_button)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.host_label)
        main_layout.addWidget(self.connection_label)
        main_layout.addWidget(self.client_label)

        self.setLayout(main_layout)

