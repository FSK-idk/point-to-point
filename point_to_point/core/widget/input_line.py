from PySide6.QtWidgets import QWidget, QLineEdit
from PySide6.QtGui import QKeyEvent, QMouseEvent


class InputLine(QLineEdit):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

    def keyPressEvent(self, arg__1: QKeyEvent) -> None:
        if self.text() and arg__1.text() == self.text()[0]:
            self.setText(self.text()[1::])
        self.setCursorPosition(0)

    def mousePressEvent(self, arg__1: QMouseEvent) -> None:
        super().mousePressEvent(arg__1)
        self.setCursorPosition(0)
