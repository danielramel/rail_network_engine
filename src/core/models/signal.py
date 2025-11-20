from dataclasses import dataclass, field
from core.models.geometry.direction import Direction
from core.models.geometry.edge import Edge
from core.models.geometry.pose import Pose
from core.models.geometry.position import Position

@dataclass
class Signal:
    pose: Pose
    next_signal: 'Signal' = None
    path: list[Edge] = field(default_factory=list)
    _subscriber: callable = None

    def connect(self, path: list[Edge], signal: 'Signal') -> None:
        self.next_signal = signal
        self.path = path
        if self._subscriber is not None:
            self._subscriber(path, signal)
        self._subscriber = None
        
    def subscribe(self, func: callable) -> None:
        if self.next_signal is not None:
            func(self.path, self.next_signal)
            return
        self._subscriber = func
        
    def train_passed(self) -> None:
        self.next_signal = None
        self.path = []
        
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
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Signal':
        return cls(
            pose=Pose.from_dict(data["pose"]["pose"]),
        )
        