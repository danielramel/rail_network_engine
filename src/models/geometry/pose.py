from typing import NamedTuple

from models.geometry.direction import Direction
from .position import Position

class Pose(NamedTuple):
    """Pose represents a position and the direction we arrived from."""
    position: Position
    direction: tuple[int, int]  # (dx, dy) normalized direction
    
    @classmethod
    def from_positions(cls, previous: Position, current: Position) -> 'Pose':
        """Create a Pose given two positions."""
        return cls(current, previous.direction_to(current))
    
    def get_valid_turns(self) -> list[tuple[int, int]]:
        """Get valid turn directions from the current direction."""
        return self.get_valid_turns(self.direction)
    
    @staticmethod
    def get_valid_turns(direction: Direction) -> list[tuple[int, int]]:
        """Get valid turn directions from the current direction."""
        VALID_TURNS = {
        (-1, -1): [(-1, -1), (-1, 0), (0, -1)],
        (-1, 1): [(-1, 1), (-1, 0), (0, 1)],
        (1, -1): [(1, -1), (1, 0), (0, -1)],
        (1, 1): [(1, 1), (1, 0), (0, 1)],
        (-1, 0): [(-1, 0), (-1, -1), (-1, 1)],
        (1, 0): [(1, 0), (1, -1), (1, 1)],
        (0, -1): [(0, -1), (-1, -1), (1, -1)],
        (0, 1): [(0, 1), (-1, 1), (1, 1)],
        (0, 0): [
            (-1, -1), (-1, 0), (-1, 1),
            (1, -1), (1, 0), (1, 1),
            (0, -1), (0, 1)
            ]
        }
        return VALID_TURNS[tuple(direction)]