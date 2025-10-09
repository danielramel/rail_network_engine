from models.geometry.edge import Edge
from models.station import Station
from models.geometry import Position

class StationRepository:
    """In-memory repository for Station objects, ensuring uniqueness by position."""
    def __init__(self):
        self._by_pos: dict[Position, Station] = {}

    def add(self, pos: Position, name: str) -> Station:        
        station = Station(name, pos)
        self._by_pos[pos] = station
        return station

    def remove(self, pos: Position) -> None:
        return self._by_pos.pop(pos)
        
    def move(self, old_pos: Position, new_pos: Position) -> None:
        station = self._by_pos.pop(old_pos)
        station.position = new_pos
        self._by_pos[new_pos] = station

    def get(self, pos: Position) -> Station:
        return self._by_pos[pos]

    def all(self) -> dict[Position, Station]:
        return self._by_pos
    
    def is_within_station_rect(self, pos: Position) -> bool:
        return any(pos.is_within_station_rect(station_pos) for station_pos in self._by_pos.keys())
    
    def remove_platform_from_station(self, station: Station, edge: Edge) -> frozenset[Edge]:
        self._by_pos[station.position].platforms.remove(edge)