from dataclasses import dataclass
from models.geometry.direction import Direction
from models.geometry.position import Position


@dataclass(frozen=True, order=True)
class Edge:
    a: Position
    b: Position
    def __iter__(self):
        return iter((self.a, self.b))
    
    @property
    def length(self) -> float:
        return self.a.distance_to(self.b)
    
    @property
    def direction(self) -> Direction:
        return self.a.direction_to(self.b)

    def __hash__(self):
        # Make it hashable independent of endpoint order
        return hash(frozenset((self.a, self.b)))

    def __eq__(self, other):
        if not isinstance(other, Edge):
            return NotImplemented
        return frozenset((self.a, self.b)) == frozenset((other.a, other.b))
    
    def midpoint(self) -> Position:
        return Position((self.a.x + self.b.x) / 2, (self.a.y + self.b.y) / 2)

    def move(self, direction: Direction, distance: float) -> 'Edge':
        new_a = Position(self.a.x + direction.x * distance, self.a.y + direction.y * distance)
        new_b = Position(self.b.x + direction.x * distance, self.b.y + direction.y * distance)
        return Edge(new_a, new_b)
    
    def to_dict(self) -> dict:
        return {
            "a": self.a.to_dict(),
            "b": self.b.to_dict(),
            "length": self.length
        }
        
    @classmethod
    def from_dict(cls, data: dict) -> 'Edge':
        a = Position.from_dict(data["a"])
        b = Position.from_dict(data["b"])
        return cls(a, b)