from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PySide6.QtGui import QFont


class ServerMenuWidgetUI(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Connect")
        self.resize(650, 400)

        button_font: QFont = QFont()
        button_font.setPointSize(18)

        self.open_connection_button: QPushButton = QPushButton(self)
        self.open_connection_button.setFixedWidth(300)
        self.open_connection_button.setText("Open connection")
        self.open_connection_button.setFont(button_font)

        self.disconnect_client_button: QPushButton = QPushButton(self)
        self.disconnect_client_button.setFixedWidth(300)
        self.disconnect_client_button.setText("Disconnect client")
        self.disconnect_client_button.setFont(button_font)

        self.close_connection_button: QPushButton = QPushButton(self)
        self.close_connection_button.setFixedWidth(300)
        self.close_connection_button.setText("Close connection")
        self.close_connection_button.setFont(button_font)

        self.back_button: QPushButton = QPushButton(self)
        self.back_button.setFixedWidth(300)
        self.back_button.setText("Back")
        self.back_button.setFont(button_font)

        button_layout: QVBoxLayout = QVBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.open_connection_button)
        button_layout.addSpacing(15)
        button_layout.addWidget(self.disconnect_client_button)
        button_layout.addSpacing(15)
        button_layout.addWidget(self.close_connection_button)
        button_layout.addSpacing(15)
        button_layout.addWidget(self.back_button)

        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

