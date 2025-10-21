from models.geometry import Position
from models.geometry.edge import Edge
from dataclasses import dataclass, field, asdict

@dataclass
class Station:
    name: str
    position: Position
    platforms: set[frozenset[Edge]] = field(default_factory=set)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "position": self.position.to_dict(),
            "platforms": [
            [edge.to_dict() for edge in platform]
            for platform in self.platforms
            ]
        }
        
    def to_dict_simple(self) -> dict:
        return {
            "name": self.name,
            "position": self.position.to_dict(),
        }


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
    
    def get_by_name(self, name: str) -> Station | None:
        for station in self._by_pos.values():
            if station.name == name:
                return station
        raise KeyError(f"Station with name {name} not found.")

    def all(self) -> dict[Position, Station]:
        return self._by_pos
    
    def is_within_station_rect(self, pos: Position) -> bool:
        return any(pos.is_within_station_rect(station_pos) for station_pos in self._by_pos.keys())
    
    def remove_platform_from_station(self, station: Station, edges: frozenset[Edge]) -> None:
        self._by_pos[station.position].platforms.remove(edges)
        
    def to_dict(self) -> dict:
        return [station.to_dict() for station in self._by_pos.values()]

    @classmethod
    def from_dict(cls, stations: list[dict]) -> None:
        instance = cls()
        for station_data in stations:
            pos = Position.from_dict(station_data["position"])
            station = Station(
                name=station_data["name"],
                position=pos,
                platforms={frozenset(Edge.from_dict(edge_data) for edge_data in platform_data)
                           for platform_data in station_data["platforms"]}
            )
            instance._by_pos[pos] = station
        return instance