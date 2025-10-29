from dataclasses import dataclass, field
from models.geometry import Position, Direction

@dataclass
class Signal:    
    position: Position
    direction: Direction
    allowed: bool = False
    _subscribers: list[callable] = field(default_factory=list)
        
    def allow(self) -> None:
        self.allowed = True
        
        for callback in self._subscribers:
            callback()
            
    def subscribe(self, callback: callable) -> None:
        self._subscribers.append(callback)