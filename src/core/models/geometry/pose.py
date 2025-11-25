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
    
    def get_connecting_poses(self, other_level: bool = False) -> list['Pose']:
        neighbors = []
        for dir in self.direction.get_valid_turns():
            nx = self.node.x + dir.x
            ny = self.node.y + dir.y
            new_state = Pose(Node(nx, ny, self.node.level), dir)

            neighbors.append(new_state)
            if other_level:
                neighbors.append(new_state.toggle_level())
        return neighbors
    
    def tunnel_level(self) -> 'Pose':
        return Pose(self.node.tunnel_level(), self.direction)
    
    def toggle_level(self) -> 'Pose':
        return Pose(self.node.toggle_level(), self.direction)
    
    def opposite(self) -> 'Pose':
        return Pose(self.node, self.direction.opposite())
    
    def get_next_in_direction(self) -> 'Pose':
        return Pose(
            Node(
                self.node.x + self.direction.x,
                self.node.y + self.direction.y,
                self.node.level
            ),
            self.direction
        )
        
    def get_previous_in_direction(self) -> 'Pose':
        return Pose(
            Node(
                self.node.x - self.direction.x,
                self.node.y - self.direction.y,
                self.node.level
                ),
            self.direction
        )
    
    
    def to_dict(self) -> dict:
        return {
            "node": self.node.to_dict(),
            "direction": self.direction.to_dict()
        }
        
        
    @classmethod
    def from_dict(cls, data: dict) -> 'Pose':
        return cls(
            node=Node.from_dict(data["node"]),
            direction=Direction(**data["direction"])
        )