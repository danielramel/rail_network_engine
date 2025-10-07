import networkx as nx
from models.geometry import Position, Pose
from models.station import Station
from services.rail.graph_query_service import GraphQueryService
from services.rail.signal_service import SignalService
from services.rail.path_finder import Pathfinder
from services.rail.platform_service import PlatformService
from infrastructure.station_repository import StationRepository



class RailMap:
    def __init__(self):
        self._graph = nx.Graph()
        self._query_service = GraphQueryService(self._graph)
        self._signal_service = SignalService(self._graph, self)
        self._platform_service = PlatformService(self._graph, self._query_service)
        self._pathfinder = Pathfinder(self)
        self._station_repository = StationRepository()
    
    @property
    def nodes(self):
        return self._graph.nodes
    
    @property
    def edges(self):
        return self._graph.edges
    
    def has_node_at(self, pos: Position) -> bool:
        return pos in self._graph.nodes
    
    def degree_at(self, pos: Position) -> int:
        return self._graph.degree[pos]
    
    def has_edge(self, edge: tuple[Position, Position]) -> bool:
        return self._graph.has_edge(*edge)
    
    # -- graph queries ---
    def is_junction(self, pos: Position) -> bool:
        return self._query_service.is_junction(pos)

    @property
    def junctions(self) -> list[Position]:
        return [n for n in self._graph.nodes if self.is_junction(n)]
    
    def get_segment(
        self, 
        edge: tuple[Position, Position], 
        end_on_signal: bool = False, 
        only_platforms: bool = False, 
        only_straight: bool = False,
        max_nr: int | None = None
    ):
        return self._query_service.get_segment(
            edge, 
            end_on_signal=end_on_signal, 
            only_platforms=only_platforms, 
            only_straight=only_straight, 
            max_nr=max_nr)

    def set_edge_attrs(self, edges: set[tuple[Position, Position]], attr: str) -> None:
        for edge in edges:
            self._graph.edges[edge][attr] = True
                    
    # -- graph modifications ---
    def remove_segment_at(self, edge: tuple[Position, Position]) -> None:
        nodes, edges = self.get_segment(edge)
        if len(nodes) == 0 and len(edges) == 1:
            # Special case: single edge between two intersections
            self._graph.remove_edge(*edges.pop())
            return
        
        for n in nodes:
            self._graph.remove_node(n)
            
    def add_segment(self, points: list[Position], speed: int) -> None:
        for p in points:
            self._graph.add_node(p)
        for a, b in zip(points[:-1], points[1:]):
            self._graph.add_edge(a, b, weight=1/speed, speed=speed)
            
            
    # --- pathfinding ---
    def is_blocked(self, pos: Position) -> bool:
        return self._pathfinder.is_blocked(pos)

    def find_path(self, start: Pose, end: Position) -> list[Position] | None:
        return self._pathfinder.find_grid_path(start, end)

    def find_network_path(self, start: Position, end: Position, only_straight: bool) -> list[Position] | None:
        return self._pathfinder.find_network_path(start, end, only_straight)

    # --- signals ---
    @property
    def signals(self) -> tuple[Pose, ...]:
        return self._signal_service.all()
    
    def has_signal_at(self, pos: Position) -> bool:
        return self._signal_service.has_signal_at(pos)
    
    def add_signal_at(self, signal: Pose) -> None:
        self._signal_service.add(signal)
        
    def get_signal_at(self, pos: Position) -> Pose:
        return self._signal_service.get(pos)

    def toggle_signal_at(self, pos: Position) -> None:
        self._signal_service.toggle(pos)

    def remove_signal_at(self, pos: Position) -> None:
        self._signal_service.remove(pos)
        
    def get_signal_at(self, pos: Position) -> Pose | None:
        return Pose(pos, self._graph.nodes[pos]['signal'])

    # --- stations ---
    @property
    def stations(self) -> tuple[Station, ...]:
        return self._station_repository.all().values()

    @property
    def station_positions(self) -> tuple[Position, ...]:
        return self._station_repository.all().keys()
    
    def add_station_at(self, pos: Position, name: str):
        self._station_repository.add(pos, name)

    def remove_station_at(self, pos: Position):
        self._station_repository.remove(pos)
        
    def move_station(self, old_pos: Position, new_pos: Position):
        self._station_repository.move(old_pos, new_pos)

    def get_station_at(self, pos: Position) -> Station:
        return self._station_repository.get(pos)
    
    def is_within_station_rect(self, pos: Position) -> bool:
        return self._station_repository.is_within_station_rect(pos)
    
    # --- platforms ---
    @property
    def platforms(self) -> dict[tuple[Position, Position], Station]:
        return self._platform_service.all()

    def add_platform_on(self, station: Station, edges: tuple[tuple[Position, Position]]):
        self._platform_service.add(station, edges)

    def remove_platform_at(self, edge: tuple[Position, Position]):
        self._platform_service.remove(edge)

    def is_platform_at(self, pos: Position) -> bool:
        return self._platform_service.is_platform_at(pos)

    def is_edge_platform(self, edge: tuple[Position, Position]) -> bool:
        return self._platform_service.is_edge_platform(edge)

    def calculate_platform_preview(self, edge: tuple[Position, Position]) -> Position | None:
        return self._platform_service.calculate_platform_preview(edge)

    def get_platform(self, edge: tuple[Position, Position]) -> set[tuple[Position, Position]] | None:
        return self._platform_service.get_platform(edge)

    def get_middle_of_platform(self, edges: tuple[tuple[Position, Position]]) -> Position | None:
        return self._platform_service.get_middle_of_platform(edges)

    def get_platform_middle_points(self) -> dict[tuple[Position, Position], Position]:
        return self._platform_service.platform_middle_points()