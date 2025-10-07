from models.geometry import Position

class Station:
    name: str
    position: Position
    def __init__(self, name: str, position: Position):
        self.name : str = name
        self.position : Position = position
        self.platforms: set[set[tuple[Position, Position]]] = set()  # set of sets of edges representing platforms