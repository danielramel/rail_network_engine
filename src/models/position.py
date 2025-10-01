from dataclasses import dataclass
from typing import NamedTuple
from config.settings import BULLDOZE_SENSITIVITY, GRID_SIZE, STATION_RECT_SIZE
from math import hypot


@dataclass(frozen=True, order=True)
class Position:
    x: float
    y: float
   
    def __iter__(self):
        return iter((self.x, self.y))
    
    def direction_to(self, other: 'Position') -> tuple[int, int]:
        """Get direction from this point to another point."""
        def signum(x: float) -> int:
            return (x > 0) - (x < 0)
        
        if self == other:
            return ValueError("Same Point")
        if abs(self.x - other.x) / GRID_SIZE > 1 or abs(self.y - other.y) / GRID_SIZE > 1:
            raise ValueError("Points are not adjacent")
       
        return (signum(other.x - self.x), signum(other.y - self.y))
    
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
    
    def within_station_rect(self, center: 'Position') -> bool:
        """Check if this point is within the station rectangle centered at another point."""
        w, h = STATION_RECT_SIZE
        w += GRID_SIZE
        h += GRID_SIZE
        return (
            abs(center.x - self.x) * 2 < w and
            abs(center.y - self.y) * 2 < h
        )

    def intersects_line(self, edge: tuple['Position', 'Position'], camera_scale: float) -> tuple[bool, float]:
        """
        Check if this point is within 'BULLDOZE_SENSITIVITY' pixels of line segment ab.
        Returns (is_within_sensitivity, distance).
        """
        a, b = edge
        # Line vector
        dx, dy = b.x - a.x, b.y - a.y
        length_squared = dx*dx + dy*dy

        t = ((self.x - a.x) * dx + (self.y - a.y) * dy) / length_squared
        t = max(0, min(1, t))  # clamp to segment
        
        # Closest point on the segment
        cx, cy = a.x + t * dx, a.y + t * dy
        
        # Distance from this point to that closest point
        dist = hypot(self.x - cx, self.y - cy)
        return dist <= BULLDOZE_SENSITIVITY / camera_scale, dist
    
    def midpoint(self, other: 'Position') -> 'Position':
        """Return the midpoint between this position and another."""
        return Position((self.x + other.x) / 2, (self.y + other.y) / 2)
    

class Pose(NamedTuple):
    """PointWithDirection represents a position and the direction we arrived from."""
    position: Position
    direction: tuple[int, int]  # (dx, dy) normalized direction
    
    @classmethod
    def from_positions(cls, previous: Position, current: Position) -> 'Pose':
        """Create a Pose given two positions."""
        return cls(current, previous.direction_to(current))