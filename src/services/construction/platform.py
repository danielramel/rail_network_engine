from models.geometry import Position
from models.map import RailMap
from models.construction import CursorTarget
from dataclasses import dataclass
import math







@dataclass
class PlatformContext:
    type: CursorTarget
    data: Position | tuple[tuple[Position, Position], Position]
    station: Position | None

def get_platform_context(map: RailMap, world_pos: Position, camera_scale: float) -> PlatformContext:
    nearest_station = min(
        map.stations,
        key=lambda s: math.hypot(s.position.x - world_pos.x, s.position.y - world_pos.y)
        )
    closest_edge = world_pos.closest_edge(map.edges, camera_scale)
    if closest_edge is not None:
        if map.is_edge_platform(closest_edge):
            return PlatformContext(CursorTarget.PLATFORM, closest_edge, nearest_station)
        _, edges = map.get_segment(closest_edge, end_on_platform=True, only_straight=True, max_nr=7)
        return PlatformContext(CursorTarget.EDGE, (edges, closest_edge), nearest_station)

    
    return PlatformContext(CursorTarget.EMPTY, world_pos, nearest_station)
