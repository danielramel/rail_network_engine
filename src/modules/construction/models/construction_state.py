from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional
from core.config.settings import Config
from core.models.geometry.node import Node
from core.models.geometry.edge import Edge
from core.models.geometry.pose import Pose
from core.models.station import Station
from shared.ui.enums.edge_action import EdgeAction

class ConstructionTool(Enum):
    RAIL = auto()
    TUNNEL = auto()
    SIGNAL = auto()
    STATION = auto()
    PLATFORM = auto()
    BULLDOZE = auto()
    
@dataclass
class ConstructionPreview:
    edges: frozenset[Edge] = field(default_factory=frozenset)
    nodes: frozenset[Node] = field(default_factory=frozenset)
    edge_action: EdgeAction = None
    
    def clear(self) -> None:
        self.edges = frozenset()
        self.nodes = frozenset()
        self.edge_action = None
    
    
@dataclass
class ConstructionState:
    """Manages the current construction mode and associated state."""
    tool: ConstructionTool = ConstructionTool.RAIL
    construction_anchor: Pose | None = None
    track_speed: int = 120
    track_length: int = Config.SHORT_SEGMENT_LENGTH
    moving_station: Optional[Station] = None
    preview: ConstructionPreview = field(default_factory=ConstructionPreview)
    platform_waiting_for_station: bool = False
    platform_edge_count: int = 7
    
    def switch_tool(self, new_mode: ConstructionTool) -> None:
        """Switch to a new construction mode, clearing previous state."""
        if new_mode == self.tool:
            return
        
        self.tool = new_mode
        self.construction_anchor = None
        self.moving_station = None
        self.preview.clear()
        self.platform_waiting_for_station = False
        
    def is_edge_in_preview(self, edge: Edge) -> bool:
        """Check if an edge (in either direction) is in the preview set."""
        return edge in self.preview.edges
    
    def is_bulldoze_preview_node(self, node: Node) -> bool:
        """Check if a node is marked for bulldozing."""
        return self.tool is ConstructionTool.BULLDOZE and node in self.preview.nodes

    def is_station_being_moved(self, station: Station) -> bool:
        """Check if a specific station is currently being moved."""
        return self.moving_station == station
    
    def reset(self) -> None:
        """Reset the construction state to its initial values."""
        self.tool = ConstructionTool.RAIL
        self.construction_anchor = None
        self.track_speed = 120
        self.moving_station = None
        self.preview.clear()
        self.platform_waiting_for_station = False