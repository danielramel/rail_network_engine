from dataclasses import dataclass
from enum import Enum
from models.geometry.position import Position
from models.station import Station

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
            'preview_edges': set(),      # type: set[tuple[Pose, Pose]]
            'preview_nodes': set(),      # type: set[Position]
            'edge_type': None,        # type: str | None
            'state': None
        }
        
    def switch_mode(self, new_mode: ConstructionMode):
        if new_mode == self.mode:
            return
        self.mode_info['construction_anchor'] = None
        self.mode_info['moving_station'] = None
        self.mode_info['preview_edges'].clear()
        self.mode_info['preview_nodes'].clear()
        self.mode_info['edge_type'] = None
        self.mode_info['state'] = None
            
        self.mode = new_mode

    def is_edge_in_preview(self, edge: tuple[Position, Position]) -> bool:
        a, b = edge
        return ((a, b) in self.mode_info['preview_edges'] or (b, a) in self.mode_info['preview_edges'])

    def is_bulldoze_preview_node(self, pos: Position) -> bool:
        return self.mode is ConstructionMode.BULLDOZE and pos in self.mode_info['preview_nodes']
    
    def is_station_being_moved(self, station: Station) -> bool:
        return self.mode_info['moving_station'] == station

class CursorTarget(Enum):
    EDGE = 1
    SIGNAL = 2
    STATION = 3
    PLATFORM = 4
    EMPTY = 5