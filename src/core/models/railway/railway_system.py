from core.models.time import Time
from core.models.railway.graph_adapter import GraphAdapter
from core.models.railway.graph_service import GraphService
from core.models.railway.path_finder import PathFinder
from core.models.railway.signalling_service import SignallingService
from core.models.repositories.station_repository import StationRepository
from core.models.repositories.route_repository import RouteRepository
from core.models.repositories.train_repository import TrainRepository
from core.models.repositories.signal_repository import SignalRepository

class RailwaySystem:
    def __init__(self):
        self.time = Time()
        self._graph_adapter = GraphAdapter()
        self._graph_service = GraphService(self)
        self._signal_repository = SignalRepository(self._graph_adapter)
        self._station_repository = StationRepository(self)
        self._route_repository = RouteRepository()
        self._train_repository = TrainRepository(self)
        self._pathfinder = PathFinder(self)
        self._signalling_service = SignallingService(self)
    
    @property
    def graph(self) -> GraphAdapter:
        return self._graph_adapter
    
    @property
    def graph_service(self) -> GraphService:
        return self._graph_service
    
    @property
    def signals(self) -> SignalRepository:
        return self._signal_repository
    
    @property
    def routes(self) -> RouteRepository:
        return self._route_repository
            
    @property
    def stations(self) -> StationRepository:
        return self._station_repository

    @property
    def trains(self) -> TrainRepository:
        return self._train_repository
    
    @property
    def pathfinder(self) -> PathFinder:
        return self._pathfinder
    
    @property
    def signalling(self) -> SignallingService:
        return self._signalling_service
    
    def tick(self):
        for train in self._train_repository.all():
            train.tick()

    def to_dict(self) -> dict:
        return {
            'graph': self._graph_adapter.to_dict(),
            'station_repository': self._station_repository.to_dict(),
            'signal_repository': self._signal_repository.to_dict(),
            'route_repository': self._route_repository.to_dict(),
            'train_repository': self._train_repository.to_dict()
        }
        
    def replace_from_dict(self, data: dict) -> None:
        self._graph_adapter = GraphAdapter.from_dict(data['graph'])
        self._station_repository = StationRepository.from_dict(self, data["station_repository"])
        self._signal_repository = SignalRepository.from_dict(self._graph_adapter, data["signal_repository"])
        self._route_repository = RouteRepository.from_dict(self, data['route_repository'])
        self._train_repository = TrainRepository.from_dict(data['train_repository'], self)