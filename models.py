
from dataclasses import dataclass
from typing import Tuple
from typing import NamedTuple



@dataclass(frozen=True, order=True)
class Point:
    x: float
    y: float
    
    def __iter__(self):
        yield self.x
        yield self.y
    

class PointWithDirection(NamedTuple):
    """PointWithDirection represents a position and the direction we arrived from."""
    point: Point
    direction: Tuple[int, int]  # (dx, dy) normalized direction