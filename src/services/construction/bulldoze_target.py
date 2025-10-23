from dataclasses import dataclass
from typing import Optional, Set, Any

from models.geometry.position import Position
from models.simulation import Simulation

class BulldozeTargetType:
    SIGNAL = 0
    STATION = 1
    PLATFORM = 2
    SEGMENT = 3
    NONE = 4
    
@dataclass
class BulldozeTarget:
    kind: BulldozeTargetType
    pos: Optional[Any] = None    # Position for nodes/signals/stations
    edge: Optional[Any] = None   # single edge for removal
    edges: Optional[Set[Any]] = None  # set of edges for preview
    nodes: Optional[Set[Any]] = None  # set of nodes for preview

def find_bulldoze_target(map: Simulation, world_pos: Position, camera_scale) -> BulldozeTarget:
    snapped = world_pos.snap_to_grid()
    if map.graph.has_node_at(snapped) and map.signals.has_signal_at(snapped):
        return BulldozeTarget(kind=BulldozeTargetType.SIGNAL, pos=snapped)

    for station_pos in map.stations.positions():
        if world_pos.is_within_station_rect(station_pos):
            return BulldozeTarget(kind=BulldozeTargetType.STATION, pos=station_pos)

    closest_edge = world_pos.closest_edge(map.graph.edges, camera_scale)
    if closest_edge is None:
        return BulldozeTarget(kind=BulldozeTargetType.NONE, pos=world_pos)

    if map.platforms.is_edge_platform(closest_edge):
        edges = map.platforms.get_platform_from_edge(closest_edge) ## edges return None TODO
        return BulldozeTarget(kind=BulldozeTargetType.PLATFORM, edge=closest_edge, edges=edges)

    nodes, edges = map.graph.get_segment(closest_edge)
    return BulldozeTarget(kind=BulldozeTargetType.SEGMENT, edge=closest_edge, edges=edges, nodes=nodes)