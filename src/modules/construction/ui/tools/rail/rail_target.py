from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, List
from core.models.geometry.node import Node
from core.models.geometry.pose import Pose
from core.models.geometry.position import Position
from core.models.railway.railway_system import RailwaySystem

class RailTargetType(Enum):
    NODE = auto()
    ANCHOR_SAME = auto()
    NO_PATH = auto()
    PATH = auto()
    BLOCKED = auto()
@dataclass
class RailTarget:
    kind: RailTargetType
    node: Node
    found_path: Optional[List] = None

def find_rail_target(railway: RailwaySystem, screen_pos: Position, construction_anchor: Optional[Pose]) -> RailTarget:
    node = screen_pos.snap_to_grid()
    if railway.stations.is_within_any(node):
        return RailTarget(kind=RailTargetType.BLOCKED, node=node)

    if construction_anchor is None:
        return RailTarget(kind=RailTargetType.NODE, node=node)

    if node == construction_anchor.node:
        return RailTarget(kind=RailTargetType.ANCHOR_SAME, node=node)

    found_path = railway.find_path(construction_anchor, node)
    if not found_path:
        return RailTarget(kind=RailTargetType.NO_PATH, node=node)

    return RailTarget(kind=RailTargetType.PATH, node=node, found_path=found_path)
