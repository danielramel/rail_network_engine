from dataclasses import dataclass
from models.construction import CursorTarget
from models.geometry import Position
from models.map import RailMap

@dataclass
class BulldozeTarget:
    type: CursorTarget
    data: object

def get_bulldoze_target(map: RailMap, world_pos: Position, camera_scale: float) -> BulldozeTarget:
    snapped = world_pos.snap_to_grid()
    if map.has_node_at(snapped) and map.has_signal_at(snapped):
        return BulldozeTarget(CursorTarget.SIGNAL, snapped)
    
    for station in map.stations.keys():
        if snapped.station_rect_overlaps(station):
            return BulldozeTarget(CursorTarget.STATION, station)

    closest_edge = world_pos.closest_edge(map.edges, camera_scale)

    if closest_edge is not None:
        if map.is_edge_platform(closest_edge):
            return BulldozeTarget(CursorTarget.PLATFORM, closest_edge)
        else:
            return BulldozeTarget(CursorTarget.EDGE, closest_edge)
            
    return BulldozeTarget(CursorTarget.EMPTY, world_pos)


    

