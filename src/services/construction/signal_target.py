from dataclasses import dataclass
from enum import Enum
from typing import Optional
from models.geometry import Position, Pose
from models.simulation import Simulation

class SignalTargetType(Enum):
    INVALID = 0
    DEAD_END = 1
    TOGGLE = 2
    ADD = 3

@dataclass
class SignalTarget:
    kind: SignalTargetType
    snapped: Position
    preview_pose: Optional[Pose] = None
    offset: bool = False

def find_signal_target(rail_map: Simulation, pos: Position) -> SignalTarget:
    snapped = pos.snap_to_grid()

    if not rail_map.graph.has_node_at(snapped) or rail_map.graph.is_junction(snapped):
        return SignalTarget(
            kind=SignalTargetType.INVALID,
            snapped=snapped,
            preview_pose=Pose(position=snapped, direction=(-1, 0)),
            offset=True
        )

    if rail_map.signals.has_signal_at(snapped):
        if rail_map.graph.degree_at(snapped) == 1:
            return SignalTarget(
                kind=SignalTargetType.DEAD_END,
                snapped=snapped,
                preview_pose=Pose(position=snapped, direction=rail_map._graph.nodes[snapped]['signal']),
                offset=True
            )

        current_direction = rail_map._graph.nodes[snapped]['signal']
        neighbors = tuple(rail_map._graph.neighbors(snapped))
        if snapped.direction_to(neighbors[0]) == current_direction:
            new_dir = snapped.direction_to(neighbors[1])
        else:
            new_dir = snapped.direction_to(neighbors[0])

        return SignalTarget(
            kind=SignalTargetType.TOGGLE,
            snapped=snapped,
            preview_pose=Pose(position=snapped, direction=new_dir),
            offset=True
        )

    # no signal at node -> preview toward first neighbor
    neighbor = next(rail_map._graph.neighbors(snapped))
    return SignalTarget(
        kind=SignalTargetType.ADD,
        snapped=snapped,
        preview_pose=Pose(position=snapped, direction=snapped.direction_to(neighbor)),
        offset=False
    )
