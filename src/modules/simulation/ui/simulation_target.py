from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from core.graphics.camera import Camera
from core.models.geometry.position import Position
from core.models.railway.railway_system import RailwaySystem
from core.models.signal import Signal

class SimulationTargetType(Enum):
    NODE = auto()
    TRAIN = auto()
    SIGNAL = auto()
    OUT_OF_BOUNDS = auto()
    NONE = auto()

@dataclass
class SimulationTarget:
    kind: SimulationTargetType
    train_id: Optional[int] = None
    signal: Optional[Signal] = None
    node: Optional[Position] = None
    
def find_simulation_target(railway: RailwaySystem, world_pos: Position) -> SimulationTarget:
    if world_pos is None:
        return SimulationTarget(SimulationTargetType.OUT_OF_BOUNDS)
    closest_edge = railway.graph_service.get_closest_edge(world_pos)
    train_id = railway.trains.get_train_on_edge(closest_edge)
    if train_id:
        return SimulationTarget(SimulationTargetType.TRAIN, train_id)

    snapped = world_pos.snap_to_grid()
    if railway.signals.has(snapped):
        return SimulationTarget(SimulationTargetType.SIGNAL, signal=railway.signals.get(snapped))
    
    if railway.graph.has_node(snapped):
        return SimulationTarget(SimulationTargetType.NODE, node=snapped)

    return SimulationTarget(SimulationTargetType.NONE, node=snapped)