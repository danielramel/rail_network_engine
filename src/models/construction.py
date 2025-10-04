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
    mode: ConstructionMode | None = None
    mode_info: dict = field(default_factory=lambda: defaultdict(dict))
    
    def __post_init__(self):
        self.switch_mode(ConstructionMode.RAIL)
        
    def switch_mode(self, new_mode: ConstructionMode):
        if new_mode == self.mode:
            return
        if new_mode is ConstructionMode.RAIL:
            self.mode_info = {"construction_anchor": None, "track_speed": 120}
        elif new_mode is ConstructionMode.STATION:
            self.mode_info = {"moving_station": None}
        else:
            self.mode_info = {} 
            
        self.mode = new_mode
        
class CursorTarget(Enum):
    EDGE = 1
    SIGNAL = 2
    STATION = 3
    PLATFORM = 4
    EMPTY = 5