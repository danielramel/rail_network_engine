from core.models.geometry import Edge
from core.config.settings import FPS, PLATFORM_LENGTH
from core.models.geometry.pose import Pose
from core.models.signal import Signal
from core.models.timetable import TimeTable
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem


class Train:
    id : int
    path : list[Edge]
    edge_progress : float = 0.0
    speed : float = 0.0  # in m/s
    acceleration : float = 2.0  # in km/s²
    max_speed : int  =  120  # in km/h
    deceleration : float = 5.0 # in km/s²
    timetable : TimeTable = None
    _is_live : bool = False
    _railway: 'RailwaySystem'

    def __init__(self, id: int, edges: list[Edge], railway: 'RailwaySystem'):
        if len(edges) != PLATFORM_LENGTH:
            raise ValueError("A train must occupy exactly PLATFORM_LENGTH edges.")
        self.id = id
        self.path = edges
        self._railway = railway
        
    def set_timetable(self, timetable: TimeTable) -> None:
        self.timetable = timetable
        
    def tick(self):
        max_safe_speed = self.get_max_safe_speed()
        if self.speed > max_safe_speed:
            if self.speed - self.deceleration > max_safe_speed:
                raise ValueError("The train is going too fast to stop!!")
            self.speed = max_safe_speed
        else:
            speed_with_acc = self.speed + (self.acceleration * (1 - (self.speed / self.max_speed))/5.0)
            self.speed = min(max_safe_speed, speed_with_acc, self.max_speed)

        edge_length = self._railway.graph.get_edge_attr(self.path[PLATFORM_LENGTH-1], 'length')
        edge_progress = round(self.edge_progress + self.speed/3.6/FPS/edge_length, 4)
        
        if edge_progress < 1:
            self.edge_progress = edge_progress
            return
        
        self.edge_progress = edge_progress - 1
        edge = self.path.pop(0)
        self._railway.signalling.free([edge])
        
    def get_occupied_edges(self) -> tuple[Edge]:
        return tuple(self.path[:PLATFORM_LENGTH])
    
    def occupies_edge(self, edge: Edge) -> bool:
        return edge in self.get_occupied_edges()
    
    @property
    def is_live(self) -> bool:
        return self._is_live
    
    def set_start_callback(self, callback) -> None:
        self._on_start = callback
    
    def start(self) -> None:
        self._is_live = True
        path, signal = self._railway.signalling.set_inital_train_path(self)
        self.path += path
        signal.subscribe(self.signal_turned_green_ahead)
        
    def shutdown(self) -> None:
        self._is_live = False
        self.timetable = None
        
    def get_locomotive_pose(self) -> Pose:
        edge = self.path[PLATFORM_LENGTH - 1]
        return Pose.from_positions(edge.a, edge.b)
    
    def get_max_safe_speed(self) -> float:
        distance = len(self.path) - (PLATFORM_LENGTH) - self.edge_progress - 0.1
        if distance <= 0:
            return 0.0
        # v_max = sqrt(2 * a * s)
        return (2 * self.deceleration * FPS * distance) ** 0.5
    
    def signal_turned_green_ahead(self, path: list[Edge], signal: Signal) -> bool:
        self.path += path
        signal.subscribe(self.signal_turned_green_ahead)