from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Set, Any
from core.models.geometry import Position
from core.models.railway.railway_system import RailwaySystem
class PlatformTargetType(Enum):
    NONE = auto()
    INVALID = auto()
    PREVIEW = auto()

@dataclass
class PlatformTarget:
    kind: PlatformTargetType
    edges: Optional[Set[Any]] = None
    message: Optional[str] = None

def find_platform_target(railway: RailwaySystem, world_pos: Position, camera_scale, platform_edge_count) -> PlatformTarget:
    closest_edge = railway.graph_service.get_closest_edge_on_grid(world_pos, camera_scale)
    if closest_edge is None or not railway.graph.has_edge(closest_edge):
        return PlatformTarget(kind=PlatformTargetType.NONE)
    
    if railway.stations.is_edge_platform(closest_edge):
        platform = railway.stations.get_platform_from_edge(closest_edge)
        return PlatformTarget(kind=PlatformTargetType.INVALID, edges=platform, message="Edge is already part of a platform!")
    
    is_valid, edges = railway.graph_service.calculate_platform_preview(closest_edge, platform_edge_count)
    if is_valid is False:
        return PlatformTarget(kind=PlatformTargetType.INVALID, edges=edges, message=f"Segment not suitable for {platform_edge_count*50}m long platform!")
    
    return PlatformTarget(kind=PlatformTargetType.PREVIEW, edges=edges)