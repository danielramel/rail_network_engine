from core.models.geometry import Edge
from core.config.settings import FPS, TRAIN_LENGTH
from core.models.geometry.direction import Direction
from core.models.signal import Signal
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem


class Train:
    path : list[Edge]
    edge_progress : float = 1.0
    speed : float = 0.0  # in m/s
    acceleration : float = 2.0  # in km/s²
    max_speed : int  =  120  # in km/h
    deceleration : float = 5.0 # in km/s²

    def __init__(self, edges: tuple[Edge], path: tuple[Edge], signal: Signal | None = None):
        if len(edges) != TRAIN_LENGTH:
            raise ValueError("A train must occupy exactly TRAIN_LENGTH edges.")
        
        self.path = list(edges) + path
        if signal is not None:
            signal.subscribe(self.signal_turned_green_ahead)
            
    def switch_direction(self, edges: tuple[Edge], path: tuple[Edge], signal: Signal | None = None) -> None:
        if len(edges) != TRAIN_LENGTH:
            raise ValueError("A train must occupy exactly TRAIN_LENGTH edges.")
        
        self.path = list(edges) + list(path)
        self.edge_progress = 0.0
        if signal is not None:
            signal.subscribe(self.signal_turned_green_ahead)

    def direction(self) -> Direction:
        return self.path[TRAIN_LENGTH].direction
    
    def direction(self) -> Direction:
        return self.path[TRAIN_LENGTH].direction
        
    def tick(self):
        max_safe_speed = self.get_max_safe_speed()
        if self.speed > max_safe_speed:
            if self.speed - self.deceleration > max_safe_speed:
                raise ValueError("The train is going too fast to stop!!")
            self.speed = max_safe_speed
        else:
            speed_with_acc = self.speed + (self.acceleration * (1 - (self.speed / self.max_speed))/5.0)
            self.speed = min(max_safe_speed, speed_with_acc, self.max_speed)

            
        edge_progress = round(self.edge_progress + self.speed/1000, 4)
        
        if edge_progress < 1:
            self.edge_progress = edge_progress
            return
        
        self.edge_progress = edge_progress - 1
        self.path.pop(0)
        
    def occupied_edges(self) -> tuple[Edge]:
        return tuple(self.path[:TRAIN_LENGTH])
    
    def occupies_edge(self, edge: Edge) -> bool:
        return edge in self.occupied_edges()
    
    def get_locomotive_edge(self) -> Edge:
        return self.path[TRAIN_LENGTH - 1]
    def get_last_carriage_edge(self) -> Edge:
        return self.path[0]
    
    def get_locomotive_position(self) -> float:
        if self.path[TRAIN_LENGTH - 1].a == self.path[TRAIN_LENGTH - 2].b:
            return self.path[TRAIN_LENGTH - 1].b
        else:
            return self.path[TRAIN_LENGTH - 1].a
    
    
    def get_max_safe_speed(self) -> float:
        distance = len(self.path) - TRAIN_LENGTH - self.edge_progress - 0.1
        if distance <= 0:
            return 0.0
        # v_max = sqrt(2 * a * s)
        return (2 * self.deceleration * FPS * distance) ** 0.5
    
    def signal_turned_green_ahead(self, path: list[Edge], signal: Signal) -> bool:
        self.path += path
        signal.subscribe(self.signal_turned_green_ahead)