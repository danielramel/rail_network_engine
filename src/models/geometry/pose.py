from typing import NamedTuple

from models.geometry.direction import Direction
from .position import Position

class Pose(NamedTuple):
    position: Position
    direction: Direction
    
    @classmethod
    def from_positions(cls, previous: Position, current: Position) -> 'Pose':
        """Create a Pose given two positions."""
        return cls(current, previous.direction_to(current))
    
    def get_valid_turns(self) -> list[Direction]:
        """Get valid turn directions from the current direction."""
        return self.get_valid_turns(self.direction)
    
    @staticmethod
    def get_valid_turns(direction: Direction) -> list[Direction]:
        """Get valid turn directions from the current direction."""
        VALID_TURNS = {
        Direction(-1, -1): [Direction(-1, -1), Direction(-1, 0), Direction(0, -1)],
        Direction(-1, 1): [Direction(-1, 1), Direction(-1, 0), Direction(0, 1)],
        Direction(1, -1): [Direction(1, -1), Direction(1, 0), Direction(0, -1)],
        Direction(1, 1): [Direction(1, 1), Direction(1, 0), Direction(0, 1)],
        Direction(-1, 0): [Direction(-1, 0), Direction(-1, -1), Direction(-1, 1)],
        Direction(1, 0): [Direction(1, 0), Direction(1, -1), Direction(1, 1)],
        Direction(0, -1): [Direction(0, -1), Direction(-1, -1), Direction(1, -1)],
        Direction(0, 1): [Direction(0, 1), Direction(-1, 1), Direction(1, 1)],
        Direction(0, 0): [
            Direction(-1, -1), Direction(-1, 0), Direction(-1, 1),
            Direction(1, -1), Direction(1, 0), Direction(1, 1),
            Direction(0, -1), Direction(0, 1)
            ]
        }
        return VALID_TURNS[direction]