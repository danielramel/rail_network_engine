# services/bulldoze.py
from dataclasses import dataclass
from enum import Enum

from utils import is_point_near_grid, point_line_intersection, point_within_station_rect, snap_to_grid
from models.map import RailMap

class BulldozeTargetType(Enum):
    EDGE = 1
    SIGNAL = 2
    STATION = 3
    NODE = 4
    EMPTY = 5

@dataclass
class BulldozeTarget:
    type: BulldozeTargetType
    data: object

def get_bulldoze_target(map: RailMap, world_pos: tuple[int, int], camera_scale: float) -> BulldozeTarget:
    # 1) If click isn't near the grid, check if it is on edge
    if not is_point_near_grid(*world_pos, camera_scale):
        for edge in map.graph.edges:
            if point_line_intersection(world_pos, edge[0], edge[1], camera_scale):
                return BulldozeTarget(BulldozeTargetType.EDGE, edge)

    snapped = snap_to_grid(*world_pos)

    for station in map.stations.keys():
        if point_within_station_rect(snapped, station):
            return BulldozeTarget(BulldozeTargetType.STATION, station)

    if snapped not in map.graph:
        return BulldozeTarget(BulldozeTargetType.EMPTY, snapped)

    if 'signal' in map.graph.nodes[snapped]:
        return BulldozeTarget(BulldozeTargetType.SIGNAL, snapped)

    return BulldozeTarget(BulldozeTargetType.NODE, snapped)
