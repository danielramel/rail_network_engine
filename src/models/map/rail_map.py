import networkx as nx
from models.geometry import Position, Pose
from services.rail.network_explorer import NetworkExplorer
from services.rail.signal_service import SignalService
from services.rail.platform_service import PlatformService
from .station_repository import StationRepository, Station


class RailMap:
    def __init__(self):
        self._graph = nx.Graph()
        self.explorer = NetworkExplorer(self._graph)
        self.signal_service = SignalService(self._graph, self)
        self.platform_service = PlatformService(self._graph, self.explorer)
        self._stations = StationRepository()

    
    def is_junction(self, pos: Position) -> bool:
        return NetworkExplorer(self._graph).is_junction(pos)

    def get_junctions(self) -> list[Position]:
        return [n for n in self._graph.nodes if self.is_junction(n)]
    
    @property
    def edges(self):
        return self._graph.edges
    
    @property
    def nodes(self):
        return self._graph.nodes
    
    def has_node_at(self, pos: Position) -> bool:
        return pos in self._graph.nodes
    
    def degree_at(self, pos: Position) -> int:
        return self._graph.degree[pos]
    
     # --- segments ---
    def get_segment(self, edge: tuple[Position, Position], end_on_signal: bool = False, only_platforms: bool = False) -> tuple[set[Position], set[tuple[Position, Position]]]:
        return self.explorer.get_segment(edge, end_on_signal=end_on_signal, only_platforms=only_platforms)

    def remove_segment_at(self, edge: tuple[Position, Position]) -> None:
        nodes, edges = self.get_segment(edge)
        if len(nodes) == 0 and len(edges) == 1:
            # Special case: single edge between two intersections
            self._graph.remove_edge(*edges.pop())
            return
        
        for n in nodes:
            self._graph.remove_node(n)
            
    def add_segment(self, points: list[Position]) -> None:
        for p in points:
            self._graph.add_node(p)
        for a, b in zip(points[:-1], points[1:]):
            self._graph.add_edge(a, b)


    # --- signals ---
    def has_signal_at(self, pos: Position) -> bool:
        return self.signal_service.has_signal_at(pos)
    
    def add_signal_at(self, signal: Pose) -> None:
        self.signal_service.add(signal)
        
    def get_signal_at(self, pos: Position) -> Pose:
        return self.signal_service.get(pos)

    def toggle_signal_at(self, pos: Position) -> None:
        self.signal_service.toggle(pos)

    def remove_signal_at(self, pos: Position) -> None:
        self.signal_service.remove(pos)
        
    def get_signal_at(self, pos: Position) -> Pose | None:
        return Pose(pos, self._graph.nodes[pos]['signal'])

    @property
    def signals(self) -> tuple[Pose, ...]:
        return self.signal_service.all()

    # --- platforms ---
    def add_platform_on(self, edges: tuple[tuple[Position, Position]], station_pos: Position):
        self.platform_service.add(edges, station_pos)

    def remove_platform_at(self, edge: tuple[Position, Position]):
        self.platform_service.remove(edge)

    @property
    def platforms(self) -> dict[tuple[Position, Position], Position]:
        return self.platform_service.all()
    
    def is_platform_at(self, pos: Position) -> bool:
        return self.platform_service.is_platform_at(pos)

    def is_edge_platform(self, edge: tuple[Position, Position]) -> bool:
        return self.platform_service.is_edge_platform(edge)

    # --- stations ---
    def add_station_at(self, pos: Position, name: str):
        self._stations.add(pos, name)

    def remove_station_at(self, pos: Position):
        self._stations.remove(pos)

    def get_station_at(self, pos: Position) -> Station:
        return self._stations.get(pos)

    @property
    def stations(self) -> dict[Position, Station]:
        return self._stations.all()