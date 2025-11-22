from dataclasses import dataclass
from typing import Optional
from core.models.geometry import Position
from core.models.railway.railway_system import RailwaySystem
from core.models.station import Station

@dataclass
class StationTarget:
    snapped: Position
    hovered_station_pos: Optional[Position] = None
    blocked_by_node: bool = False
    overlaps_station: bool = False

def find_station_target(railway: RailwaySystem, world_pos: Position, moving_station: Station) -> StationTarget:
    snapped = world_pos.snap_to_grid()

    hovered = None
    for station in railway.stations.all():
        if world_pos.is_within_station_rect(station.position):
            hovered = station.position
            break

    blocked = any(snapped.is_within_station_rect(node_pos) for node_pos in railway.graph.nodes)
    overlaps = any(snapped.station_rects_overlap(station.position) for station in railway.stations.all() if station.position != (moving_station.position if moving_station else None))

    return StationTarget(
        snapped=snapped,
        hovered_station_pos=hovered,
        blocked_by_node=blocked,
        overlaps_station=overlaps
    )
