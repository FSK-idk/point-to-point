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
        self.score_label.setText("Winner: None")
        self.score_label.setFont(button_font)

        self.back_button: QPushButton = QPushButton(self)
        self.back_button.setFixedWidth(300)
        self.back_button.setText("Back")
        self.back_button.setFont(button_font)

        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()
        main_layout.addWidget(self.score_label)
        main_layout.addStretch()
        main_layout.addWidget(self.back_button)

        self.setLayout(main_layout)

