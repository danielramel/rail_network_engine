from dataclasses import dataclass
from .position import Position

@dataclass(frozen=True, order=True)
class Edge:
    a: Position
    b: Position
    length: float = 0.0

    def __post_init__(self):
        object.__setattr__(self, 'length', self.a.distance_to(self.b))

    def __iter__(self):
        return iter((self.a, self.b))

    def __hash__(self):
        # Make it hashable independent of endpoint order
        return hash(frozenset((self.a, self.b)))

    def __eq__(self, other):
        if not isinstance(other, Edge):
            return NotImplemented
        return frozenset((self.a, self.b)) == frozenset((other.a, other.b))
    
    def midpoint(self) -> Position:
        return Position((self.a.x + self.b.x) / 2, (self.a.y + self.b.y) / 2)
