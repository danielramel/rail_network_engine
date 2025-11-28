from dataclasses import dataclass, field
from core.models.geometry.pose import Pose
from core.models.geometry.edge import Edge
from core.models.geometry.direction import Direction
from core.models.geometry.node import Node
from typing import Callable, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem

@dataclass
class Signal:
    pose: Pose
    next_signal: Optional['Signal'] = None
    path: list[Edge] = field(default_factory=list)
    _release_subscriber: Callable = None
    _drop_subscriber: Callable = None
    _passed_subscriber: Callable = None
        
    def connect(self, path: list[Edge], next_signal: 'Signal') -> None:
        self.next_signal = next_signal
        self.path = path
        if self._release_subscriber is not None:
            self._release_subscriber(self)
        
    def subscribe_release(self, func: Callable) -> Callable:
        self._release_subscriber = func
        def unsubscribe():
            self._release_subscriber = None
        return unsubscribe
    
    def passed_subscribe(self, func: Callable) -> Callable:
        self._passed_subscriber = func
        def unsubscribe():
            self._passed_subscriber = None
        return unsubscribe
    
    def subscribe_drop(self, func: Callable) -> None:
        self._drop_subscriber = func
        
    def reached(self) -> None:
        self._release_subscriber = None
        self.next_signal = None
        self.path = []
        
    def passed(self) -> None:
        if self._passed_subscriber is not None:
            self._passed_subscriber()
        
    def drop(self) -> None:
        self.next_signal = None
        self.path = []

        if self._drop_subscriber is not None:
            func = self._drop_subscriber
            self._drop_subscriber = None
            func()
            
    def reset(self) -> None:
        self.next_signal = None
        self.path = []
        self._release_subscriber = None
        self._passed_subscriber = None
        self._drop_subscriber = None
            
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
        