from dataclasses import dataclass
from typing import Optional
from models.geometry import Position
from models.map import RailMap

@dataclass
class StationTarget:
    snapped: Position
    hovered_station_pos: Optional[Position] = None
    blocked_by_node: bool = False
    overlaps_station: bool = False

def find_station_target(rail_map: RailMap, world_pos: Position) -> StationTarget:
    snapped = world_pos.snap_to_grid()

    hovered = None
    for station_pos in rail_map.station_positions:
        if world_pos.is_within_station_rect(station_pos):
            hovered = station_pos
            break

    blocked = any(snapped.is_within_station_rect(node_pos) for node_pos in rail_map.nodes)
    overlaps = any(snapped.station_rect_overlaps(station_pos) for station_pos in rail_map.station_positions)

    return StationTarget(
        snapped=snapped,
        hovered_station_pos=hovered,
        blocked_by_node=blocked,
        overlaps_station=overlaps
    )
