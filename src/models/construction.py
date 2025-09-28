from dataclasses import dataclass
from enum import Enum
from models.position import PositionWithDirection

class ConstructionMode(Enum):
    RAIL = 1
    SIGNAL = 2
    STATION = 3
    BULLDOZE = 4
    PLATFORM = 5
    
@dataclass
class ConstructionState:
    Mode: ConstructionMode | None = ConstructionMode.RAIL
    construction_anchor: PositionWithDirection | None = None

class CursorTarget(Enum):
    EDGE = 1
    SIGNAL = 2
    STATION = 3
    NODE = 4
    PLATFORM = 5
    EMPTY = 6