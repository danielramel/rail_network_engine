from dataclasses import dataclass
from .position import Position


@dataclass(frozen=True)
class Edge:
    a: Position
    b: Position

    def __post_init__(self):
        # Ensure consistent ordering for a and b
        if self.b < self.a:
            self.a, self.b = self.b, self.a