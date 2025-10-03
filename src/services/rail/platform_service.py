from models.map.rail_map import GraphQueryService
from models.geometry import Position
from networkx import Graph


class PlatformService:
    def __init__(self, graph: Graph, segment_finder: GraphQueryService):
        self._graph = graph
        self._segfinder = segment_finder

    def add(self, edges: tuple[Position, Position], station_pos: Position) -> None:
        for a, b in edges:
            self._graph.edges[a, b]['station'] = station_pos

    def remove(self, edge: tuple[Position, Position]) -> None:
        _, edges = self._segfinder.get_segment(edge, end_on_signal=False, only_platforms=True)

        for edge in edges:
            del self._graph.edges[edge]['station']

    def all(self) -> dict[tuple[Position, Position], Position]:
        return {edge: data['station'] for edge, data in self._graph.edges.items() if 'station' in data}
    
    def is_platform_at(self, pos: Position) -> bool:
        return all('station' in self._graph.edges[edge] for edge in self._graph.edges(pos))
    
    def is_edge_platform(self, edge: tuple[Position, Position]) -> bool:
        return 'station' in self._graph.edges[edge]