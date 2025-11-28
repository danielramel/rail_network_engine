from enum import Enum, auto

class EdgeAction(Enum):
    NO_SPEED = auto()
    SPEED = auto()
    PLATFORM = auto()
    LOCKED_PLATFORM = auto()
    PLATFORM_SELECTED = auto()
    PLATFORM_PREVIEW = auto()
    INVALID_PLATFORM = auto()
    BULLDOZE = auto()
    LOCKED = auto()
    LOCKED_PREVIEW = auto()
    INVALID_TRAIN_PLACEMENT = auto()