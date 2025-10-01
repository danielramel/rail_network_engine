from networkx import Graph
from models.geometry import Position, Pose
from services.rail.segment_finder import NetworkExplorer
from services.rail.signal_service import SignalService
from services.rail.platform_service import PlatformService
from .station_repository import StationRepository, Station


class RailMap:
    def __init__(self):
        self.graph = Graph()
        self.segment_finder = NetworkExplorer(self.graph)
        self.signal_service = SignalService(self.graph)
        self.platform_service = PlatformService(self.graph, self.segment_finder)
        self.stations = StationRepository()
        
    def has_node_at(self, pos: Position) -> bool:
        return pos in self.graph
        
    def get_all_edges(self) -> tuple[tuple[Position, Position]]:
        return tuple(self.graph.edges)

    def is_intersection(self, pos: Position) -> bool:
        return pos in self.graph and self.graph.degree(pos) > 2

    def get_intersections(self) -> list[Position]:
        return [n for n in self.graph.nodes if self.graph.degree(n) > 2]

    # --- signals ---
    def has_signal_at(self, pos: Position) -> bool:
        return self.signal_service.has_signal_at(pos)
    
    def add_signal_at(self, signal: Pose) -> None:
        self.signal_service.add_signal(signal)

    def toggle_signal_at(self, pos: Position) -> None:
        self.signal_service.toggle_signal(pos)

    def remove_signal_at(self, pos: Position) -> None:
        self.signal_service.remove_signal(pos)

    def get_signals(self) -> tuple[Pose, ...]:
        return self.signal_service.get_all_signals()

    # --- platforms ---
    def add_platform(self, nodes: tuple[Position], edges: tuple[tuple[Position, Position]], station_pos: Position):
        self.platform_service.add_platform(nodes, edges, station_pos)

    def remove_platform_at(self, pos: Position | tuple[Position, Position]):
        self.platform_service.remove_platform_at(pos)

    def get_platforms(self) -> dict[tuple[Position, Position], Position]:
        return self.platform_service.get_platforms()

    # --- stations ---
    def add_station_at(self, pos: Position, name: str):
        self.stations.add(pos, name)

    def remove_station_at(self, pos: Position):
        self.stations.remove(pos)

    def get_station(self, pos: Position) -> Station:
        return self.stations.get(pos)

    def get_all_stations(self) -> dict[Position, Station]:
        return self.stations.all()

    # --- segments ---
    def get_segments_at(self, edge: tuple[Position, Position], end_on_signal: bool = False, only_platforms: bool = False) -> tuple[set[Position], set[tuple[Position, Position]]]:
        return self.segment_finder.get_segment(edge, end_on_signal=end_on_signal, only_platforms=only_platforms)

    def remove_segment_at(self, edge: tuple[Position, Position]) -> None:
        nodes, edges = self.get_segments_at(edge)
        if len(nodes) == 0 and len(edges) == 1:
            # Special case: single edge between two intersections
            self.graph.remove_edge(*edges.pop())
            return
        
        for n in nodes:
            self.graph.remove_node(n)
            
    def add_segment(self, points: list[Position]) -> None:
        for p in points:
            self.graph.add_node(p)
        for a, b in zip(points[:-1], points[1:]):
            self.graph.add_edge(a, b)


    def has_platform_at(self, pos: Position) -> bool:
        return self.platform_service.is_platform_at(pos)

    def is_edge_platform(self, edge: tuple[Position, Position]) -> bool:
        return self.platform_service.is_edge_platform(edge)