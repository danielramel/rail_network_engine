from dataclasses import dataclass
from typing import Optional
from models.geometry import Position, Pose
from domain.rail_map import RailMap

@dataclass
class SignalTarget:
    kind: str                       # 'invalid' | 'dead_end' | 'toggle' | 'add'
    snapped: Position
    preview_pose: Optional[Pose] = None
    offset: bool = False

def find_signal_target(rail_map: RailMap, pos: Position) -> SignalTarget:
    snapped = pos.snap_to_grid()

    if not rail_map.has_node_at(snapped) or rail_map.is_junction(snapped):
        return SignalTarget(
            kind='invalid',
            snapped=snapped,
            preview_pose=Pose(position=snapped, direction=(-1, 0)),
            offset=True
        )

    if rail_map.has_signal_at(snapped):
        if rail_map.degree_at(snapped) == 1:
            return SignalTarget(
                kind='dead_end',
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
            kind='toggle',
            snapped=snapped,
            preview_pose=Pose(position=snapped, direction=new_dir),
            offset=True
        )

    # no signal at node -> preview toward first neighbor
    neighbor = next(rail_map._graph.neighbors(snapped))
    return SignalTarget(
        kind='add',
        snapped=snapped,
        preview_pose=Pose(position=snapped, direction=snapped.direction_to(neighbor)),
        offset=False
    )
