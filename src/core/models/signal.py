from dataclasses import dataclass, field
from core.models.geometry.direction import Direction
from core.models.geometry.edge import Edge
from core.models.geometry.pose import Pose
from core.models.geometry.position import Position
from typing import Optional

@dataclass
class Signal:
    pose: Pose
    next_signal: Optional['Signal'] = None
    path: list[Edge] = field(default_factory=list)
    _subscribers: list[callable] = field(default_factory=list)

    def connect(self, path: list[Edge], signal: 'Signal') -> None:
        self.next_signal = signal
        self.path = path
        for callback in self._subscribers:
            callback(path, signal)
            
        self._subscribers = []
        
    def disconnect(self) -> None:
        self.next_signal = None
        self.path = []
            
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
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Signal':
        return cls(
            pose=Pose.from_dict(data["pose"]["pose"]),
        )
        