from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Set, Any
from core.models.geometry.position import Position
from core.models.railway.railway_system import RailwaySystem
from core.config.settings import Config


class DeadEndTargetType(Enum):
    NONE = auto()
    INVALID = auto()
    PREVIEW = auto()

@dataclass
class DeadEndTarget:
    kind: DeadEndTargetType
    edges: Optional[Set[Any]] = None
    message: Optional[str] = None

def find_dead_end_target(railway: RailwaySystem, world_pos: Position) -> DeadEndTarget:
    closest_edge = railway.graph_service.get_closest_edge(world_pos)
    if closest_edge is None:
        return DeadEndTarget(kind=DeadEndTargetType.NONE)

    if railway.stations.is_edge_platform(closest_edge):
        platform = railway.stations.get_platform_from_edge(closest_edge)
        return DeadEndTarget(kind=DeadEndTargetType.INVALID, edges=platform, message="Edge is already part of a platform!")

    if railway.graph.get_edge_length(closest_edge) != Config.SHORT_SEGMENT_LENGTH:
        return DeadEndTarget(kind=DeadEndTargetType.INVALID, edges=frozenset([closest_edge]), message=f"Only {Config.SHORT_SEGMENT_LENGTH}m segments are allowed for dead ends!")

    is_valid, edges = railway.graph_service.calculate_platform_preview(closest_edge, Config.MAX_PLATFORM_EDGE_COUNT)
    if is_valid is False:
        return DeadEndTarget(kind=DeadEndTargetType.INVALID, edges=edges, message=f"Segment does not fit dead-end. Minimum length: {Config.MAX_PLATFORM_EDGE_COUNT * Config.SHORT_SEGMENT_LENGTH}m!")
    
    has_dead_end = False
    for edge in edges:
        if railway.signals.has(edge.a) or railway.signals.has(edge.b):
            return DeadEndTarget(kind=DeadEndTargetType.INVALID, edges=edges, message="Cannot place dead-end on segments with signals!")
        
        if railway.graph.degree_at(edge.a) == 1 or railway.graph.degree_at(edge.b) == 1:
            has_dead_end = True
    if not has_dead_end:
        return DeadEndTarget(kind=DeadEndTargetType.INVALID, edges=edges, message="Selected segment is not a dead end!")

    return DeadEndTarget(kind=DeadEndTargetType.PREVIEW, edges=edges)