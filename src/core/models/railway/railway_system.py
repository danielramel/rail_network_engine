from core.models.geometry import Position, Pose
from core.models.railway.graph_adapter import GraphAdapter
from core.models.railway.graph_service import GraphService
from core.models.railway.path_service import PathService
from core.models.railway.signalling_service import SignallingService
from core.models.repositories.station_repository import StationRepository
from core.models.repositories.schedule_repository import ScheduleRepository
from core.models.repositories.train_repository import TrainRepository
from core.models.repositories.signal_repository import SignalRepository

class RailwaySystem:
    def __init__(self):
        self._graph_adapter = GraphAdapter()
        self._graph_service = GraphService(self)
        self._signal_repository = SignalRepository(self._graph_adapter)
        self._station_repository = StationRepository(self._graph_adapter)
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
        return self._signal_repository
    
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
            'schedule_repository': self._schedule_repository.to_dict(),
        }
        
    def from_dict(self, data: dict) -> None:
        self._graph_adapter = self._graph_adapter.from_dict(data['graph'])
        self._station_repository = StationRepository.from_dict(self._graph_adapter, data["station_repository"])
        self._signal_repository = SignalRepository.from_dict(self._graph_adapter, data["signal_repository"])
        self._schedule_repository = ScheduleRepository.from_dict(self, data['schedule_repository'])