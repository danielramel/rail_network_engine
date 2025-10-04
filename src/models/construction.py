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
    mode_info: dict = None
    
    def __post_init__(self):
        self.mode_info = {
            'construction_anchor': None,  # type: Pose | None
            'track_speed': 120,             # type: int
            'moving_station': None,      # type: Station | None
            'hidden_edges': set(),      # type: set[tuple[Pose, Pose]]
        }
        
    def switch_mode(self, new_mode: ConstructionMode):
        if new_mode == self.mode:
            return
        self.mode_info['construction_anchor'] = None
        self.mode_info['moving_station'] = None
        self.mode_info['hidden_edges'].clear()
            
        self.mode = new_mode
        
class CursorTarget(Enum):
    EDGE = 1
    SIGNAL = 2
    STATION = 3
    PLATFORM = 4
    EMPTY = 5