from collections import deque
from core.models.geometry.edge import Edge
from core.models.geometry.pose import Pose
from core.config.settings import Config
from core.models.rail import Rail
from core.models.signal import Signal
from core.models.timetable import TimeTable
from core.models.train_config import TrainConfig

from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem
    
DT = 1 / Config.FPS
INITIAL_DISTANCE_TO_PLATFORM_END = 1.0


class Train:
    id: int = None
    path : list[Rail] = None
    _railway: 'RailwaySystem'
    config: TrainConfig
    speed : float = 0.0
    timetable : TimeTable = None
    _is_live : bool = False
    _path_distance : float = 0.0
    _occupied_edge_count_cache : int | None = None
    _unsubscribe: Callable | None = None
    _braking_curve: list[float] = None 
     
    def __init__(self, edges: list[Edge], railway: 'RailwaySystem', config: TrainConfig) -> None:
        self._railway = railway
        self.config = config.copy()
        self.path = []
        self._braking_curve = []
        self.extend_path(edges[-(int((self.config.total_length + INITIAL_DISTANCE_TO_PLATFORM_END) // Config.SHORT_SEGMENT_LENGTH) + 1):])
        
        remaining = self.get_distance_until_next_edge()
        self._path_distance = remaining - INITIAL_DISTANCE_TO_PLATFORM_END
        
    def set_timetable(self, timetable: TimeTable) -> None:
        self.timetable = timetable
        
    def tick(self):
        if not self._is_live:
            return
        
        #TODO continue from braking curve calculation

        distance_until_next_edge = self.get_distance_until_next_edge()
        speed_due_to_braking = self.get_max_speed(distance_until_next_edge, self._braking_curve[-1])
        speed_with_acc = self.speed + (self.config.acceleration * DT)
        speed_due_to_tracks = min(rail.speed for rail in self.path[:self._occupied_edge_count])
        self.speed = min(speed_due_to_braking, speed_with_acc, speed_due_to_tracks)
            
        if self.speed == 0.0:
            return
            
            
        self._occupied_edge_count_cache = None
        travel_distance = self.speed * DT - self.config.deceleration * DT * DT / 2
        if distance_until_next_edge < travel_distance:
            self._braking_curve.pop()
        self._path_distance += travel_distance
        
        first_edge_length = self.path[0].length
        if self._path_distance >= first_edge_length:
            self._path_distance -= first_edge_length
            passed_rail = self.path.pop(0)
            self._railway.signalling.passed(passed_rail.edge)
            
    def calculate_braking_curve(self):
        self._braking_curve = []
        speed = 0.0
        for rail in reversed(self.path[self._occupied_edge_count - 1:]):
            self._braking_curve.append(speed)
            speed = min(rail.speed, self.get_max_speed(rail.length, speed))
            
            
        #             if self._railway.stations.is_edge_platform(rail.edge):
    #                 station_id = self._railway.stations.get_edge_platform(rail.edge)
    #                 if self.timetable and station_id == self.timetable.get_next_station().id:
    #                     platform = self._railway.stations.get_platform_from_edge(rail.edge)
    #                     braking_speed = min(braking_speed, _get_max_speed(distance + len(platform)*Config.SHORT_SEGMENT_LENGTH, 0.0))
    #                     braking_speed = min(braking_speed, min(self._railway.graph.get_edge_speed(edge) for edge in platform))
    #                     return braking_speed
            
    
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
        while signal.next_signal is not None:
            self.extend_path(signal.path)
            signal = signal.next_signal
        
        self._unsubscribe = signal.subscribe(self.signal_turned_green_ahead)
        
        self.calculate_braking_curve()
        
    def reverse(self) -> None:
        self._path_distance = self.get_distance_until_next_edge()
        self.path = [rail.reversed() for rail in reversed(self.path)]        
            
    def shutdown(self) -> None:
        self._is_live = False
        self.path = self.path[:self._occupied_edge_count]
        self._unsubscribe()
        
    def get_locomotive_pose(self) -> Pose:
        return Pose.from_edge(self.path[self._occupied_edge_count - 1].edge)
    
    
    def extend_path(self, extension: list[Edge]) -> None:
        self.path += [self._railway.graph.get_rail(edge) for edge in extension]
        
    def get_max_speed(self, distance: float, speed: float) -> float:
        if distance <= 1.0:
            return speed
            # FORMULA: V = sqrt(u^2 + 2as)
        return (speed**2 + (2 * distance * self.config.deceleration)) ** 0.5
                
        
    def get_distance_until_next_edge(self) -> float:
        remaining = self.config.total_length + self._path_distance
        i = 0
        while remaining - self.path[i].length > 0:
            remaining -= self.path[i].length
            i += 1
        return self.path[i].length - remaining
            
                    
    def signal_turned_green_ahead(self, path: list[Edge], signal: Signal) -> bool:
        self.extend_path(path)
        while signal.next_signal is not None:
            self.extend_path(signal.path)
            signal = signal.next_signal
        self._unsubscribe = signal.subscribe(self.signal_turned_green_ahead)
        self.calculate_braking_curve()