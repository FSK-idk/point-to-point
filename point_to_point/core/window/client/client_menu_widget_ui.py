from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel
from PySide6.QtGui import QFont


class ClientMenuWidgetUI(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.resize(650, 400)

        button_font: QFont = QFont()
        button_font.setPointSize(18)

        self.host_line_edit: QLineEdit = QLineEdit()
        self.host_line_edit.setFixedWidth(300)
        self.host_line_edit.setFont(button_font)
        self.host_line_edit.setPlaceholderText("Host")

        self.port_line_edit: QLineEdit = QLineEdit()
        self.port_line_edit.setFixedWidth(300)
        self.port_line_edit.setFont(button_font)
        self.port_line_edit.setPlaceholderText("Port")

        self.connect_to_server_button: QPushButton = QPushButton(self)
        self.connect_to_server_button.setFixedWidth(300)
        self.connect_to_server_button.setText("Connect")
        self.connect_to_server_button.setFont(button_font)

        self.disconnect_from_server_button: QPushButton = QPushButton(self)
        self.disconnect_from_server_button.setFixedWidth(300)
        self.disconnect_from_server_button.setText("Disconnect")
        self.disconnect_from_server_button.setFont(button_font)

        self.play_button: QPushButton = QPushButton(self)
        self.play_button.setFixedWidth(300)
        self.play_button.setText("Play")
        self.play_button.setFont(button_font)

        self.back_button: QPushButton = QPushButton(self)
        self.back_button.setFixedWidth(300)
        self.back_button.setText("Back")
        self.back_button.setFont(button_font)

        self.connection_label: QLabel = QLabel(self)
        self.connection_label.setText("Connection is closed")

        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.host_line_edit)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.port_line_edit)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.connect_to_server_button)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.disconnect_from_server_button)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.play_button)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.back_button)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.connection_label)

        self.setLayout(main_layout)

