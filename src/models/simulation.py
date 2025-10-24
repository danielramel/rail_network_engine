import networkx as nx
from models.geometry import Position, Pose, Edge
from models.schedule import Schedule
from services.rail.graph_query_service import GraphService
from services.rail.signal_service import SignalService
from services.rail.path_service import PathService
from services.rail.platform_service import PlatformService
from models.station import StationRepository
from models.schedule import ScheduleRepository

class Simulation:
    def __init__(self):
        self._graph = nx.Graph()
        self._graph_service = GraphService(self._graph)
        self._signal_service = SignalService(self._graph)
        self._platform_service = PlatformService(self._graph, self._graph_service)
        self._pathfinder = PathService(self)
        self._station_repository = StationRepository()
        self._schedule_repository = ScheduleRepository()
    
    @property
    def graph(self) -> GraphService:
        return self._graph_service
    
    @property
    def signals(self) -> SignalService:
        return self._signal_service
    
    @property
    def schedules(self) -> ScheduleRepository:
        return self._schedule_repository
            
    def find_path(self, start: Pose, end: Position) -> list[Position] | None:
        return self._pathfinder.find_grid_path(start, end)

    # --- stations ---
    @property
    def stations(self) -> StationRepository:
        return self._station_repository

    def remove_station_at(self, pos: Position):
        station = self._station_repository.get_by_position(pos)
        self._station_repository.remove(station.id)
        for platforms in station.platforms:
            self._platform_service.remove(platforms)
    
    # --- platforms ---
    @property
    def platforms(self) -> PlatformService:
        return self._platform_service

    def remove_platform_at(self, edge: Edge):
        platform_edges = self.platforms.get_platform_from_edge(edge)
        station = self._graph.edges[edge]['station']
        self._platform_service.remove(platform_edges)
        self._station_repository.remove_platform_from_station(station, platform_edges)
    
    # -- serialization ---
    def to_dict(self) -> dict:
        return {
            'graph': self._graph_service.to_dict(),
            'stations': self._station_repository.to_dict(),
            'schedules': self._schedule_repository.to_dict(),
        }
        

    def from_dict(self, data: dict) -> None:
        self._station_repository = StationRepository.from_dict(data['stations'])
        self._schedule_repository = ScheduleRepository.from_dict(data['schedules'], self)
        self._graph_service.from_dict(data['graph'])