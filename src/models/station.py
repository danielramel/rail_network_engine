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

class StationRepository:
    """In-memory repository for Station objects, ensuring uniqueness by ID."""
    def __init__(self):
        self._stations: dict[int, Station] = {}
        self._next_id: int = 1

    def add(self, pos: Position, name: str) -> Station:
        station = Station(name, pos, id=self._next_id)
        self._stations[station.id] = station
        self._next_id += 1
        return station
    
    def remove(self, station_id: int) -> Station:
        return self._stations.pop(station_id)

    def move(self, station_id: int, new_pos: Position) -> None:
        station = self._stations[station_id]
        station.position = new_pos

    def get(self, station_id: int) -> Station:
        return self._stations[station_id]
    
    def get_by_position(self, pos: Position) -> Station | None:
        for station in self._stations.values():
            if station.position == pos:
                return station
        return None
    
    def get_by_name(self, name: str) -> Station | None:
        for station in self._stations.values():
            if station.name == name:
                return station
        return None

    def all(self) -> list[Station]:
        return list(self._stations.values())
    
    def positions(self) -> list[Position]:
        return [station.position for station in self._stations.values()]
    
    def is_within_any(self, pos: Position) -> bool:
        return any(pos.is_within_station_rect(station.position) for station in self._stations.values())
    
    def remove_platform_from_station(self, station: Station, edges: frozenset[Edge]) -> None:
        self._stations[station.id].platforms.remove(edges)
        
    def to_dict(self) -> dict:
        return {
            "next_id": self._next_id,
            "stations": [station.to_dict() for station in self._stations.values()]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'StationRepository':
        instance = cls()
        instance._next_id = data["next_id"]
        
        stations = data["stations"]
        for station_data in stations:
            pos = Position.from_dict(station_data["position"])
            station = Station(
                name=station_data["name"],
                position=pos,
                id=station_data["id"],
                platforms={frozenset(Edge.from_dict(edge_data) for edge_data in platform_data)
                           for platform_data in station_data["platforms"]}
            )
            instance._stations[station.id] = station

        return instance