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
            func = self._subscriber
            self._subscriber = None
            func(self, path, signal)
        
    def subscribe(self, func: Callable) -> None:
        self._subscriber = func
        return self.unsubscribe
    
    def unsubscribe(self) -> None:
        self._subscriber = None
        
    def reached(self) -> None:
        self._subscriber = None
        self.next_signal = None
        self.path = []
        
    def drop(self) -> None:
        self.next_signal = None
        self.path = []

        if self._subscriber is not None:
            func = self._subscriber
            self._subscriber = None
            func()
        
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
        