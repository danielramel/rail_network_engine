
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
        map.get_all_stations().values(),
        key=lambda s: math.hypot(s.position.x - world_pos.x, s.position.y - world_pos.y)
        )
    closest_edge = world_pos.closest_edge(map.get_all_edges(), camera_scale)
    if closest_edge is not None:
        return PlatformContext(CursorTarget.EDGE, closest_edge, nearest_station)

    
    return PlatformContext(CursorTarget.EMPTY, world_pos, nearest_station)
