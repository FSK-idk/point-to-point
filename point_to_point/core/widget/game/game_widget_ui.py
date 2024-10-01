from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtGui import QFont

from core.widget.input_line.input_line import InputLine


class GameWidgetUI(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.resize(650, 400)

        font18: QFont = QFont()
        font18.setPointSize(18)

        self.other_label: QLabel = QLabel(self)
        self.other_label.setFixedWidth(120)
        self.other_label.setFont(font18)
        self.other_label.setText("Opponent")

        self.other_input_line: InputLine = InputLine(self)
        self.other_input_line.setReadOnly(True)
        self.other_input_line.setFixedWidth(600)
        self.other_input_line.setFont(font18)
        self.other_input_line.setText("Point to Point")

        self.this_label: QLabel = QLabel(self)
        self.this_label.setFixedWidth(120)
        self.this_label.setFont(font18)
        self.this_label.setText("You")

        self.this_input_line: InputLine = InputLine(self)
        self.this_input_line.setFixedWidth(600)
        self.this_input_line.setFont(font18)
        self.this_input_line.setText("Point to Point")

        self.back_button: QPushButton = QPushButton(self)
        self.back_button.setFixedWidth(300)
        self.back_button.setText("Back")
        self.back_button.setFont(font18)

        other_layout: QHBoxLayout = QHBoxLayout()
        other_layout.setContentsMargins(0, 0, 0, 0)
        other_layout.setSpacing(0)
        other_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        other_layout.addWidget(self.other_label)
        other_layout.addSpacing(15)
        other_layout.addWidget(self.other_input_line)

        this_layout: QHBoxLayout = QHBoxLayout()
        this_layout.setContentsMargins(0, 0, 0, 0)
        this_layout.setSpacing(0)
        this_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        this_layout.addWidget(self.this_label)
        this_layout.addSpacing(15)
        this_layout.addWidget(self.this_input_line)

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
        main_layout.addLayout(other_layout)
        main_layout.addStretch()
        main_layout.addLayout(this_layout)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

