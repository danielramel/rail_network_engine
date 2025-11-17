from typing import NamedTuple

from core.config.settings import GRID_SIZE
from core.models.geometry import Edge, Direction, Position

class Pose(NamedTuple):
    position: Position
    direction: Direction
    
    @classmethod
    def from_positions(cls, previous: Position, current: Position) -> 'Pose':
        """Create a Pose given two positions."""
        return cls(current, previous.direction_to(current))
    
    @classmethod
    def from_edge(cls, edge: Edge) -> 'Pose':
        return cls.from_positions(edge.a, edge.b)
    
    def get_neighbors_in_direction(self) -> list[tuple['Pose', float]]:
        neighbors = []
        for dir in self.direction.get_valid_turns():
            nx = self.position.x + dir.x * GRID_SIZE
            ny = self.position.y + dir.y * GRID_SIZE
            new_state = Pose(Position(nx, ny), dir)

            neighbors.append((new_state, dir.get_cost()))
        return neighbors
    
    def to_dict(self) -> dict:
        return {
            "position": self.position.to_dict(),
            "direction": self.direction.to_dict()
        }
        
    @classmethod
    def from_dict(cls, data: dict) -> 'Pose':
        return cls(
            position=Position.from_dict(data["position"]),
            direction=Direction(**data["direction"])
        )