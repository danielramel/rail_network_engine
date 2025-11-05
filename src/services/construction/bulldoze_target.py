from dataclasses import dataclass
from typing import Optional, Set, Any

from models.geometry.position import Position
from models.railway_system import RailwaySystem

class BulldozeTargetType:
    SIGNAL = 0
    STATION = 1
    PLATFORM = 2
    SEGMENT = 3
    NONE = 4
    
@dataclass
class BulldozeTarget:
    kind: BulldozeTargetType
    position: Optional[Any] = None    # Position for nodes/signals/stations
    edge: Optional[Any] = None   # single edge for removal
    edges: Optional[Set[Any]] = None  # set of edges for preview
    nodes: Optional[Set[Any]] = None  # set of nodes for preview

def find_bulldoze_target(railway: RailwaySystem, world_pos: Position, camera_scale) -> BulldozeTarget:
    snapped = world_pos.snap_to_grid()
    if railway.graph.has_node_at(snapped) and railway.signals.has_signal_at(snapped):
        return BulldozeTarget(kind=BulldozeTargetType.SIGNAL, position=snapped)

    for station in railway.stations.all():
        if world_pos.is_within_station_rect(station.position):
            return BulldozeTarget(kind=BulldozeTargetType.STATION, position=station.position)

    closest_edge = world_pos.closest_edge(railway.graph.edges, camera_scale)
    if closest_edge is None:
        return BulldozeTarget(kind=BulldozeTargetType.NONE, position=world_pos)

    if railway.stations.is_edge_platform(closest_edge):
        edges = railway.stations.get_platform_from_edge(closest_edge) ## edges return None TODO
        return BulldozeTarget(kind=BulldozeTargetType.PLATFORM, edge=closest_edge, edges=edges)

    nodes, edges = railway.graph_service.get_segment(closest_edge)
    return BulldozeTarget(kind=BulldozeTargetType.SEGMENT, edge=closest_edge, edges=edges, nodes=nodes)