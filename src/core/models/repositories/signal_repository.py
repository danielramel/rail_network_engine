from core.models.railway.graph_adapter import GraphAdapter
from core.models.geometry.node import Node
from core.models.geometry.pose import Pose
from core.models.signal import Signal

class SignalRepository:
    """Service responsible for adding / toggling / removing signals."""
    def __init__(self, graph: GraphAdapter):
        self._graph = graph

    def has(self, node: Node) -> bool:
        return self._graph.has_node(node) and self._graph.has_node_attr(node, 'signal')
    
    def has_with_pose(self, pose: Pose) -> bool:
        if not self.has(pose.node):
            return False
        signal = self.get(pose.node)
        return signal.direction == pose.direction
    
    def get(self, node: Node) -> Signal | None:
        if not self.has(node):
            return None
        return self._graph.get_node_attr(node, 'signal')

    def set(self, pose: Pose) -> None:
        self._graph.set_node_attr(pose.node, 'signal', Signal(pose))

    def remove(self, node: Node) -> None:
        self._graph.remove_node_attr(node, 'signal')

    def all(self) -> tuple[Signal]:
        return tuple(self._graph.all_nodes_with_attr('signal').values())
    
    def add_signals_to_dead_ends(self) -> None:
        poses = self._graph.get_dead_end_poses()
        for pose in poses:
            if not self.has_with_pose(pose):
                self.set(pose) # overwrites existing signal if any
        
    
    def to_dict(self):
        return [signal.pose.to_dict() for signal in self.all()]
    
    @classmethod
    def from_dict(cls, graph: GraphAdapter, data: list[dict]) -> 'SignalRepository':
        instance = cls(graph)
        for pose in data:
            instance.set(Pose.from_dict(pose))
            
        return instance