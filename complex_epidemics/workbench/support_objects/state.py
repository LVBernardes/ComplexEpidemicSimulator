from enum import Enum, auto


class State(Enum):
    CREATED = auto()
    RUNNING = auto()
    FINISHED = auto()
    ERROR = auto()
