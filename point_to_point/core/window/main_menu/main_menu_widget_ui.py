from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout
from PySide6.QtGui import QFont


class MainMenuWidgetUI(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setGeometry(0, 0, 1000, 600)
        self.setMinimumSize(400, 300)

        label_font: QFont = QFont()
        label_font.setPointSize(48)

        button_font: QFont = QFont()
        button_font.setPointSize(18)

        self.game_name_label: QLabel = QLabel(self)
        self.game_name_label.setFixedWidth(300)
        self.game_name_label.setText("Point\nto\nPoint")
        self.game_name_label.setFont(label_font)
        self.game_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.play_button: QPushButton = QPushButton(self)
        self.play_button.setFixedWidth(300)
        self.play_button.setText("Play")
        self.play_button.setFont(button_font)

        self.server_button: QPushButton = QPushButton(self)
        self.server_button.setFixedWidth(300)
        self.server_button.setText("Server")
        self.server_button.setFont(button_font)

        self.client_button: QPushButton = QPushButton(self)
        self.client_button.setFixedWidth(300)
        self.client_button.setText("Client")
        self.client_button.setFont(button_font)

        self.settings_button: QPushButton = QPushButton(self)
        self.settings_button.setFixedWidth(300)
        self.settings_button.setText("Settings")
        self.settings_button.setFont(button_font)

        self.connected_label: QLabel = QLabel(self)
        self.connected_label.setText("Connected to: None")

        button_layout: QVBoxLayout = QVBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.play_button)
        button_layout.addSpacing(15)
        button_layout.addWidget(self.server_button)
        button_layout.addSpacing(15)
        button_layout.addWidget(self.client_button)
        button_layout.addSpacing(15)
        button_layout.addWidget(self.settings_button)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.game_name_label, 1)
        main_layout.addLayout(button_layout, 1)
        main_layout.addWidget(self.connected_label)

        self.setLayout(main_layout)

