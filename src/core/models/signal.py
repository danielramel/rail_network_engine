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
    railway: 'RailwaySystem'
    next_signal: Optional['Signal'] = None
    path: list[Edge] = field(default_factory=list)
    _release_subscriber: Callable = None
    _drop_subscriber: Callable = None
    _passed_subscriber: Callable = None
    is_continuous: bool = False
    automatically_reconnect: Optional[tuple[list[Edge], 'Signal', Callable]] = None
    
    def __init__(self, pose: Pose, railway: 'RailwaySystem') -> None:
        self.pose = pose
        self._railway = railway
        

    def connect(self, path: list[Edge], next_signal: 'Signal', init_automatic_connection: bool) -> None:
        self.next_signal = next_signal
        self.path = path
        if self._release_subscriber is not None:
            self._release_subscriber(self)
            
        if init_automatic_connection:
            unsubscribe = next_signal.passed_subscribe(self.auto_reconnect)
            self.automatically_reconnect = (path, next_signal, unsubscribe)
        
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
        self.automatically_reconnect[2]()  # Call the unsubscribe function
        self.automatically_reconnect = None
            
    def auto_reconnect(self) -> None:
        if self.automatically_reconnect is not None:
            path, next_signal, _ = self.automatically_reconnect
            self.connect(path, next_signal, False)
            self._railway.signalling.lock_path(path)
        
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
        