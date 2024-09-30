from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from PySide6.QtGui import QFont


class ScoreWidgetUI(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.resize(650, 400)

        button_font: QFont = QFont()
        button_font.setPointSize(18)

        self.score_label: QLabel = QLabel(self)
        self.score_label.setText("None")
        self.score_label.setFont(button_font)
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.back_button: QPushButton = QPushButton(self)
        self.back_button.setFixedWidth(300)
        self.back_button.setText("Back")
        self.back_button.setFont(button_font)

        label_layout: QVBoxLayout = QVBoxLayout()
        label_layout.setContentsMargins(0, 0, 0, 0)
        label_layout.setSpacing(0)
        label_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_layout.addWidget(self.score_label)

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
        main_layout.addLayout(label_layout)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

