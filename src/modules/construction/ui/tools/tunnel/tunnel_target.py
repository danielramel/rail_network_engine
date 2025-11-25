from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, List
from core.models.geometry.node import Node
from core.models.geometry.pose import Pose
from core.models.geometry.position import Position
from core.models.railway.railway_system import RailwaySystem

class TunnelTargetType(Enum):
    ANCHOR = auto()
    ANCHOR_SAME = auto()
    NO_PATH = auto()
    PATH = auto()
    BLOCKED = auto()

@dataclass
class TunnelTarget:
    kind: TunnelTargetType
    node: Node
    found_path: Optional[List] = None
    message : Optional[str] = None
    anchor: Optional[Pose] = None

def find_tunnel_target(railway: RailwaySystem, world_pos: Position, construction_anchor: Optional[Pose]) -> TunnelTarget:
    snapped = world_pos.snap_to_grid()
    
    if railway.stations.is_within_any(snapped):
        return TunnelTarget(kind=TunnelTargetType.BLOCKED, node=snapped, message="Cannot build tunnel through station!")

    if not railway.graph.has_node(snapped):
        return TunnelTarget(kind=TunnelTargetType.BLOCKED, node=snapped, message="Tunnel has to start/end on existing section endpoint!")
    
    if railway.graph_service.is_tunnel_entry(snapped):
        return TunnelTarget(kind=TunnelTargetType.BLOCKED, node=snapped, message="Cannot build tunnel on tunnel entry/exit!")
    
    if railway.graph.degree_at(snapped) != 1:
        return TunnelTarget(kind=TunnelTargetType.BLOCKED, node=snapped, message="Tunnel has to connect to section endpoint!")
    
    if construction_anchor is not None and snapped == construction_anchor.node:
        return TunnelTarget(kind=TunnelTargetType.ANCHOR_SAME, node=snapped)
    
    if railway.signals.has(snapped):
        return TunnelTarget(kind=TunnelTargetType.BLOCKED, node=snapped, message="Please remove the signal first!")        
    neighbor = railway.graph.neighbors(snapped)[0]
    
    if construction_anchor is None:
        return TunnelTarget(kind=TunnelTargetType.ANCHOR, anchor=Pose.from_nodes(neighbor, snapped), node=snapped)

    
    found_path = railway.pathfinder.find_tunnel_path(construction_anchor, Pose.from_nodes(snapped, neighbor).get_previous_in_direction())
    if found_path is None:
        return TunnelTarget(kind=TunnelTargetType.NO_PATH, node=snapped)
    
    return TunnelTarget(kind=TunnelTargetType.PATH, node=snapped, found_path=found_path)