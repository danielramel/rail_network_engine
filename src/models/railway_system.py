import networkx as nx
from models.geometry import Position, Pose, Edge
from models.graph_adapter import GraphAdapter
from services.railway_system.graph_service import GraphService
from services.railway_system.path_service import PathService
from models.platform_repository import PlatformRepository
from services.railway_system.signalling_service import SignallingService
from models.station import StationRepository
from models.schedule import ScheduleRepository
from models.train import TrainRepository
from models.signal import SignalRepository

class RailwaySystem:
    def __init__(self):
        self._graph = nx.Graph()
        self._graph_adapter = GraphAdapter(self._graph)
        self._graph_service = GraphService(self._graph_adapter)
        self._signal_service = SignalRepository(self._graph_adapter)
        self._platform_service = PlatformRepository(self._graph_adapter)
        self._station_repository = StationRepository()
        self._schedule_repository = ScheduleRepository()
        self._train_repository = TrainRepository()
        self._pathfinder = PathService(self)
        self._signalling_service = SignallingService(self)
    
    @property
    def graph(self) -> GraphAdapter:
        return self._graph_adapter
    
    @property
    def graph_service(self) -> GraphService:
        return self._graph_service
    
    @property
    def signals(self) -> SignalRepository:
        return self._signal_service
    
    @property
    def schedules(self) -> ScheduleRepository:
        return self._schedule_repository
            
    @property
    def stations(self) -> StationRepository:
        return self._station_repository

    @property
    def trains(self) -> TrainRepository:
        return self._train_repository
    
    def find_path(self, start: Pose, end: Position) -> list[Position] | None:
        return self._pathfinder.find_grid_path(start, end)
    
    @property
    def platforms(self) -> PlatformRepository:
        return self._platform_service
    
    @property
    def signalling(self) -> SignallingService:
        return self._signalling_service
    
    def tick(self):
        for train in self._train_repository.all():
            train.tick()

    def remove_station_at(self, pos: Position):
        station = self._station_repository.get_by_position(pos)
        self._station_repository.remove(station.id)
        for platforms in station.platforms:
            self._platform_service.remove(platforms)

    def remove_platform_at(self, edge: Edge):
        platform_edges = self.platforms.get_platform_from_edge(edge)
        station = self._graph.edges[edge]['station']
        self._platform_service.remove(platform_edges)
        self._station_repository.remove_platform_from_station(station, platform_edges)
    
    def to_dict(self) -> dict:
        return {
            'graph': self._graph_service.to_dict(),
            'stations': self._station_repository.to_dict(),
            'schedules': self._schedule_repository.to_dict(),
        }
        
    def from_dict(self, data: dict) -> None:
        self._station_repository = StationRepository.from_dict(data['stations'])
        self._schedule_repository = ScheduleRepository.from_dict(data['schedules'], self)
        self._graph_adapter.from_dict(data['graph'])