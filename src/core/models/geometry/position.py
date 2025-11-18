from dataclasses import dataclass, asdict
from core.config.settings import GRID_SIZE, STATION_RECT_SIZE
from math import hypot, floor

from typing import TYPE_CHECKING

from core.models.geometry.direction import Direction
if TYPE_CHECKING:
    from core.models.geometry.edge import Edge


@dataclass(frozen=True, order=True)
class Position:
    x: int
    y: int

    def __post_init__(self):
        # Ensure x and y are integers: if not, round them to nearest int.
        rounded_x = int(round(self.x))
        rounded_y = int(round(self.y))
        object.__setattr__(self, 'x', rounded_x)
        object.__setattr__(self, 'y', rounded_y)
            
    def __iter__(self):
        return iter((self.x, self.y))
    
    def direction_to(self, other: 'Position') -> Direction:
        """Get direction from this point to another point."""
        def signum(x: int) -> int:
            return (x > 0) - (x < 0)
        
        if self == other:
            return ValueError("Same Point")
        if abs(self.x - other.x) / GRID_SIZE > 1 or abs(self.y - other.y) / GRID_SIZE > 1:
            raise ValueError("Points are not adjacent")

        return Direction(signum(other.x - self.x), signum(other.y - self.y))
    
    def heuristic_to(self, other: 'Position') -> float:
        """Use chebysev distance as heuristic for A* pathfinding."""
        return max(abs(self.x - other.x), abs(self.y - other.y)) / GRID_SIZE


    def snap_to_grid(self) -> 'Position':
        """Create a new Point snapped to the grid."""
        snapped_x = round(self.x / GRID_SIZE) * GRID_SIZE
        snapped_y = round(self.y / GRID_SIZE) * GRID_SIZE
        return Position(snapped_x, snapped_y)
    
    def station_rect_overlaps(self, other: 'Position') -> bool:
        """Check if station rectangles at this point and another point overlap."""
        w, h = STATION_RECT_SIZE
        w += GRID_SIZE
        h += GRID_SIZE
        return (
            abs(self.x - other.x) < w and
            abs(self.y - other.y) < h
        )
    
    def is_within_station_rect(self, center: 'Position') -> bool:
        """Check if this point is within the station rectangle centered at another point."""
        w, h = STATION_RECT_SIZE
        return (
            abs(center.x - self.x) * 2 < w + 1 and
            abs(center.y - self.y) * 2 < h + 1
        )
    
    def distance_to(self, other: 'Position') -> float:
        """Calculate the Euclidean distance to another position."""
        return hypot(self.x - other.x, self.y - other.y)
    
    def get_grid_edges(self) -> tuple['Edge']:
        from core.models.geometry.edge import Edge
        """Get the edges of the grid cell containing this position."""
        cell_x = floor(self.x / GRID_SIZE) * GRID_SIZE
        cell_y = floor(self.y / GRID_SIZE) * GRID_SIZE

        corners = (
            Position(cell_x, cell_y),
            Position(cell_x + GRID_SIZE, cell_y),
            Position(cell_x + GRID_SIZE, cell_y + GRID_SIZE),
            Position(cell_x, cell_y + GRID_SIZE),
        )

        return (
            Edge(corners[0], corners[1]),
            Edge(corners[1], corners[2]),
            Edge(corners[2], corners[3]),
            Edge(corners[3], corners[0]),
            Edge(corners[0], corners[2]),
            Edge(corners[1], corners[3]),
        )
    
    def distance_to_edge(self, edge: 'Edge') -> float:
        a, b = edge.a, edge.b
        ax, ay = a.x, a.y
        bx, by = b.x, b.y
        px, py = self.x, self.y
        vx, vy = bx - ax, by - ay
        wx, wy = px - ax, py - ay
        c1 = wx * vx + wy * vy
        if c1 <= 0:
            return ((px - ax)**2 + (py - ay)**2)**0.5
        c2 = vx * vx + vy * vy
        if c2 <= c1:
            return ((px - bx)**2 + (py - by)**2)**0.5
        t = c1 / c2
        cx, cy = ax + t * vx, ay + t * vy
        return ((px - cx)**2 + (py - cy)**2)**0.5
    
    def move(self, dx: int, dy: int) -> 'Position':
        """Return a new Position moved by dx and dy."""
        return Position(self.x + dx, self.y + dy)

    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Position':
        return cls(**data)