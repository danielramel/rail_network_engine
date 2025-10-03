from dataclasses import dataclass, field
from enum import Enum
from models.geometry import Pose
from models.station import Station
from collections import defaultdict

class ConstructionMode(Enum):
    RAIL = 1
    SIGNAL = 2
    STATION = 3
    PLATFORM = 4
    BULLDOZE = 5
    
@dataclass
class ConstructionState:
    mode: ConstructionMode | None = ConstructionMode.RAIL
    construction_anchor: Pose | None = None
    moving_station: Station | None = None
    Rail: dict[str, Pose | int | None] = field(default_factory=lambda: defaultdict(lambda: None, {"anchor": None, "track_speed": 120}))

class CursorTarget(Enum):
    EDGE = 1
    SIGNAL = 2
    STATION = 3
    PLATFORM = 4
    EMPTY = 5