from dataclasses import dataclass
from enum import Enum
from typing import Optional
from models.geometry import Position, Pose
from models.railway_system import RailwaySystem

class SignalTargetType(Enum):
    INVALID = 0
    TOGGLE = 2
    ADD = 3

@dataclass
class SignalTarget:
    kind: SignalTargetType
    pose: Pose
    offset: bool = False

def find_signal_target(railway: RailwaySystem, pos: Position) -> SignalTarget:
    snapped = pos.snap_to_grid()

    if not railway.graph.has_node_at(snapped) or railway.graph.is_junction(snapped):
        return SignalTarget(
            kind=SignalTargetType.INVALID,
            pose=Pose(position=snapped, direction=(1, 0)),
            offset=True
        )

    if railway.signals.has_signal_at(snapped):
        if railway.graph.degree_at(snapped) == 1:
                pose=Pose(position=snapped, direction=railway._graph.nodes[snapped]['signal'].direction),

        current_direction = railway._graph.nodes[snapped]['signal'].direction
        neighbors = railway.graph.neighbors(snapped)
        direction = snapped.direction_to(neighbors[0])
        if direction == current_direction and railway.graph.degree_at(snapped) == 2:
            direction = snapped.direction_to(neighbors[1])

        return SignalTarget(
            kind=SignalTargetType.TOGGLE,
            pose=Pose(snapped, direction),
            offset=True
        )

    # no signal at node -> preview toward first neighbor
    neighbors = sorted(railway.graph.neighbors(snapped), reverse=True)
    
    direction = snapped.direction_to(neighbors[0])
    
    if railway.graph.degree_at(snapped) == 1:
        direction = direction.get_opposite()
        
    return SignalTarget(
        kind=SignalTargetType.ADD,
        pose=Pose(snapped, direction),
        offset=False
    )
