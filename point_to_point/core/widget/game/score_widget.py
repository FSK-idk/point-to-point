from PySide6.QtCore import QObject

from core.widget.game.score_widget_ui import ScoreWidgetUI


class ScoreWidget(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.ui: ScoreWidgetUI = ScoreWidgetUI()

        self.ui.show()

    def setScoreText(self, text: str) -> None:
        self.ui.score_label.setText(text)
