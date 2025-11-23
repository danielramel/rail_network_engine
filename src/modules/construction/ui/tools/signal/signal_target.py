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

    if not railway.graph.has_node(snapped) or railway.graph_service.is_junction(snapped) or railway.graph_service.is_curve(snapped):
        if not railway.graph.has_node(snapped):
            message = "No track at this position!"
        elif railway.graph_service.is_junction(snapped):
            message = "Cannot place signal at junctions!"
        else:
            message = "Cannot place signal on curves!"
            
        return SignalTarget(
            kind=SignalTargetType.INVALID,
            pose=Pose(node=snapped, direction=(1, 0)),
            message=message
        )

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
