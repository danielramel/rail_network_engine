from models.geometry import Position
from models.geometry.edge import Edge

class Station:
    name: str
    position: Position
    def __init__(self, name: str, position: Position):
        self.name : str = name
        self.position : Position = position
        self.platforms: set[frozenset[Edge]] = set()