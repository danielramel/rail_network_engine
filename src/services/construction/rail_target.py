from dataclasses import dataclass
from enum import Enum
from typing import Optional, List
from models.geometry import Position, Pose
from models.railway_system import RailwaySystem

class RailTargetType(Enum):
    NODE = 1
    ANCHOR_SAME = 2
    NO_PATH = 3
    PATH = 4

@dataclass
class RailTarget:
    kind: RailTargetType
    snapped: Position
    construction_anchor: Optional[Pose] = None
    found_path: Optional[List] = None

def find_rail_target(railway: RailwaySystem, screen_pos: Position, construction_anchor: Optional[Pose]) -> RailTarget:
    snapped = screen_pos.snap_to_grid()

    if construction_anchor is None:
        return RailTarget(kind=RailTargetType.NODE, snapped=snapped, construction_anchor=None)

    if snapped == construction_anchor.position:
        return RailTarget(kind=RailTargetType.ANCHOR_SAME, snapped=snapped, construction_anchor=construction_anchor)

    found_path = railway.find_path(construction_anchor, snapped)
    if not found_path:
        return RailTarget(kind=RailTargetType.NO_PATH, snapped=snapped, construction_anchor=construction_anchor)

    return RailTarget(kind=RailTargetType.PATH, snapped=snapped, construction_anchor=construction_anchor, found_path=found_path)
