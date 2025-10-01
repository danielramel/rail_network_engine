from dataclasses import dataclass
from enum import Enum
from models.geometry import Pose

class ConstructionMode(Enum):
    RAIL = 1
    SIGNAL = 2
    STATION = 3
    PLATFORM = 4
    BULLDOZE = 5
    
@dataclass
class ConstructionState:
    Mode: ConstructionMode | None = ConstructionMode.RAIL
    construction_anchor: Pose | None = None

class CursorTarget(Enum):
    EDGE = 1
    SIGNAL = 2
    STATION = 3
    PLATFORM = 4
    EMPTY = 5