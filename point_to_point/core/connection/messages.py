class MessageType():
    NOTHING = "nothing"
    DISCONNECT = "disconnect"
    READY = "ready"
    NOT_READY = "not_ready"
    START_GAME = "start_game"
    SETUP_TEXT = "setup_text" # data: initial text / only server can send
    TEXT_CHANGED = "text_changed" # data: left text
    FINISH_GAME = "finish_game" # who send is winner
    INTERRUPT_GAME = "interrupt_game"

class Message:
    HEADER: int = 64
    FORMAT: str = "utf-8"

    def __init__(self, type: str, data: bytes | None = None) -> None:
        self.type: str = type
        if data is None:
            data = "None".encode(self.FORMAT)
        self.data: bytes = data
