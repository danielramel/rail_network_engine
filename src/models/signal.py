from dataclasses import dataclass, field
from models.geometry import Position, Direction
from models.geometry.edge import Edge

@dataclass
class Signal:    
    position: Position
    direction: Direction
    is_green: bool = False
    _subscribers: list[callable] = field(default_factory=list)

    def connect(self, path: list[Edge], signal: 'Signal') -> None:
        self.is_green = True
        for callback in self._subscribers:
            callback(path, signal)
            
        self._subscribers = []
            
    def subscribe(self, callback: callable) -> None:
        self._subscribers.append(callback)