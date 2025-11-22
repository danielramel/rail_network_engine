from dataclasses import dataclass
from core.models.geometry.edge import Edge
from core.models.geometry.node import Node
from core.models.railway.railway_system import RailwaySystem

class BulldozeTargetType:
    SIGNAL = 0
    STATION = 1
    PLATFORM = 2
    SEGMENT = 3
    NONE = 4
    
@dataclass
class BulldozeTarget:
    kind: BulldozeTargetType
    node: Node = None    # Position for nodes/signals/stations
    edge: Edge = None   # single edge for removal
    edges: frozenset[Edge] = None  # set of edges for preview
    nodes: frozenset[Node] = None  # set of nodes for preview

def find_bulldoze_target(railway: RailwaySystem, world_pos: Node, camera_scale) -> BulldozeTarget:
    snapped = world_pos.snap_to_grid()
    if railway.signals.has_signal_at(snapped):
        return BulldozeTarget(kind=BulldozeTargetType.SIGNAL, node=snapped)

    for station in railway.stations.all():
        if world_pos.is_within_station_rect(station.node):
            return BulldozeTarget(kind=BulldozeTargetType.STATION, node=station.node)

    closest_edge = railway.graph_service.get_closest_edge(world_pos, camera_scale)
    if closest_edge is None:
        return BulldozeTarget(kind=BulldozeTargetType.NONE, node=world_pos)

    if railway.stations.is_edge_platform(closest_edge):
        edges = railway.stations.get_platform_from_edge(closest_edge)
        return BulldozeTarget(kind=BulldozeTargetType.PLATFORM, edge=closest_edge, edges=edges)

    nodes, edges = railway.graph_service.get_segment(closest_edge)
    return BulldozeTarget(kind=BulldozeTargetType.SEGMENT, edge=closest_edge, edges=edges, nodes=nodes)