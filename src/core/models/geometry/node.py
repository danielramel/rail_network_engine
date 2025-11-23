from dataclasses import dataclass, asdict
from math import hypot
from core.config.settings import Config
from core.models.geometry.direction import Direction

@dataclass(frozen=True, order=True)
class Node:
    x: int
    y: int
    level: int = 0
    
    def __post_init__(self):
        if not isinstance(self.x, int):
            raise TypeError("x must be int")
        if not isinstance(self.y, int):
            raise TypeError("y must be int")
    
    def distance_to(self, other: 'Node') -> float:
        """Calculate the Euclidean distance to another node."""
        return hypot(self.x - other.x, self.y - other.y)
    
    def heuristic_to(self, other: 'Node') -> float:
        """Use chebysev distance as heuristic for A* pathfinding."""
        return max(abs(self.x - other.x), abs(self.y - other.y))

    
    def station_rects_overlap(self, other: 'Node') -> bool:
        """Check if station rectangles at this point and another point overlap."""
        return (
            abs(self.x - other.x) < Config.STATION_RECT_WIDTH + 1 and
            abs(self.y - other.y) < Config.STATION_RECT_HEIGHT + 1
        )
        
    def tunnel_level(self) -> 'Node':
        return Node(self.x, self.y, level=1)
    
    def surface_level(self) -> 'Node':
        return Node(self.x, self.y, level=0)

    
    def direction_to(self, other: 'Node') -> Direction:
        """Get direction from this point to another point."""
        def signum(x: int) -> int:
            return (x > 0) - (x < 0)
        
        if self == other:
            return ValueError("Same Point")
        if abs(self.x - other.x) > 1 or abs(self.y - other.y) > 1:
            raise ValueError("Points are not adjacent")

        return Direction(signum(other.x - self.x), signum(other.y - self.y))
    
    def is_within_station_rect(self, center: 'Node') -> bool:
        return (
            abs(center.x - self.x) * 2 < Config.STATION_RECT_WIDTH + 1 and
            abs(center.y - self.y) * 2 < Config.STATION_RECT_HEIGHT + 1
        )
    
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Node':
        return cls(**data)