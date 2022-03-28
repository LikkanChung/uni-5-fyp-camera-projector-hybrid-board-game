from enum import Enum, auto


class State(Enum):
    CALIBRATING = auto()
    MAIN = auto()
    GAME = auto()
    QUIT = auto()
