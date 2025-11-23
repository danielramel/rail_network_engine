from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Set, Any
from core.config.settings import Config
from core.models import station
from core.models.geometry.node import Node
from core.models.geometry.position import Position
from core.models.railway.railway_system import RailwaySystem
from core.models.station import Station
class PlatformTargetType(Enum):
    STATION_FOUND = auto()
    WAITING_FOR_STATION = auto()
    NONE = auto()
    INVALID = auto()
    PREVIEW = auto()

@dataclass
class PlatformTarget:
    kind: PlatformTargetType
    edges: Optional[Set[Any]] = None
    message: Optional[str] = None
    station : Optional[Station] = None

def find_platform_target(railway: RailwaySystem, world_pos: Position, platform_edge_count, waiting_for_station: bool) -> PlatformTarget:
    if waiting_for_station:
        for station in railway.stations.all():
            if world_pos.is_within_station_rect(station.node):
                return PlatformTarget(kind=PlatformTargetType.STATION_FOUND, station=station)
        return PlatformTarget(kind=PlatformTargetType.WAITING_FOR_STATION)
    
    closest_edge = railway.graph_service.get_closest_edge(world_pos)
    if closest_edge is None:
        return PlatformTarget(kind=PlatformTargetType.NONE)
    
    if railway.stations.is_edge_platform(closest_edge):
        platform = railway.stations.get_platform_from_edge(closest_edge)
        return PlatformTarget(kind=PlatformTargetType.INVALID, edges=platform, message="Edge is already part of a platform!")
    
    if railway.graph.get_edge_length(closest_edge) != Config.SHORT_SEGMENT_LENGTH:
        return PlatformTarget(kind=PlatformTargetType.INVALID, edges=frozenset([closest_edge]), message=f"Only {Config.SHORT_SEGMENT_LENGTH}m segments are allowed for platforms!")
    
    is_valid, edges = railway.graph_service.calculate_platform_preview(closest_edge, platform_edge_count)
    if is_valid is False:
        return PlatformTarget(kind=PlatformTargetType.INVALID, edges=edges, message=f"Segment does not fit {platform_edge_count*Config.SHORT_SEGMENT_LENGTH}m long platform!")
    
    return PlatformTarget(kind=PlatformTargetType.PREVIEW, edges=edges)