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