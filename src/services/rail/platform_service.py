
from models.map.rail_map import SegmentFinder
from models.position import Position
from networkx import Graph


class PlatformService:
    def __init__(self, graph: Graph, segment_finder: SegmentFinder):
        self._graph = graph
        self._segfinder = segment_finder

    def add_platform(self, nodes: tuple[Position], edges: tuple[Position, Position], station_pos: Position) -> None:
        for pos in nodes:
            self._graph.nodes[pos]['station'] = station_pos

        for a, b in edges:
            self._graph.edges[a, b]['station'] = station_pos

    def remove_platform_at(self, pos: Position | tuple[Position, Position]) -> None:
        seg = self._segfinder.find_segment(pos, end_on_signal=False, only_platforms=True)

        for n in seg.nodes:
            del self._graph.nodes[n]['station']

        for a, b in seg.edges:
            del self._graph.edges[a, b]['station']

    def get_platforms(self) -> dict[tuple[Position, Position], Position]:
        return {edge: data['station'] for edge, data in self._graph.edges.items() if 'station' in data}
    
    def is_node_platform(self, pos: Position) -> bool:
        return 'station' in self._graph.nodes[pos]
    
    def is_edge_platform(self, edge: tuple[Position, Position]) -> bool:
        return 'station' in self._graph.edges[edge]