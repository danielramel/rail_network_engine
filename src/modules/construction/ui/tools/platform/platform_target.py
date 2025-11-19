# services/platform_tool.py
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Set, Any
from core.config.settings import PLATFORM_LENGTH, GRID_SIZE
from core.models.geometry import Position
from core.models.geometry.edge import Edge
from core.models.railway.railway_system import RailwaySystem
class PlatformTargetType(Enum):
    INVALID = auto()
    PREVIEW = 2

@dataclass
class PlatformTarget:
    kind: PlatformTargetType
    closest_edge: Optional[Any] = None
    edges: Optional[Set[Any]] = None
    is_valid: bool = False

def find_platform_target(railway: RailwaySystem, world_pos: Position, camera_scale) -> PlatformTarget:
    closest_edge = railway.graph_service.get_closest_edge_on_grid(world_pos, camera_scale)
    if closest_edge is None or \
        not railway.graph.has_edge(closest_edge) or \
        railway.stations.is_edge_platform(closest_edge):
        return PlatformTarget(kind=PlatformTargetType.INVALID, closest_edge=None)
    
    is_valid, edges = railway.graph_service.calculate_platform_preview(closest_edge)
    return PlatformTarget(kind=PlatformTargetType.PREVIEW, closest_edge=closest_edge, edges=edges, is_valid=is_valid)
