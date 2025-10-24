from dataclasses import dataclass
from typing import Optional
from models.geometry import Position
from models.simulation import Simulation
from models.station import Station

@dataclass
class StationTarget:
    snapped: Position
    hovered_station_pos: Optional[Position] = None
    blocked_by_node: bool = False
    overlaps_station: bool = False

def find_station_target(simulation: Simulation, world_pos: Position, moving_station: Station) -> StationTarget:
    snapped = world_pos.snap_to_grid()

    hovered = None
    for station in simulation.stations.all():
        if world_pos.is_within_station_rect(station.position):
            hovered = station.position
            break

    blocked = any(snapped.is_within_station_rect(node_pos) for node_pos in simulation.graph.nodes)
    overlaps = any(snapped.station_rect_overlaps(station.position) for station in simulation.stations.all() if station.position != (moving_station.position if moving_station else None))

    return StationTarget(
        snapped=snapped,
        hovered_station_pos=hovered,
        blocked_by_node=blocked,
        overlaps_station=overlaps
    )
