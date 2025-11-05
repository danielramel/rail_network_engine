from models.geometry import Position
from models.geometry.edge import Edge
from dataclasses import dataclass, field

@dataclass
class Station:
    name: str
    position: Position
    id: int
    platforms: set[frozenset[Edge]] = field(default_factory=set)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "position": self.position.to_dict(),
            "platforms": [
            [edge.to_dict() for edge in platform]
            for platform in self.platforms
            ]
        }