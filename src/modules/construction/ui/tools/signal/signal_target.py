from dataclasses import dataclass
from enum import Enum, auto
from core.models.geometry.pose import Pose

from core.models.geometry.position import Position
from core.models.railway.railway_system import RailwaySystem

class SignalTargetType(Enum):
    INVALID = auto()
    TOGGLE = auto()
    ADD = auto()

@dataclass
class SignalTarget:
    kind: SignalTargetType
    pose: Pose
    message: str | None = None

def find_signal_target(railway: RailwaySystem, pos: Position) -> SignalTarget:
    snapped = pos.snap_to_grid()
    invalid_pose = Pose(node=snapped, direction=(1, 0))
    if not railway.graph.has_node(snapped):
        return SignalTarget(kind=SignalTargetType.INVALID, pose=invalid_pose, message="No track at this position!")

    if railway.graph_service.is_junction(snapped):
        return SignalTarget(kind=SignalTargetType.INVALID, pose=invalid_pose, message="Cannot place signal at junctions!")

    if railway.graph_service.is_curve(snapped):
        return SignalTarget(kind=SignalTargetType.INVALID, pose=invalid_pose, message="Cannot place signal on curves!")
    
    if railway.graph_service.is_tunnel_entry(snapped):
        return SignalTarget(kind=SignalTargetType.INVALID, pose=invalid_pose, message="Cannot place signal at tunnel entrances!")

    if railway.signals.has_signal(snapped):
        toggle_direction = railway.signals.get(snapped).direction.opposite()
        
        if railway.graph.degree_at(snapped) < 2:
            return SignalTarget(
                kind=SignalTargetType.INVALID,
                pose=Pose(node=snapped, direction=toggle_direction),
                message="Cannot toggle signals at dead ends!"
            )
            

        return SignalTarget(
            kind=SignalTargetType.TOGGLE,
            pose=Pose(snapped, toggle_direction),
        )

    # no signal at node -> preview toward first neighbor
    neighbors = sorted(railway.graph.neighbors(snapped), reverse=True)
    
    direction = snapped.direction_to(neighbors[0])
    
    if railway.graph.degree_at(snapped) == 1:
        direction = direction.opposite()
        
    return SignalTarget(
        kind=SignalTargetType.ADD,
        pose=Pose(snapped, direction),
    )
