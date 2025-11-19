from core.models.railway.graph_adapter import GraphAdapter
from core.models.geometry import Position, Pose
from core.models.signal import Signal

class SignalRepository:
    """Service responsible for adding / toggling / removing signals."""
    def __init__(self, graph: GraphAdapter):
        self._graph = graph

    def has_signal_at(self, pos: Position) -> bool:
        return self._graph.has_node_at(pos) and self._graph.has_node_attr(pos, 'signal')
    
    def has_signal_with_pose_at(self, pose: Pose) -> bool:
        if not self.has_signal_at(pose.position):
            return False
        signal = self.get(pose.position)
        return signal.direction == pose.direction
    
    def get(self, pos: Position) -> Signal:
        if not self.has_signal_at(pos):
            return None
        return self._graph.get_node_attr(pos, 'signal')

    def set(self, pose: Pose) -> None:
        self._graph.set_node_attr(pose.position, 'signal', Signal(pose))

    def remove(self, pos: Position) -> None:
        self._graph.remove_node_attr(pos, 'signal')

    def all(self) -> tuple[Signal]:
        return tuple(self._graph.all_nodes_with_attr('signal').values())
    
    def add_signals_to_dead_ends(self) -> None:
        poses = self._graph.get_dead_end_poses()
        for pose in poses:
            if not self.has_signal_with_pose_at(pose):
                self.set(pose) # overwrites existing signal if any
        
    
    def to_dict(self):
        return [signal.pose.to_dict() for signal in self.all()]
    
    @classmethod
    def from_dict(cls, graph: GraphAdapter, data: list[dict]) -> 'SignalRepository':
        instance = cls(graph)
        for pose in data:
            instance.set(Pose.from_dict(pose))
            
        return instance