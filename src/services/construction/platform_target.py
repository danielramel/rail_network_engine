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
    too_short: bool = False

def find_platform_target(rail_map: RailMap, world_pos: Position, camera_scale) -> PlatformTarget:
    closest_edge = world_pos.closest_edge(rail_map.edges, camera_scale)
    if closest_edge is None:
        return PlatformTarget(kind='none', closest_edge=None)

    if rail_map.is_edge_platform(closest_edge):
        return PlatformTarget(kind='existing_platform', closest_edge=closest_edge)

    edges = rail_map.calculate_platform_preview(closest_edge)
    too_short = False
    try:
        edge = next(iter(edges))
        seg_len = edge[0].distance_to(edge[1])
        if seg_len * len(edges) < PLATFORM_LENGTH * GRID_SIZE:
            too_short = True
    except StopIteration:
        edges = set()
        too_short = True

    return PlatformTarget(kind='preview', closest_edge=closest_edge, edges=edges, too_short=too_short)
