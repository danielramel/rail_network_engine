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
    edge_progress : float = 0.25
    speed : float = 0.0  # in m/s
    acceleration : float = 1.2  # in m/s²
    max_speed : int  =  120  # in km/h
    deceleration : float = 1.4 # in m/s²
    timetable : TimeTable = None
    _is_live : bool = False
    is_shutting_down : bool = False
    _railway: 'RailwaySystem'

    def __init__(self, id: int, edges: list[Edge], railway: 'RailwaySystem'):
        if len(edges) != PLATFORM_LENGTH:
            raise ValueError("A train must occupy exactly PLATFORM_LENGTH edges.")
        self.id = id
        self.path = edges
        self._railway = railway
        
    def set_timetable(self, timetable: TimeTable) -> None:
        self.timetable = timetable
        
    def reverse(self) -> None:
        if self.edge_progress < 0.5:
            for edge in self.path[self.occupied_edge_count:]:
                self._railway.signalling.passed([edge])
            
            self.edge_progress = 0.5 - self.edge_progress
            self.path = [edge.reversed() for edge in self.path[self.occupied_edge_count-1::-1]]
        else:
            raise NotImplementedError("Reversing a train that is past the halfway point of an edge is not implemented.")
        
        
    def tick(self):
        if not self._is_live:
            return
        
        if self.is_shutting_down:
            self.speed = max(0.0, self.speed - self.deceleration/FPS)
            if self.speed == 0.0:
                self._shutdown()
                return
                
        else:
            max_safe_speed = self.get_max_safe_speed()
            if self.speed > max_safe_speed:
                self.speed = max(max_safe_speed, 0.0)
            else:
                speed_with_acc = self.speed + (self.acceleration/FPS)
                self.speed = min(max_safe_speed, speed_with_acc, self.max_speed/3.6)
                
            if self.speed == 0.0:
                return

        edge_length = self._railway.graph.get_edge_attr(self.path[self.occupied_edge_count-1], 'length')
        travel_progress = self.speed/edge_length/FPS
        edge_progress = self.edge_progress + travel_progress
        if edge_progress < 1:
            if self.edge_progress < 0.5 <= edge_progress:
                edge = self.path.pop(0)
                self._railway.signalling.passed(edge)
            self.edge_progress = round(edge_progress, 6)
            return
        
        next_edge_length = self._railway.graph.get_edge_attr(self.path[self.occupied_edge_count], 'length')
        edge_progress -= 1
        edge_progress = edge_progress * edge_length / next_edge_length
        self.edge_progress = round(edge_progress, 6)

    @property
    def occupied_edge_count(self) -> int:
        #TODO: in case of different track length this needs to be updated
        return PLATFORM_LENGTH if self.edge_progress < 0.5 else PLATFORM_LENGTH - 1
        
    def get_occupied_edges(self) -> tuple[Edge]:
        return tuple(self.path[:self.occupied_edge_count])
    
    def occupies_edge(self, edge: Edge) -> bool:
        return edge in self.get_occupied_edges()
    
    @property
    def is_live(self) -> bool:
        return self._is_live
    
    def start(self) -> None:
        self._is_live = True
        path, signal = self._railway.signalling.get_initial_path(self.get_locomotive_pose())
        self.path += path
        signal.subscribe(self.signal_turned_green_ahead)
        
    def _shutdown(self) -> None:    
        self._is_live = False
        self._railway.signalling.unlock_path(self.path[self.occupied_edge_count:])
        
    def get_locomotive_pose(self) -> Pose:
        edge = self.path[self.occupied_edge_count - 1]
        return Pose.from_edge(edge)
    
    def get_max_safe_speed(self) -> float:
        # sum physical lengths of remaining edges
        remaining_edges = self.path[self.occupied_edge_count-1:]
        if not remaining_edges:
            return 0.0
        distance = (1 - self.edge_progress) * self._railway.graph.get_edge_attr(remaining_edges[0], 'length')
        distance += sum(self._railway.graph.get_edge_attr(edge, 'length') for edge in remaining_edges[1:])
        distance = max(0, distance - 50)
        return (2 * distance * self.deceleration ) ** 0.5
    
    def signal_turned_green_ahead(self, path: list[Edge], signal: Signal) -> bool:
        self.path += path
        signal.subscribe(self.signal_turned_green_ahead)