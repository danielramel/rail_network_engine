# services/platform_tool.py
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Set, Any
from config.settings import PLATFORM_LENGTH, GRID_SIZE
from models.geometry import Position
from models.railway_system import RailwaySystem

class PlatformTargetType(Enum):
    NONE = 0
    EXISTING_PLATFORM = 1
    PREVIEW = 2

@dataclass
class PlatformTarget:
    kind: PlatformTargetType
    closest_edge: Optional[Any] = None
    edges: Optional[Set[Any]] = None
    is_valid: bool = False

def find_platform_target(railway: RailwaySystem, world_pos: Position, camera_scale) -> PlatformTarget:
    closest_edge = world_pos.closest_edge(railway.graph.edges, camera_scale)
    if closest_edge is None:
        return PlatformTarget(kind=PlatformTargetType.NONE, closest_edge=None)

    if railway.stations.is_edge_platform(closest_edge):
        return PlatformTarget(kind=PlatformTargetType.EXISTING_PLATFORM, closest_edge=closest_edge)

    is_valid, edges = railway.graph_service.calculate_platform_preview(closest_edge)
    

    return PlatformTarget(kind=PlatformTargetType.PREVIEW, closest_edge=closest_edge, edges=edges, is_valid=is_valid)
