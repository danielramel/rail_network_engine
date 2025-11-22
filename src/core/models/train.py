from core.models.geometry.edge import Edge
from core.models.geometry.pose import Pose
from core.config.settings import Config
from core.models.rail import Rail
from core.models.signal import Signal
from core.models.timetable import TimeTable
from core.models.train_config import TrainConfig

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem
    
DT = 1 / Config.FPS
INITIAL_DISTANCE_TO_PLATFORM_END = 1.0


class Train:
    id: int = None
    path : list[Rail] = []
    _railway: 'RailwaySystem'
    config: TrainConfig
    speed : float = 0.0
    timetable : TimeTable = None
    _is_live : bool = False
    _path_distance : float = 0.0
    _occupied_edge_count_cache : int | None = None
     
    def __init__(self, edges: list[Edge], railway: 'RailwaySystem', config: TrainConfig) -> None:
        self._railway = railway
        self.config = config.copy()
        self.path = [self._railway.graph.get_rail(edge) for edge in edges[-(int((self.config.total_length + INITIAL_DISTANCE_TO_PLATFORM_END) // Config.SHORT_SEGMENT_LENGTH) + 1):]]
        
        remaining = self.get_distance_to_path_end()
        self._path_distance = remaining - INITIAL_DISTANCE_TO_PLATFORM_END
        
    def set_timetable(self, timetable: TimeTable) -> None:
        self.timetable = timetable
        
    def tick(self):
        if not self._is_live:
            return

        max_safe_speed = self.get_max_safe_speed()
        speed_with_acc = self.speed + (self.config.acceleration * DT)
        self.speed = min(max_safe_speed, speed_with_acc)
            
        if self.speed == 0.0:
            return
            
            
        self._occupied_edge_count_cache = None
        travel_distance = self.speed * DT - self.config.deceleration * DT * DT / 2
        self._path_distance += travel_distance
        # self._target_distance = max(self._target_distance - travel_distance, 0.0)
        
        first_edge_length = self.path[0].length
        if self._path_distance >= first_edge_length:
            self._path_distance -= first_edge_length
            passed_rail = self.path.pop(0)
            self._railway.signalling.passed(passed_rail.edge)
    
    @property
    def _occupied_edge_count(self) -> int:
        if self._occupied_edge_count_cache is not None:
            return self._occupied_edge_count_cache
        
        remaining = self.config.total_length + self._path_distance
        count = 0
        while remaining > 0:
            remaining -= self.path[count].length
            count += 1
        
        self._occupied_edge_count_cache = count
        return count
        
    def get_occupied_rails(self) -> tuple[Rail, ...]:
        return self.path[:self._occupied_edge_count]
    
    def occupies_edge(self, edge: Edge) -> bool:
        return edge in tuple(rail.edge for rail in self.path[:self._occupied_edge_count])
    
    @property
    def is_live(self) -> bool:
        return self._is_live
    
    def start(self) -> None:
        self._is_live = True
        path, signal = self._railway.signalling.get_initial_path(self.get_locomotive_pose())
        self.extend_path(path)
        signal.subscribe(self.signal_turned_green_ahead)
        
    def reverse(self) -> None:
        self._target_distance = self._path_distance
        self._path_distance = self.get_distance_to_path_end()
        self.path = [rail.reversed() for rail in reversed(self.path)]
        
        
    def shutdown(self) -> None:
        self._is_live = False
        
    def get_locomotive_pose(self) -> Pose:
        return Pose.from_edge(self.path[self._occupied_edge_count - 1].edge)
    
    def get_max_safe_speed(self) -> float:
        def get_max_speed(distance: float, speed: float) -> float:
            if distance <= 1.0:
                return speed
            # FORMULA: V = sqrt(u^2 + 2as)
            return (speed**2 + (2 * distance * self.config.deceleration)) ** 0.5
        
        distance = self.get_distance_to_path_end()
        min_speed = min(self.config.max_speed, self.path[self._occupied_edge_count - 1].speed)
        for rail in self.path[self._occupied_edge_count:]:
            min_speed = min(min_speed, get_max_speed(distance, rail.speed))
            distance += rail.length
            
        min_speed = min(min_speed, get_max_speed(distance, 0.0))
            
        return min_speed
    
    def get_distance_to_path_end(self) -> float:
        remaining = self.config.total_length + self._path_distance
        i = 0
        while remaining - self.path[i].length > 0:
            remaining -= self.path[i].length
            i += 1
        return self.path[i].length - remaining
            
    def extend_path(self, extension: list[Edge]):
        path = [self._railway.graph.get_rail(edge) for edge in extension]
        self.path += path
                    
    def signal_turned_green_ahead(self, path: list[Edge], signal: Signal) -> bool:
        self.extend_path(path)
        signal.subscribe(self.signal_turned_green_ahead)