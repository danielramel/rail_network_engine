from models.geometry import Position
from models.geometry.edge import Edge
from dataclasses import dataclass, field

@dataclass
class Station:
    name: str
    position: Position
    platforms: set[frozenset[Edge]] = field(default_factory=set)