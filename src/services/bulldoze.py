from dataclasses import dataclass
from models.construction import CursorTarget

from models.position import Position
from models.map import RailMap



@dataclass
class BulldozeTarget:
    type: CursorTarget
    data: object

def get_bulldoze_target(map: RailMap, world_pos: Position, camera_scale: float) -> BulldozeTarget:
    # 1) If click isn't near the grid, check if it is on edge
    if not world_pos.is_near_grid(camera_scale):
        for edge in map.graph.edges:
            if world_pos.intersects_line(edge, camera_scale):
                return BulldozeTarget(CursorTarget.EDGE, edge)

    snapped = world_pos.snap_to_grid()

    for station in map.stations.keys():
        if snapped.station_rect_overlaps(station):
            return BulldozeTarget(CursorTarget.STATION, station)

    if snapped not in map.graph:
        return BulldozeTarget(CursorTarget.EMPTY, snapped)

    if 'signal' in map.graph.nodes[snapped]:
        return BulldozeTarget(CursorTarget.SIGNAL, snapped)

    return BulldozeTarget(CursorTarget.NODE, snapped)
