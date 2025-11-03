from dataclasses import dataclass, field
from models.geometry.direction import Direction
from models.geometry.edge import Edge
from models.geometry.pose import Pose
from models.geometry.position import Position

@dataclass
class Signal:    
    pose: Pose
    is_green: bool = False
    _subscribers: list[callable] = field(default_factory=list)

    def connect(self, path: list[Edge], signal: 'Signal') -> None:
        self.is_green = True
        for callback in self._subscribers:
            callback(path, signal)
            
        self._subscribers = []
            
    def subscribe(self, callback: callable) -> None:
        self._subscribers.append(callback)
        
    @property
    def direction(self) -> Direction:
        return self.pose.direction
    
    @property
    def position(self) -> Position:
        return self.pose.position
    
    def to_dict(self) -> dict:
        return {
            "pose": self.pose.to_dict(),
        }
        
    def from_dict(data: dict) -> 'Signal':
        return Signal(
            pose=Pose.from_dict(data["pose"]),
        )
        
        
        
from models.graph_adapter import GraphAdapter

class SignalRepository:
    """Service responsible for adding / toggling / removing signals."""
    def __init__(self, graph: GraphAdapter):
        self._graph = graph

    def has_signal_at(self, pos: Position) -> bool:
        return self._graph.has_node_attr(pos, 'signal')
    
    def get(self, pos: Position) -> Signal:
        return self._graph.get_node_attr(pos, 'signal')

    def add(self, pose: Pose) -> None:
        self._graph.set_node_attr(pose.position, 'signal', Signal(pose))

    def remove(self, pos: Position) -> None:
        self._graph.remove_node_attr(pos, 'signal')

    def toggle(self, pose: Pose) -> None:
        self.remove(pose.position)
        self.add(pose)

    def all(self) -> tuple[Signal]:
        return tuple(self._graph.all_nodes_with_attr('signal').values())