from models.geometry import Position

class Station:
    name: str
    position: Position
    def __init__(self, name: str, position: Position):
        self.name = name
        self.position = position