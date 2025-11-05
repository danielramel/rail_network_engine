from dataclasses import dataclass
from enum import Enum
from typing import Optional, List
from core.models.geometry import Position, Pose
from core.models.railway.railway_system import RailwaySystem

class RailTargetType(Enum):
    NODE = 1
    ANCHOR_SAME = 2
    NO_PATH = 3
    PATH = 4
    BLOCKED = 5

@dataclass
class RailTarget:
    kind: RailTargetType
    snapped: Position
    found_path: Optional[List] = None

def find_rail_target(railway: RailwaySystem, screen_pos: Position, construction_anchor: Optional[Pose]) -> RailTarget:
    snapped = screen_pos.snap_to_grid()
    if railway._pathfinder.is_blocked(snapped):
        return RailTarget(kind=RailTargetType.BLOCKED, snapped=snapped)

    if construction_anchor is None:
        return RailTarget(kind=RailTargetType.NODE, snapped=snapped)

    if snapped == construction_anchor.position:
        return RailTarget(kind=RailTargetType.ANCHOR_SAME, snapped=snapped)

    found_path = railway.find_path(construction_anchor, snapped)
    if not found_path:
        return RailTarget(kind=RailTargetType.NO_PATH, snapped=snapped)

    return RailTarget(kind=RailTargetType.PATH, snapped=snapped, found_path=found_path)
