from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional
from core.models.geometry.direction import Direction
from core.models.geometry.node import Node
from core.models.geometry.pose import Pose
from core.models.geometry.position import Position
from core.models.railway.railway_system import RailwaySystem

class TrackTargetType(Enum):
    ANCHOR = auto()
    ANCHOR_SAME = auto()
    NO_PATH = auto()
    PATH = auto()
    BLOCKED = auto()

@dataclass
class TrackTarget:
    kind: TrackTargetType
    node: Node
    found_path: Optional[tuple[Node]] = None
    anchor: Optional[Pose] = None

def find_track_target(railway: RailwaySystem, world_pos: Position, construction_anchor: Optional[Pose]) -> TrackTarget:
    snapped = world_pos.snap_to_grid()
    
    if railway.pathfinder.is_node_blocked(snapped):
        return TrackTarget(kind=TrackTargetType.BLOCKED, node=snapped)

    if construction_anchor is None:
        if railway.signals.has(snapped):
            signal = railway.signals.get(snapped)
            return TrackTarget(kind=TrackTargetType.ANCHOR, node=snapped, anchor=signal.pose)
        return TrackTarget(kind=TrackTargetType.ANCHOR, node=snapped, anchor=Pose(snapped, Direction(0, 0)))

    if snapped.x == construction_anchor.node.x and snapped.y == construction_anchor.node.y:
        return TrackTarget(kind=TrackTargetType.ANCHOR_SAME, node=snapped)
    
    found_path = railway.pathfinder.find_grid_path(construction_anchor, snapped)
    if found_path is None:
        return TrackTarget(kind=TrackTargetType.NO_PATH, node=snapped)

    return TrackTarget(kind=TrackTargetType.PATH, node=snapped, found_path=found_path)
