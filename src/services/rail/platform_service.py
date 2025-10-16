from config.settings import PLATFORM_LENGTH
from domain.rail_map import GraphQueryService
from models.geometry import Position, Edge, edge
from networkx import Graph
from models.station import Station

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from domain.rail_map import RailMap

class PlatformService:
    def __init__(self, graph: Graph, map: 'RailMap'):
        self._graph = graph
        self._map = map

    def add(self, station: Station, edges: frozenset[Edge]) -> None:
        for edge in edges:
            self._graph.edges[edge]['station'] = station
            
        station.platforms.add(frozenset(edges))

    def remove(self, edges: frozenset[Edge]) -> None:
        for edge in edges:
            del self._graph.edges[edge]['station']
    
    def all(self) -> dict[frozenset[Position, Position], Position]:
        return {Edge(*edge): station for *edge, station in self._graph.edges.data('station') if station is not None}
    
    def is_platform_at(self, pos: Position) -> bool:
        edges = self._graph.edges(pos)
        if len(edges) == 1: return False
        
        return all('station' in self._graph.edges[edge] for edge in self._graph.edges(pos))
    
    def is_edge_platform(self, edge: Edge) -> bool:
        return 'station' in self._graph.edges[*edge]
    
    def calculate_platform_preview(self, edge: Edge) -> tuple[bool, frozenset[Edge]]:
        _, edges = self._map.get_segment(edge, only_straight=True, max_nr=PLATFORM_LENGTH)
        for edge in edges:
            # check for platform corner cutting
            pass

        return (len(edges) == PLATFORM_LENGTH), edges

    def get_platform_from_edge(self, edge: Edge) -> frozenset[Edge]:
        _, edges = self._map.get_segment(edge, only_platforms=True)
        return edges

    def platforms_middle_points(self, station: Station) -> set[Position]:
        return {self.get_middle_of_platform(platform) for platform in station.platforms}
        
    def get_middle_of_platform(self, edges: frozenset[Edge]) -> Position | None:
        sorted_edges = sorted(edges)
        mid_edge = sorted_edges[len(sorted_edges) // 2]
        return mid_edge.midpoint()