class MessageType():
    NOTHING = "nothing" # nothing happend
    DISCONNECT = "disconnect" # sender wants to disconnect
    READY = "ready" # sender is ready to play
    NOT_READY = "not_ready" # sender is not ready to play
    START_GAME = "start_game" # sender starts game
    SETUP_TEXT = "setup_text" # server sends the played text | data: initial text
    TEXT_CHANGED = "text_changed" # sender changed text | data: left text
    FINISH_GAME = "finish_game" # sender is winner
    INTERRUPT_GAME = "interrupt_game" # sender interrupted the game 


class Message:
    HEADER: int = 64
    FORMAT: str = "utf-8"

    def __init__(self, type: str, data: bytes | None = None) -> None:
        self.type: str = type
        if data is None:
            data = "None".encode(self.FORMAT)
        self.data: bytes = data
