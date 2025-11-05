from models.geometry import Position, Edge
from models.station import Station
from core.models.railway.graph_adapter import GraphAdapter

class StationRepository:
    """In-memory repository for Station objects with platform management."""
    
    def __init__(self, graph: GraphAdapter):
        self._stations: dict[str, Station] = {}
        self._next_id: int = 1
        self._graph = graph
    
    def add(self, pos: Position, name: str) -> Station:
        station = Station(name, pos, id=self._next_id)
        self._stations[station.id] = station
        self._next_id += 1
        return station
    
    def remove(self, station_id: str) -> Station:
        return self._stations.pop(station_id)
    
    def move(self, station_id: str, new_pos: Position) -> None:
        station = self._stations[station_id]
        station.position = new_pos
    
    def get(self, station_id: str) -> Station:
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
    
    def all(self) -> tuple[Station]:
        return tuple(self._stations.values())
    
    def is_within_any(self, pos: Position) -> bool:
        return any(pos.is_within_station_rect(station.position) for station in self._stations.values())
    
    def add_platform(self, station_id: str, edges: frozenset[Edge]) -> None:
        for edge in edges:
            self._graph.set_edge_attr(edge, 'station', station_id)
            self._graph.set_node_attr(edge.a, 'station', station_id)
            self._graph.set_node_attr(edge.b, 'station', station_id)
        self._stations[station_id].platforms.add(frozenset(edges))
    
    def remove_platform(self, edges: frozenset[Edge]) -> None:
        for edge in edges:
            self._graph.remove_edge_attr(edge, 'station')
    
    def remove_platform_from_station(self, station_id: str, edges: frozenset[Edge]) -> None:
        self._stations[station_id].platforms.remove(edges)
    
    def is_platform_at(self, pos: Position) -> bool:
        return self._graph.has_node_attr(pos, 'station')
    
    def is_edge_platform(self, edge: Edge) -> bool:
        return self._graph.has_edge_attr(edge, 'station')
    
    def get_platform_from_edge(self, edge: Edge) -> frozenset[Edge]:
        station_id = self._graph.get_edge_attr(edge, 'station')
        for platform in self._stations[station_id].platforms:
            if edge in platform:
                return platform
    
    def platforms_middle_points(self, station: Station) -> set[Position]:
        return {self.get_middle_of_platform(platform) for platform in station.platforms}
    
    def get_middle_of_platform(self, edges: frozenset[Edge]) -> Position | None:
        sorted_edges = sorted(edges)
        mid_edge = sorted_edges[len(sorted_edges) // 2]
        return mid_edge.midpoint()
    
    def remove_station_at(self, pos: Position):
        station = self.get_by_position(pos)
        self.remove(station.id)
        for platform in station.platforms:
            self.remove_platform(platform)

    def remove_platform_at(self, edge: Edge):
        platform_edges = self.get_platform_from_edge(edge)
        station_id = self._graph.get_edge_attr(edge, 'station')
        self.remove_platform(platform_edges)
        self.remove_platform_from_station(station_id, platform_edges)

    def to_dict(self) -> dict:
        return {
            "next_id": self._next_id,
            "stations": {station.id: station.to_dict() for station in self._stations.values()}
        }
    
    @classmethod
    def from_dict(cls, graph: GraphAdapter, data: dict) -> 'StationRepository':
        instance = cls(graph)
        instance._next_id = data["next_id"]
        
        stations = data["stations"]
        for id, station_data in stations.items():
            station = Station(
                name=station_data["name"],
                position=Position.from_dict(station_data["position"]),
                id=id,
                platforms={frozenset(Edge.from_dict(edge_data) for edge_data in platform_data)
                           for platform_data in station_data["platforms"]}
            )
            instance._stations[id] = station
            for platform in station.platforms:
                instance.add_platform(id, platform)
        return instance