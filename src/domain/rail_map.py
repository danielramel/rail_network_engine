import networkx as nx
from models.geometry import Position, Pose, Edge
from models.station import Station
from models.train import TrainRepository
from services.rail.graph_query_service import GraphQueryService
from services.rail.signal_service import SignalService
from services.rail.path_finder import Pathfinder
from services.rail.platform_service import PlatformService
from models.station import StationRepository

class RailMap:
    def __init__(self):
        self._graph = nx.Graph()
        self._query_service = GraphQueryService(self._graph)
        self._signal_service = SignalService(self._graph, self)
        self._platform_service = PlatformService(self._graph, self)
        self._pathfinder = Pathfinder(self)
        self._station_repository = StationRepository()
        self._train_repository = TrainRepository()
    
    @property
    def nodes(self) -> set[Position]:
        return self._graph.nodes
    
    @property
    def edges(self) -> frozenset[Edge]:
        return frozenset((Edge(*edge) for edge in self._graph.edges))

    def edges_with_data(self, key=None) -> dict[Edge, dict]:
        if key:
            return {Edge(*edge): data for *edge, data in self._graph.edges.data(key)}
        
        return {Edge(*edge): data for *edge, data in self._graph.edges.data()}

    def has_node_at(self, pos: Position) -> bool:
        return pos in self._graph.nodes
    
    def degree_at(self, pos: Position) -> int:
        return self._graph.degree[pos]
    
    def has_edge(self, edge: Edge) -> bool:
        return self._graph.has_edge(*edge)
    
    # -- graph queries ---
    def is_junction(self, pos: Position) -> bool:
        return self._query_service.is_junction(pos)

    @property
    def junctions(self) -> list[Position]:
        return [n for n in self._graph.nodes if self.is_junction(n)]
    
    def get_segment(
        self, 
        edge: Edge, 
        end_on_signal: bool = False, 
        only_platforms: bool = False, 
        only_straight: bool = False,
        max_nr: int | None = None
    ) -> tuple[frozenset[Position], frozenset[Edge]]:
        return self._query_service.get_segment(
            edge, 
            end_on_signal=end_on_signal, 
            only_platforms=only_platforms, 
            only_straight=only_straight, 
            max_nr=max_nr)
                    
    # -- graph modifications ---
    def remove_segment_at(self, edge: Edge) -> None:
        nodes, edges = self.get_segment(edge)
        if len(nodes) == 0 and len(edges) == 1:
            # Special case: single edge between two intersections
            self._graph.remove_edge(*next(iter(edges)))
            return
        
        for n in nodes:
            self._graph.remove_node(n)
            
    def add_segment(self, points: list[Position], speed: int) -> None:
        for p in points:
            self._graph.add_node(p)
        for a, b in zip(points[:-1], points[1:]):
            self._graph.add_edge(a, b, speed=speed)
            
            
    # --- pathfinding ---
    def is_blocked(self, pos: Position) -> bool:
        return self._pathfinder.is_blocked(pos)

    def find_path(self, start: Pose, end: Position) -> list[Position] | None:
        return self._pathfinder.find_grid_path(start, end)

    # --- signals ---
    @property
    def signals(self) -> set[Pose]:
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

    # --- stations ---
    @property
    def stations(self) -> tuple[Station]:
        return tuple(self._station_repository.all().values())

    @property
    def station_positions(self) -> set[Position]:
        return set(self._station_repository.all().keys())
    
    def add_station_at(self, pos: Position, name: str):
        self._station_repository.add(pos, name)

    def remove_station_at(self, pos: Position):
        station = self._station_repository.remove(pos)
        for platforms in station.platforms:
            self._platform_service.remove(platforms)
        
    def move_station(self, old_pos: Position, new_pos: Position):
        self._station_repository.move(old_pos, new_pos)

    def get_station_at(self, pos: Position) -> Station:
        return self._station_repository.get(pos)
    
    def get_station_by_name(self, name: str) -> Station | None:
        return self._station_repository.get_by_name(name)
    
    def is_within_station_rect(self, pos: Position) -> bool:
        return self._station_repository.is_within_station_rect(pos)
    
    # --- platforms ---
    @property
    def platforms(self) -> dict[Edge, Station]:
        return self._platform_service.all()

    def add_platform_on(self, station: Station, edges: set[Edge]):
        self._platform_service.add(station, edges)

    def remove_platform_at(self, edge: Edge):
        platform_edges = self.get_platform_from_edge(edge)
        station = self._graph.edges[edge]['station']
        self._platform_service.remove(platform_edges)
        self._station_repository.remove_platform_from_station(station, platform_edges)

    def is_platform_at(self, pos: Position) -> bool:
        return self._platform_service.is_platform_at(pos)

    def is_edge_platform(self, edge: Edge) -> bool:
        return self._platform_service.is_edge_platform(edge)

    def calculate_platform_preview(self, edge: Edge) -> tuple[bool, frozenset[Edge]] | None:
        return self._platform_service.calculate_platform_preview(edge)

    def get_platform_from_edge(self, edge: Edge) -> set[Edge] | None:
        return self._platform_service.get_platform_from_edge(edge)

    def get_middle_of_platform(self, edges: set[Edge]) -> Position | None:
        return self._platform_service.get_middle_of_platform(edges)

    def get_platforms_middle_points(self, station: Station) -> set[Position]:
        return self._platform_service.platforms_middle_points(station)
    
    # -- serialization ---
    def to_dict(self) -> dict:
        graph_data = nx.node_link_data(self._graph)
        
        # convert Position objects in node attributes to dicts
        for node in graph_data['nodes']:
            node['id'] = node['id'].to_dict()
            
        for link in graph_data['links']:
            for key in ('source', 'target'):
                link[key] = link[key].to_dict()
            if 'station' in link:
                link['station'] = link['station'].to_dict_simple()
            
        station_data = self._station_repository.to_dict()

        return {
            'graph': graph_data,
            'stations': station_data
        }
        

    def from_dict(self, data: dict) -> None:
        graph_data = data['graph']
        self._station_repository = StationRepository.from_dict(data['stations'])

        # convert dicts in node attributes back to Position objects
        for node in graph_data['nodes']:
            node['id'] = Position.from_dict(node['id'])
            if 'signal' in node:
                node['signal'] = tuple(node['signal'])
            
        for link in graph_data['links']:
            for key in ('source', 'target'):
                link[key] = Position.from_dict(link[key])
            if 'station' in link:
                pos = Position.from_dict(link['station']['position'])
                link['station'] = self.get_station_at(pos)

        temp_graph = nx.node_link_graph(graph_data)
        
        self._graph.clear()
        self._graph.add_nodes_from(temp_graph.nodes(data=True))
        self._graph.add_edges_from(temp_graph.edges(data=True))
        
        
    # --train repository ---
    @property
    def train_repository(self) -> TrainRepository:
        return self._train_repository