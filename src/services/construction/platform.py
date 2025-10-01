
from models.geometry import Position
from models.map import RailMap
from models.construction import CursorTarget
from dataclasses import dataclass

@dataclass
class PlatformContext:
    type: CursorTarget
    data: Position | tuple[Position, Position]
    nearest_station: Position | None

def get_platform_context(map: RailMap, world_pos: Position, camera_scale: float) -> PlatformContext:
    nearest_station = min(map.get_all_stations().keys(), key=lambda s: ((s.x - world_pos.x) ** 2 + (s.y - world_pos.y) ** 2) ** 0.5, default=None)

    for edge in map.get_all_edges():
        if world_pos.intersects_line(edge, camera_scale):
            return PlatformContext(CursorTarget.EDGE, edge, nearest_station)

    
    return PlatformContext(CursorTarget.EMPTY, world_pos, nearest_station)
