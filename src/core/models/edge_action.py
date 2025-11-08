from enum import Enum, auto

class EdgeAction(Enum):
    NORMAL = auto()
    SPEED = auto()
    PLATFORM = auto()
    PLATFORM_SELECTED = auto()
    INVALID_PLATFORM = auto()
    BULLDOZE = auto()
    LOCKED = auto()
    LOCKED_PREVIEW = auto()
    LOCKED_PLATFORM = auto()