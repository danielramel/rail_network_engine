from dataclasses import dataclass, field
from core.models.geometry.pose import Pose
from core.models.geometry.edge import Edge
from core.models.geometry.direction import Direction
from core.models.geometry.node import Node
from typing import Callable

@dataclass
class Signal:
    pose: Pose
    next_signal: 'Signal' = None
    path: list[Edge] = field(default_factory=list)
    _subscriber: Callable = None

    def connect(self, path: list[Edge], signal: 'Signal') -> None:
        self.next_signal = signal
        self.path = path
        if self._subscriber is not None:
            self._subscriber(path, signal)
        self._subscriber = None
        
    def subscribe(self, func: Callable) -> None:
        if self.next_signal is not None:
            func(self.path, self.next_signal)
            return self.unsubscribe
        self._subscriber = func
        return self.unsubscribe
    
    def unsubscribe(self) -> None:
        self._subscriber = None
        
    def passed(self) -> None:
        self.next_signal = None
        self.path = []
        
    @property
    def direction(self) -> Direction:
        return self.pose.direction
    
    @property
    def node(self) -> Node:
        return self.pose.node
    
    def to_dict(self) -> dict:
        return {
            "pose": self.pose.to_dict(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Signal':
        return cls(
            pose=Pose.from_dict(data["pose"]["pose"]),
        )
        