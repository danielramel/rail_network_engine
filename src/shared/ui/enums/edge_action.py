from enum import Enum, auto

class EdgeAction(Enum):
    NO_SPEED = auto()
    SPEED = auto()
    PLATFORM = auto()
    LOCKED_PLATFORM = auto()
    PLATFORM_SELECTED = auto()
    PLATFORM_PREVIEW = auto()
    PLATFORM_OCCUPIED = auto()
    INVALID_PLATFORM = auto()
    BULLDOZE = auto()
    LOCKED = auto()
    LOCKED_PREVIEW = auto()
    OCCUPIED_PREVIEW = auto()
    INVALID_TRAIN_PLACEMENT = auto()