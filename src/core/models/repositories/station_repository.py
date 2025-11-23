from core.models.geometry.edge import Edge
from core.models.geometry.node import Node
from core.models.geometry.position import Position

from core.models.station import Station
from core.models.railway.graph_adapter import GraphAdapter
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem

class StationRepository:
    """In-memory repository for Station objects with platform management."""
    
    def __init__(self, railway: "RailwaySystem"):
        self._stations: dict[str, Station] = {}
        self._next_id: int = 1
        self._railway = railway
    
    def add(self, node: Node, name: str) -> Station:
        station = Station(name, node, self._next_id)
        self._stations[station.id] = station
        self._next_id += 1
        return station
    
    def _remove(self, station_id: str) -> Station:
        return self._stations.pop(station_id)
    
    def move(self, station_id: str, new_node: Node) -> None:
        station = self._stations[station_id]
        station.node = new_node
    
    def get(self, station_id: str) -> Station:
        return self._stations[station_id]
    
    def get_by_node(self, node: Node) -> Station | None:
        for station in self._stations.values():
            if station.node == node:
                return station
        return None
    
    def get_by_name(self, name: str) -> Station | None:
        for station in self._stations.values():
            if station.name == name:
                return station
        return None
    
    def all(self) -> tuple[Station]:
        return tuple(self._stations.values())
    
    def is_within_any(self, node: Node) -> bool:
        return any(node.is_within_station_rect(station.node) for station in self._stations.values())
    
    def add_platform(self, station_id: str, edges: frozenset[Edge]) -> None:
        platform = [edge.sorted() for edge in sorted(edges)]
        self._railway.graph.set_edge_attr(platform[0], 'station', station_id)
        for edge in platform[1:]:
            self._railway.graph.set_edge_attr(edge, 'station', station_id)
            self._railway.graph.set_node_attr(edge.a, 'station', station_id)
        
        self._stations[station_id].platforms.add(edges)
    
    def _remove_platform(self, edges: frozenset[Edge]) -> None:
        for edge in edges:
            self._railway.graph.remove_edge_attr(edge, 'station')
            self._railway.graph.remove_node_attr(edge.a, 'station')
            self._railway.graph.remove_node_attr(edge.b, 'station')
            
    def is_platform_at(self, node: Node) -> bool:
        if not self._railway.graph.has_node(node):
            return False
        return self._railway.graph.has_node_attr(node, 'station')
    
    def _remove_platform_from_station(self, station_id: str, edges: frozenset[Edge]) -> None:
        self._stations[station_id].platforms.remove(edges)
    
    def get_platform_at(self, node: Node) -> bool:
        return self._railway.graph.get_node_attr(node, 'station')
    
    def is_edge_platform(self, edge: Edge) -> bool:
        if not self._railway.graph.has_edge(edge):
            return False
        return self._railway.graph.has_edge_attr(edge, 'station')
    
    def get_platform_from_edge(self, edge: Edge) -> frozenset[Edge]:
        station_id = self._railway.graph.get_edge_attr(edge, 'station')
        for platform in self._stations[station_id].platforms:
            if edge in platform:
                return platform
    
    def platforms_middle_points(self, station: Station) -> set[Position]:
        return {self.get_middle_of_platform(platform) for platform in station.platforms}
    
    def get_middle_of_platform(self, edges: frozenset[Edge]) -> Position | None:
        sorted_edges = sorted(edges)
        mid_edge = sorted_edges[len(sorted_edges) // 2]
        return mid_edge.midpoint()
    
    def remove_station_at(self, node: Node):
        station = self.get_by_node(node)
        self._remove(station.id)
        for platform in station.platforms:
            self._remove_platform(platform)
            
        self._railway.schedules.remove_station_from_all(station.id)

    def remove_platform_at(self, edge: Edge):
        platform_edges = self.get_platform_from_edge(edge)
        station_id = self._railway.graph.get_edge_attr(edge, 'station')
        self._remove_platform(platform_edges)
        self._remove_platform_from_station(station_id, platform_edges)
        
    def add_portal(self, edges: frozenset[Edge]) -> None:
        for edge in edges:
            self._railway.graph.set_edge_attr(edge, 'portal', True)
            
    def remove_portal(self, edges: frozenset[Edge]) -> None:
        for edge in edges:
            self._railway.graph.remove_edge_attr(edge, 'portal')

    def to_dict(self) -> dict:
        return {
            "next_id": self._next_id,
            "stations": {station.id: station.to_dict() for station in self._stations.values()},
        }
    
    @classmethod
    def from_dict(cls, graph: GraphAdapter, data: dict) -> 'StationRepository':
        instance = cls(graph)
        instance._next_id = data["next_id"]
        
        stations = data["stations"]
        for id, station_data in stations.items():
            id = int(id)
            station = Station(
                name=station_data["name"],
                node=Node.from_dict(station_data["node"]),
                id=id,
                platforms={frozenset(Edge.from_dict_simple(edge_data) for edge_data in platform_data)
                           for platform_data in station_data["platforms"]}
            )
            instance._stations[id] = station
            for platform in station.platforms:
                instance.add_platform(id, platform)
        return instance