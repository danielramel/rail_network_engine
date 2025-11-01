from typing import NamedTuple

from config.settings import GRID_SIZE
from models.geometry.direction import Direction
from .position import Position

class Pose(NamedTuple):
    position: Position
    direction: Direction
    
    @classmethod
    def from_positions(cls, previous: Position, current: Position) -> 'Pose':
        """Create a Pose given two positions."""
        return cls(current, previous.direction_to(current))
    
    def get_valid_neighbors(self) -> list[tuple['Pose', float]]:
        neighbors = []
        for dir in self.direction.get_valid_turns():
            nx = self.position.x + dir.x * GRID_SIZE
            ny = self.position.y + dir.y * GRID_SIZE
            new_state = Pose(Position(nx, ny), dir)

            neighbors.append((new_state, dir.get_cost()))
        return neighbors