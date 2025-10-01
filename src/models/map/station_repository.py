from models.geometry import Position

class Station:
    name: str
    position: Position
    def __init__(self, name: str, position: Position):
        self.name = name
        self.position = position
        
        
class StationRepository:
    """In-memory repository for Station objects, ensuring uniqueness by position."""

    def __init__(self):
        self._by_pos: dict[Position, Station] = {}

    def add(self, pos: Position, name: str) -> Station:
        if pos in self._by_pos: raise ValueError("Station already exists at this position")
        
        self._by_pos[pos] = Station(name, pos)

    def remove(self, pos: Position) -> None:
        del self._by_pos[pos]

    def get(self, pos: Position) -> Station:
        return self._by_pos[pos]

    def all(self) -> dict[Position, Station]:
        return self._by_pos
    
