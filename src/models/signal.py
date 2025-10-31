from dataclasses import dataclass, field
from models.geometry import Position, Direction

@dataclass
class Signal:    
    position: Position
    direction: Direction
    next_signal : 'Signal' = None
    _subscribers: list[callable] = field(default_factory=list)
        
    def connect(self, next_signal: 'Signal') -> None:
        self.next_signal = next_signal
        for callback in self._subscribers:
            callback(next_signal)
            
    @property
    def is_green(self):
        return self.next_signal is not None
            
    def subscribe(self, callback: callable) -> None:
        self._subscribers.append(callback)