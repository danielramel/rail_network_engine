from config.settings import GRID_SIZE, PLATFORM_LENGTH
from models.geometry import Position, Edge
from models.station import Station
from models.graph_adapter import GraphAdapter

class PlatformRepository:
    def __init__(self, graph: GraphAdapter):
        self._graph = graph

    def add(self, station: Station, edges: frozenset[Edge]) -> None:
        for edge in edges:
            self._graph.set_edge_attr(edge, 'station', station)
            
        station.platforms.add(frozenset(edges))

    def remove(self, edges: frozenset[Edge]) -> None:
        for edge in edges:
            self._graph.remove_edge_attr(edge, 'station')
    
    def is_platform_at(self, pos: Position) -> bool:
        edges = self._graph.get_edges(pos)
        if len(edges) == 1: return False

        return all(self._graph.has_edge_attr(edge, 'station') for edge in edges)

    def is_edge_platform(self, edge: Edge) -> bool:
        return self._graph.has_edge_attr(edge, 'station')

    def get_platform_from_edge(self, edge: Edge) -> frozenset[Edge]:
        # fixes next to each other platforms being indistinguishable
        station = self._graph.get_edge_attr(edge, 'station')
        for platform in station.platforms:
            if edge in platform:
                return platform

    def platforms_middle_points(self, station: Station) -> set[Position]:
        return {self.get_middle_of_platform(platform) for platform in station.platforms}
        
    def get_middle_of_platform(self, edges: frozenset[Edge]) -> Position | None:
        sorted_edges = sorted(edges)
        mid_edge = sorted_edges[len(sorted_edges) // 2]
        return mid_edge.midpoint()