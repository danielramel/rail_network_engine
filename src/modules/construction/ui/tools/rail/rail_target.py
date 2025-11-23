from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional
from core.models.geometry.direction import Direction
from core.models.geometry.node import Node
from core.models.geometry.pose import Pose
from core.models.geometry.position import Position
from core.models.railway.railway_system import RailwaySystem

class RailTargetType(Enum):
    ANCHOR = auto()
    ANCHOR_SAME = auto()
    NO_PATH = auto()
    PATH = auto()
    BLOCKED = auto()

@dataclass
class RailTarget:
    kind: RailTargetType
    node: Node
    found_path: Optional[tuple[Node]] = None
    anchor: Optional[Pose] = None

def find_rail_target(railway: RailwaySystem, world_pos: Position, construction_anchor: Optional[Pose]) -> RailTarget:
    snapped = world_pos.snap_to_grid()
    
    if railway.pathfinder.is_node_blocked(snapped):
        return RailTarget(kind=RailTargetType.BLOCKED, node=snapped)

    if construction_anchor is None:
        if railway.signals.has_signal(snapped):
            signal = railway.signals.get(snapped)
            return RailTarget(kind=RailTargetType.ANCHOR, node=snapped, anchor=signal.pose)
        return RailTarget(kind=RailTargetType.ANCHOR, node=snapped, anchor=Pose(snapped, Direction(0, 0)))

    if snapped.x == construction_anchor.node.x and snapped.y == construction_anchor.node.y:
        return RailTarget(kind=RailTargetType.ANCHOR_SAME, node=snapped)
    
    found_path = railway.pathfinder.find_grid_path(construction_anchor, snapped)
    if found_path is None:
        return RailTarget(kind=RailTargetType.NO_PATH, node=snapped)

    return RailTarget(kind=RailTargetType.PATH, node=snapped, found_path=found_path)
