from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from models.geometry import Position, Pose, Edge
from models.station import Station



class ConstructionMode(Enum):
    RAIL = 1
    SIGNAL = 2
    STATION = 3
    PLATFORM = 4
    BULLDOZE = 5
    
class EdgeType(Enum):
    PLATFORM = 1
    PLATFORM_SELECTED = 2

@dataclass
class ConstructionState:
    """Manages the current construction mode and associated state."""
    mode: ConstructionMode = ConstructionMode.RAIL
    construction_anchor: Pose | None = None
    track_speed: int = 120
    moving_station: Optional[Station] = None
    preview_edges: set[Edge] = field(default_factory=set)
    preview_nodes: set[Position] = field(default_factory=set)
    edge_type: Optional[EdgeType] = None
    state: Optional[str] = None
    
    def switch_mode(self, new_mode: ConstructionMode) -> None:
        """Switch to a new construction mode, clearing previous state."""
        if new_mode == self.mode:
            return
        
        self.construction_anchor = None
        self.moving_station = None
        self.preview_edges.clear()
        self.preview_nodes.clear()
        self.edge_type = None
        self.state = None
        self.mode = new_mode
    
    def is_edge_in_preview(self, edge: Edge) -> bool:
        """Check if an edge (in either direction) is in the preview set."""
        return edge in self.preview_edges

    def is_bulldoze_preview_node(self, pos: Position) -> bool:
        """Check if a position is marked for bulldozing."""
        return self.mode is ConstructionMode.BULLDOZE and pos in self.preview_nodes
    
    def is_station_being_moved(self, station: Station) -> bool:
        """Check if a specific station is currently being moved."""
        return self.moving_station == station