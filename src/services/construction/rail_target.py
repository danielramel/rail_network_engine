from dataclasses import dataclass
from typing import Optional, List
from models.geometry import Position, Pose
from domain.rail_map import RailMap

@dataclass
class RailTarget:
    kind: str                       # 'blocked' | 'node' | 'anchor_same' | 'no_path' | 'path'
    snapped: Position
    construction_anchor: Optional[Pose] = None
    found_path: Optional[List] = None

def find_rail_target(rail_map: RailMap, pos: Position, construction_anchor: Optional[Pose]) -> RailTarget:
    snapped = pos.snap_to_grid()
    if rail_map.is_blocked(snapped):
        return RailTarget(kind='blocked', snapped=snapped, construction_anchor=construction_anchor)

    if construction_anchor is None:
        return RailTarget(kind='node', snapped=snapped, construction_anchor=None)

    if snapped == construction_anchor.position:
        return RailTarget(kind='anchor_same', snapped=snapped, construction_anchor=construction_anchor)

    found_path = rail_map.find_path(construction_anchor, snapped)
    if not found_path:
        return RailTarget(kind='no_path', snapped=snapped, construction_anchor=construction_anchor)

    return RailTarget(kind='path', snapped=snapped, construction_anchor=construction_anchor, found_path=found_path)
