from core.models.geometry.edge import Edge
from dataclasses import dataclass

@dataclass
class Rail:
    edge: Edge
    speed: int
    length: int
    
    def reversed(self) -> 'Rail':
        return Rail(self.edge.reversed(), self.speed, self.length)