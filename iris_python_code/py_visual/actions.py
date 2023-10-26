from enum import Enum, auto

# Enumeration of all the possible actions doable in the graphical user interface.
class ActionType(Enum):
    SELECT_HUMAN = auto()
    SELECT_BOT = auto()
    BOT_PLAY = auto()
    MOVE = auto()
    GOBACK = auto()