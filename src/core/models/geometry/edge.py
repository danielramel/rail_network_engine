from dataclasses import dataclass
from core.models.geometry.direction import Direction
from core.models.geometry.position import Position


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
        return {self.a, self.b} == {other.a, other.b}
    
    def equals_ordered(self, other: 'Edge') -> bool:
        return self.a == other.a and self.b == other.b
    
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
        
    def ordered(self) -> 'Edge':
        if self.a <= self.b:
            return Edge(self.a, self.b)
        else:
            return Edge(self.b, self.a)

    
    def reversed(self) -> 'Edge':
        return Edge(self.b, self.a)
        
    @classmethod
    def from_dict(cls, data: dict) -> 'Edge':
        a = Position.from_dict(data["a"])
        b = Position.from_dict(data["b"])
        return cls(a, b)