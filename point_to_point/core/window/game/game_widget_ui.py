from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PySide6.QtGui import QFont

from core.widget.input_line import InputLine


class GameWidgetUI(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.resize(650, 400)

        button_font: QFont = QFont()
        button_font.setPointSize(18)

        self.other_input_line: InputLine = InputLine()
        self.other_input_line.setReadOnly(True)
        self.other_input_line.setFixedWidth(600)
        self.other_input_line.setFont(button_font)
        self.other_input_line.setText("Point to Point")

        self.this_input_line: InputLine = InputLine()
        self.this_input_line.setFixedWidth(600)
        self.this_input_line.setFont(button_font)
        self.this_input_line.setText("Point to Point")

        self.back_button: QPushButton = QPushButton(self)
        self.back_button.setFixedWidth(300)
        self.back_button.setText("Back")
        self.back_button.setFont(button_font)

        button_layout: QVBoxLayout = QVBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.back_button)

        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()
        main_layout.addWidget(self.other_input_line)
        main_layout.addStretch()
        main_layout.addWidget(self.this_input_line)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

