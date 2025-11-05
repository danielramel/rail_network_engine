from dataclasses import dataclass, asdict
from core.config.settings import BULLDOZE_SENSITIVITY, GRID_SIZE, STATION_RECT_SIZE
from math import hypot

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
        """Calculate the heuristic cost to another position using Chebyshev distance."""
        return max(abs(self.x - other.x), abs(self.y - other.y))

    def snap_to_grid(self) -> 'Position':
        """Create a new Point snapped to the grid."""
        snapped_x = round(self.x / GRID_SIZE) * GRID_SIZE
        snapped_y = round(self.y / GRID_SIZE) * GRID_SIZE
        return Position(snapped_x, snapped_y)
    
    def is_near_grid(self, camera_scale: float) -> bool:
        """Check if this point is near a grid intersection."""
        mod_x = self.x % GRID_SIZE
        mod_y = self.y % GRID_SIZE
        sensitivity = BULLDOZE_SENSITIVITY * 1.2 / camera_scale**0.7
        return (
            (mod_x < sensitivity or mod_x > GRID_SIZE - sensitivity) and 
            (mod_y < sensitivity or mod_y > GRID_SIZE - sensitivity)
        )
    
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
    def closest_point_to_edge(self, edge: 'Edge') -> 'Position':
        """Get the closest point on the line segment defined by edge to this point."""
        a, b = edge
        # Line vector
        dx, dy = b.x - a.x, b.y - a.y
        length_squared = dx*dx + dy*dy

        t = ((self.x - a.x) * dx + (self.y - a.y) * dy) / length_squared
        t = max(0, min(1, t))  # clamp to segment
        
        # Closest point on the segment
        cx, cy = a.x + t * dx, a.y + t * dy
        return Position(cx, cy)

    def intersects_line(self, edge: 'Edge', camera_scale: float) -> tuple[bool, float]:
        """
        Check if this point is within 'BULLDOZE_SENSITIVITY' pixels of line segment ab.
        Returns (is_within_sensitivity, distance).
        """
        closest_point = self.closest_point_to_edge(edge)
        dist = self.distance_to(closest_point)
        
        return dist <= BULLDOZE_SENSITIVITY / camera_scale, dist

    def closest_edge(self, edges: list['Edge'], camera_scale: float) -> 'Edge | None':
        """Get the closest edge from a list of edges to this point."""
        closest_edge = None
        closest_dist = float('inf')
        
        for edge in edges:
            is_within, dist = self.intersects_line(edge, camera_scale)
            if is_within and dist < closest_dist:
                closest_dist = dist
                closest_edge = edge
        
        return closest_edge
    
    
    def distance_to(self, other: 'Position') -> float:
        """Calculate the Euclidean distance to another position."""
        return hypot(self.x - other.x, self.y - other.y)
    
    def move(self, dx: int, dy: int) -> 'Position':
        """Return a new Position moved by dx and dy."""
        return Position(self.x + dx, self.y + dy)

    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Position':
        return cls(**data)