from core.models.geometry.edge import Edge
from core.models.geometry.pose import Pose
from core.config.settings import Config
from core.models.rail import Rail
from core.models.signal import Signal
from core.models.schedule import Schedule
from core.models.train_config import TrainConfig

from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem
    
DT = 1 / Config.FPS

class Train:
    id: int = None
    path : list[Rail] = None
    _railway: 'RailwaySystem'
    config: TrainConfig
    speed : float = 0.0
    schedule : Schedule = None
    live : bool = False
    _path_distance : float = 0.0
    _occupied_edge_count_cache : int | None = None
    _unsubscribe: Callable | None = None
    _speed_profile: list[float] = None
    _routed_to_station_ahead: bool = False
    _dwell_time_counter: float = 0.0
     
    def __init__(self, edges: list[Edge], railway: 'RailwaySystem', config: TrainConfig) -> None:
        self._railway = railway
        self.config = config.copy()
        self._speed_profile = []
        self.path = [self._railway.graph.get_rail(edge) for edge in edges]
        self._path_distance = self.get_distance_until_next_edge() - Config.TRAIN_SAFETY_BUFFER
        
        if self._path_distance < 0.0:
            self._path_distance += self.path[0].length
        
    def tick(self):
        if not self.live:
            return
        
        distance_until_next_edge = self.get_distance_until_next_edge()
        speed_due_to_braking = self.get_max_speed(distance_until_next_edge, self._speed_profile[-1])
        speed_with_acc = self.speed + (self.config.acceleration * DT)
        speed_due_to_tracks = min(rail.speed for rail in self.path[:self._occupied_edge_count])
        self.speed = min(speed_due_to_braking, speed_with_acc, speed_due_to_tracks)
            
        if self.speed == 0.0:
            if self._routed_to_station_ahead:
                #train is stopped at station
                self._dwell_time_counter += DT
                dep_time = self.schedule.get_departure_time()
                if dep_time is not None and dep_time <= self._railway.time.in_minutes() and self._dwell_time_counter >= Config.MIN_TRAIN_STOP_TIME:
                    self._routed_to_station_ahead = False
                    self.schedule.depart_station()
                    self.compute_speed_profile()
                    self._dwell_time_counter = 0.0
            return
            
        travel_distance = (self.speed * DT - self.config.deceleration * DT * DT / 2)/3.6
        if distance_until_next_edge < travel_distance:
            self._speed_profile.pop()
            self._railway.signalling.reached(self.path[self._occupied_edge_count].edge.a)
            
        self._occupied_edge_count_cache = None
        self._path_distance += travel_distance
        
        first_edge_length = self.path[0].length
        if self._path_distance >= first_edge_length:
            self._path_distance -= first_edge_length
            passed_rail = self.path.pop(0)
            self._railway.signalling.passed(passed_rail.edge)
            
    
    def start(self) -> None:
        self.live = True
        self.set_initial_path()
        self.compute_speed_profile()
        
    def set_initial_path(self) -> None:
        path, signal = self._railway.signalling.get_initial_path(self.get_locomotive_pose())
        self.extend_path(path, signal)
        
    def signal_cleared(self, signal: Signal, path: list[Edge], next_signal: Signal) -> bool:
        self.extend_path(path, next_signal)
        self.compute_speed_profile()
        signal.subscribe(self.signal_dropped)
        
    def extend_path(self, extension: list[Edge], signal: Signal) -> None:
        self.path += [self._railway.graph.get_rail(edge) for edge in extension]
        while signal.next_signal is not None:
            self.path += [self._railway.graph.get_rail(edge) for edge in signal.path]
            signal.subscribe(self.signal_dropped)
            signal = signal.next_signal
        self._unsubscribe = signal.subscribe(self.signal_cleared)
    
    def signal_dropped(self) -> None:
        self._unsubscribe()
        self.path = self.path[:self._occupied_edge_count]
        self._routed_to_station_ahead = False
        self.set_initial_path()
        self.compute_speed_profile()
        
    def reverse(self) -> None:
        self._path_distance = self.get_distance_until_next_edge()
        self.path = [rail.reversed() for rail in reversed(self.path)]
            
    def shutdown(self) -> None:
        self.live = False
        self._railway.signalling.release_path([rail.edge for rail in self.path[self._occupied_edge_count:]])
        self.path = self.path[:self._occupied_edge_count]
        self._unsubscribe()
        self._routed_to_station_ahead = False
        
        
    def compute_speed_profile(self):
        if self._routed_to_station_ahead:
            return
        self._speed_profile = []
        speed = 0.0
        for rail in reversed(self.path[self._occupied_edge_count - 1:]):
            if not self._routed_to_station_ahead and self._railway.stations.is_edge_platform(rail.edge):
                station_id = self._railway.stations.get_edge_station(rail.edge)
                if self.schedule and station_id == self.schedule.get_next_station().id:
                    self._routed_to_station_ahead = True
                    speed = 0.0
            #add the speed at the end of this rail
            self._speed_profile.append(speed)
            speed = min(rail.speed, self.get_max_speed(rail.length, speed))
        
    def get_max_speed(self, distance: float, speed: float) -> float:
        if distance <= 1.0:
            return speed
            # FORMULA: V = sqrt(u^2 + 2as)
        return (speed**2 + (2 * distance * self.config.deceleration)) ** 0.5
                
    def get_locomotive_pose(self) -> Pose:
        return Pose.from_edge(self.path[self._occupied_edge_count - 1].edge)
    
            
    def set_schedule(self, schedule: Schedule) -> None:
        self.schedule = schedule
        
    def remove_schedule(self) -> None:
        self.schedule = None
    
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
        
    def get_distance_until_next_edge(self) -> float:
        remaining = self.config.total_length + self._path_distance
        i = 0
        while remaining - self.path[i].length > 0:
            remaining -= self.path[i].length
            i += 1
        return self.path[i].length - remaining
        
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'path': [rail.edge.to_dict_simple() for rail in self.path],
            'config': self.config.to_dict(),
            '_path_distance': self._path_distance
        }
        
    @classmethod
    def from_dict(cls, data: dict, railway: 'RailwaySystem') -> 'Train':
        edges = [Edge.from_dict(edge_data) for edge_data in data['path']]
        config = TrainConfig.from_dict(data['config'])
        train = cls(edges, railway, config)
        train.id = data['id']
        train._path_distance = data['_path_distance']
        return train