from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget

from core.widget.client.client_menu_widget_ui import ClientMenuWidgetUI


class ClientMenuWidget(QObject):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__()

        self.ui: ClientMenuWidgetUI = ClientMenuWidgetUI(parent)

        self.ui.show()

