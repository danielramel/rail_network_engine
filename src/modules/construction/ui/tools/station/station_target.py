from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional
from core.models.geometry.node import Node
from core.models.geometry.position import Position
from core.models.railway.railway_system import RailwaySystem
from core.models.station import Station
class StationTargetType(Enum):
    VALID = auto()
    HOVERED = auto()
    BLOCKED = auto()

@dataclass
class StationTarget:
    kind: StationTargetType
    node: Optional[Node] = None

def find_station_target(railway: RailwaySystem, world_pos: Position, moving_station: Station) -> StationTarget:
    snapped = world_pos.snap_to_grid()

    if not moving_station:
        for station in railway.stations.all():
            if world_pos.is_within_station_rect(station.node):
                return StationTarget(
                    kind=StationTargetType.HOVERED,
                    node=station.node
                )

    if railway.graph_service.is_station_blocked_by_node(snapped) or \
        any(snapped.station_rects_overlap(station.node) for station in railway.stations.all() if station.node != (moving_station.node if moving_station else None)):
            return StationTarget(
                kind=StationTargetType.BLOCKED,
                node=snapped)

    return StationTarget(
        kind=StationTargetType.VALID,
        node=snapped
    )
