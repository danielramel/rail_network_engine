from typing import NamedTuple

from core.models.geometry.edge import Edge
from core.models.geometry.node import Node
from core.models.geometry.direction import Direction

class Pose(NamedTuple):
    node: Node
    direction: Direction
    
    @classmethod
    def from_nodes(cls, previous: Node, current: Node) -> 'Pose':
        """Create a Pose given two nodes."""
        return cls(current, previous.direction_to(current))
    
    @classmethod
    def from_edge(cls, edge: Edge) -> 'Pose':
        return cls.from_nodes(edge.a, edge.b)
    
    def get_valid_turns(self) -> list['Pose']:
        neighbors = []
        for dir in self.direction.get_valid_turns():
            nx = self.node.x + dir.x
            ny = self.node.y + dir.y
            new_state = Pose(Node(nx, ny), dir)

            neighbors.append(new_state)
        return neighbors
    
    def opposite(self) -> 'Pose':
        return Pose(self.node, self.direction.opposite())
    
    def get_next_in_direction(self) -> 'Pose':
        return Pose(
            Node(
                self.node.x + self.direction.x,
                self.node.y + self.direction.y
            ),
            self.direction
        )
    
    
    def to_dict(self) -> dict:
        return {
            "position": self.node.to_dict(),
            "direction": self.direction.to_dict()
        }
        
        
    @classmethod
    def from_dict(cls, data: dict) -> 'Pose':
        return cls(
            node=Node.from_dict(data["node"]),
            direction=Direction(**data["direction"])
        )