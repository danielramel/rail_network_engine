from enum import Enum

class EdgeAction(Enum):
    NORMAL = 0
    SPEED = 1
    PLATFORM = 10
    PLATFORM_SELECTED = 2
    INVALID_PLATFORM = 3
    BULLDOZE = 4
    LOCKED = 5
    LOCKED_PREVIEW = 6
    LOCKED_PLATFORM = 7
    OCCUPIED = 8
    OCCUPIED_PLATFORM = 9