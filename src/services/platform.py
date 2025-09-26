
from models.position import Position
from models.map import RailMap
from models.construction import CursorTarget
from dataclasses import dataclass

@dataclass
class PlatformContext:
    type: CursorTarget
    data: Position | tuple[Position, Position]
    nearest_station: Position | None

def get_platform_context(map: RailMap, world_pos: Position, camera_scale: float) -> PlatformContext:
    # calculate nearest station
    if len(map.stations) == 0:
        nearest_station = None
    else:
        nearest_station = min(map.stations.keys(), key=lambda s: ((s.x - world_pos.x) ** 2 + (s.y - world_pos.y) ** 2) ** 0.5, default=None)

    for edge in map.graph.edges:
        if world_pos.intersects_line(edge, camera_scale):
            return PlatformContext(CursorTarget.EDGE, edge, nearest_station)

    snapped = world_pos.snap_to_grid()
    if snapped in map.graph:
        return PlatformContext(CursorTarget.NODE, snapped, nearest_station)

    return PlatformContext(CursorTarget.EMPTY, snapped, nearest_station)
