from core.models.geometry.edge import Edge
from core.models.geometry.node import Node
from dataclasses import dataclass, field

@dataclass
class Station:
    name: str
    node: Node
    id: int
    platforms: set[frozenset[Edge]] = field(default_factory=set)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "node": self.node.to_dict(),
            "platforms": [
            [edge.to_dict() for edge in platform]
            for platform in self.platforms
            ]
        }