from dataclasses import dataclass
from core.models.geometry.direction import Direction
from core.models.geometry.node import Node
from core.models.geometry.position import Position


@dataclass(frozen=True, order=True)
class Edge:
    a: Node
    b: Node

    def __iter__(self):
        return iter((self.a, self.b))
    
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
    
    def tunnel_level(self) -> 'Edge':
        a_other = self.a.tunnel_level()
        b_other = self.b.tunnel_level()
        return Edge(a_other, b_other)
    
    def surface_level(self) -> 'Edge':
        a_other = self.a.surface_level()
        b_other = self.b.surface_level()
        return Edge(a_other, b_other)
    
    def equals_ordered(self, other: 'Edge') -> bool:
        return self.a == other.a and self.b == other.b
    
    def midpoint(self) -> Position:
        return Position((self.a.x + self.b.x) / 2, (self.a.y + self.b.y) / 2)
    
    def is_diagonal(self) -> bool:
        return self.a.x != self.b.x and self.a.y != self.b.y
    
    
    def to_dict_simple(self) -> dict:
        return {
            "a": self.a.to_dict(),
            "b": self.b.to_dict()
            }

    def ordered(self, reversed: bool = False) -> 'Edge':
        return Edge(*sorted((self.a, self.b), reverse=reversed))
    
    def reversed(self) -> 'Edge':
        return Edge(self.b, self.a)
        
    @classmethod
    def from_dict_simple(cls, data: dict) -> 'Edge':
        a = Node.from_dict(data["a"])
        b = Node.from_dict(data["b"])
        return cls(a, b)