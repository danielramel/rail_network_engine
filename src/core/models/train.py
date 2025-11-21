from core.models.geometry import Edge
from core.config.settings import Config
from core.models.geometry.pose import Pose
from core.models.rail import Rail
from core.models.signal import Signal
from core.models.timetable import TimeTable
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem
    
class TrainConfig:
    car_count: int = 3
    car_length: float = 24.5
    car_gap: int = 1
    acceleration: float = 1.2
    deceleration: float = 1.4
    max_speed: int = 160
    
    @property
    def total_length(self) -> float:
        return (self.car_count * self.car_length) + ((self.car_count - 1) * self.car_gap)
    
    def copy(self):
        c = TrainConfig()
        c.car_count = self.car_count
        c.car_length = self.car_length
        c.car_gap = self.car_gap
        c.acceleration = self.acceleration
        c.deceleration = self.deceleration
        c.max_speed = self.max_speed
        return c

class Train:
    id : int
    path : list[Rail] = []
    _railway: 'RailwaySystem'
    config: TrainConfig
    speed : float = 0.0  # in m/s
    timetable : TimeTable = None
    _is_live : bool = False
    _is_shutting_down : bool = False
    _target_speed: int = 0
    _target_distance: float = 0.0
    _path_distance : float = 0.0
    _occupied_edge_count_cache : int | None = None
     
    def __init__(self, id: int, edges: list[Edge], railway: 'RailwaySystem', config: TrainConfig) -> None:
        self.id = id
        self._railway = railway
        self.config = config.copy()
        self.path = [self._railway.graph.get_rail(edge) for edge in edges[-(int(self.config.total_length // Config.SHORT_SEGMENT_LENGTH) + 1):]]
        
    def set_timetable(self, timetable: TimeTable) -> None:
        self.timetable = timetable
        
    def tick(self):
        if not self._is_live:
            return
        
        if self._is_shutting_down:
            self.speed = max(0.0, self.speed - self.config.deceleration/Config.FPS)
            if self.speed == 0.0:
                self._shutdown()
                return
        else:
            max_safe_speed = self.get_max_safe_speed()
            speed_with_acc = self.speed + (self.config.acceleration/Config.FPS)
            self.speed = min(max_safe_speed, speed_with_acc, self.config.max_speed/3.6)
                
            if self.speed == 0.0:
                return

        self._occupied_edge_count_cache = None
        self._path_distance += round(self.speed / Config.FPS, 6)
        self._target_distance = max(self._target_distance - self.speed/Config.FPS, 0.0)
        
        first_edge_length = self.path[0].length
        if self._path_distance >= first_edge_length:
            self._path_distance -= first_edge_length
            passed_rail = self.path.pop(0)
            self._railway.signalling.passed(passed_rail.edge)
    
    @property
    def occupied_edge_count(self) -> int:
        if self._occupied_edge_count_cache is not None:
            return self._occupied_edge_count_cache
        
        distance = 0.0
        count = 0
        while distance <= self.config.total_length + self._path_distance:
            distance += self.path[count].length
            count += 1
        
        self._occupied_edge_count_cache = count
        return count
        
    def get_occupied_rails(self) -> tuple[Rail, ...]:
        return self.path[:self.occupied_edge_count]
    
    def occupies_edge(self, edge: Edge) -> bool:
        return edge in tuple(rail.edge for rail in self.path[:self.occupied_edge_count])
    
    @property
    def is_live(self) -> bool:
        return self._is_live
    
    def start(self) -> None:
        self._is_live = True
        path, signal = self._railway.signalling.get_initial_path(self.get_locomotive_pose())
        self.extend_path(path)
        signal.subscribe(self.signal_turned_green_ahead)
        
    def initiate_shutdown(self) -> None:
        if self.speed == 0.0:
            self._shutdown()
            return
        self._is_shutting_down = True
        
    def _shutdown(self) -> None:
        self._is_live = False
        self._is_shutting_down = False
        self.path = self.path[:self.occupied_edge_count]
        self._railway.signalling.unlock_path(self.path[self.occupied_edge_count:])
        
    def get_locomotive_pose(self) -> Pose:
        return Pose.from_edge(self.path[self.occupied_edge_count - 1].edge)
    
    def get_max_safe_speed(self) -> float:
        # FORMULA: V = sqrt(u^2 + 2as)
        return (self._target_speed**2 + (2 * self._target_distance * self.config.deceleration)) ** 0.5
    
    def extend_path(self, extension: list[Edge]):
        extension = [self._railway.graph.get_rail(edge) for edge in extension]
        self.path += extension
        self._target_distance += sum(rail.length for rail in extension)
    
    def signal_turned_green_ahead(self, path: list[Edge], signal: Signal) -> bool:
        self.extend_path(path)
        signal.subscribe(self.signal_turned_green_ahead)
        
        
    def reverse(self) -> None:
        raise NotImplementedError("Reversing trains is not implemented yet.")
        if self.edge_progress < 0.5:
            for edge in self.path[self._occupied_edge_count:]:
                self._railway.signalling.passed([edge])
            
            self.edge_progress = 0.5 - self.edge_progress
            self.path = [edge.reversed() for edge in self.path[self._occupied_edge_count-1::-1]]
        else:
            raise NotImplementedError("Reversing a train that is past the halfway point of an edge is not implemented.")