from dataclasses import dataclass
from typing import Optional, Set, Any

@dataclass
class BulldozeTarget:
    kind: str                    # 'signal' | 'station' | 'platform' | 'segment' | 'node' | 'none'
    pos: Optional[Any] = None    # Position for nodes/signals/stations
    edge: Optional[Any] = None   # single edge for removal
    edges: Optional[Set[Any]] = None  # set of edges for preview
    nodes: Optional[Set[Any]] = None  # set of nodes for preview

def find_bulldoze_target(map, world_pos, camera_scale) -> BulldozeTarget:
    snapped = world_pos.snap_to_grid()
    if map.has_node_at(snapped) and map.has_signal_at(snapped):
        return BulldozeTarget(kind='signal', pos=snapped)

    for station_pos in map.station_positions:
        if world_pos.is_within_station_rect(station_pos):
            return BulldozeTarget(kind='station', pos=station_pos)

    closest_edge = world_pos.closest_edge(map.edges, camera_scale)
    if closest_edge is None:
        return BulldozeTarget(kind='node', pos=world_pos)

    if map.is_edge_platform(closest_edge):
        edges = map.get_platform(closest_edge)
        return BulldozeTarget(kind='platform', edge=closest_edge, edges=edges)

    nodes, edges = map.get_segment(closest_edge)
    return BulldozeTarget(kind='segment', edge=closest_edge, edges=edges, nodes=nodes)
