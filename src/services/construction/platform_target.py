# services/platform_tool.py
from dataclasses import dataclass
from typing import Optional, Set, Any
from config.settings import PLATFORM_LENGTH, GRID_SIZE
from models.geometry import Position
from domain.rail_map import RailMap

@dataclass
class PlatformTarget:
    kind: str                    # 'none' | 'existing_platform' | 'preview'
    closest_edge: Optional[Any] = None
    edges: Optional[Set[Any]] = None
    is_valid: bool = False

def find_platform_target(rail_map: RailMap, world_pos: Position, camera_scale) -> PlatformTarget:
    closest_edge = world_pos.closest_edge(rail_map.edges, camera_scale)
    if closest_edge is None:
        return PlatformTarget(kind='none', closest_edge=None)

    if rail_map.is_edge_platform(closest_edge):
        return PlatformTarget(kind='existing_platform', closest_edge=closest_edge)

    is_valid, edges = rail_map.calculate_platform_preview(closest_edge)
    

    return PlatformTarget(kind='preview', closest_edge=closest_edge, edges=edges, is_valid=is_valid)
