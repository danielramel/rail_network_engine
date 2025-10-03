from models.geometry import Position
from models.station import Station
        
        
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
    
    def is_within_station_rect(self, pos: Position) -> bool:
        return any(pos.is_within_station_rect(station_pos) for station_pos in self._by_pos.keys())
