from core.models.railway.graph_adapter import GraphAdapter
from core.models.geometry.node import Node
from core.models.geometry.pose import Pose
from core.models.signal import Signal
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem

class SignalRepository:
    """Service responsible for adding / toggling / removing signals."""
    def __init__(self, railway: 'RailwaySystem'):
        self._railway = railway

    def has(self, node: Node) -> bool:
        return self._railway.graph.has_node(node) and self._railway.graph.has_node_attr(node, 'signal')
    
    def has_with_pose(self, pose: Pose) -> bool:
        if not self.has(pose.node):
            return False
        signal = self.get(pose.node)
        return signal.direction == pose.direction
    
    def get(self, node: Node) -> Signal | None:
        if not self.has(node):
            return None
        return self._railway.graph.get_node_attr(node, 'signal')

    def set(self, pose: Pose) -> None:
        self._railway.graph.set_node_attr(pose.node, 'signal', Signal(pose))

    def remove(self, node: Node) -> None:
        self._railway.graph.remove_node_attr(node, 'signal')

    def all(self) -> tuple[Signal]:
        return tuple(self._railway.graph.all_nodes_with_attr('signal').values())
        
    def to_dict(self):
        return [signal.pose.to_dict() for signal in self.all()]
    
    @classmethod
    def from_dict(cls, railway: 'RailwaySystem', data: list[dict]) -> 'SignalRepository':
        instance = cls(railway)
        for signal_pose in data:
            instance.set(Pose.from_dict(signal_pose))
        return instance