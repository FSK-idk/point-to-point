from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout
from PySide6.QtGui import QFont


class MainMenuWidgetUI(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setGeometry(0, 0, 1000, 600)
        self.setMinimumSize(400, 300)

        font18: QFont = QFont()
        font18.setPointSize(18)

        font48: QFont = QFont()
        font48.setPointSize(48)

        self.game_name_label: QLabel = QLabel(self)
        self.game_name_label.setFixedWidth(300)
        self.game_name_label.setText("Point\nto\nPoint")
        self.game_name_label.setFont(font48)
        self.game_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.server_button: QPushButton = QPushButton(self)
        self.server_button.setFixedWidth(300)
        self.server_button.setText("Server")
        self.server_button.setFont(font18)

        self.client_button: QPushButton = QPushButton(self)
        self.client_button.setFixedWidth(300)
        self.client_button.setText("Client")
        self.client_button.setFont(font18)

        button_layout: QVBoxLayout = QVBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.server_button)
        button_layout.addSpacing(15)
        button_layout.addWidget(self.client_button)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.game_name_label, 1)
        main_layout.addLayout(button_layout, 1)

        self.setLayout(main_layout)

