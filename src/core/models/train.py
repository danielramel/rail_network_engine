from core.models.geometry import Edge
from core.config.settings import FPS, PLATFORM_LENGTH
from core.models.signal import Signal


class Train:
    id : int
    path : list[Edge]
    edge_progress : float = 0.0
    speed : float = 0.0  # in m/s
    acceleration : float = 2.0  # in km/s²
    max_speed : int  =  120  # in km/h
    deceleration : float = 5.0 # in km/s²

    def __init__(self, id: int, edges: list[Edge]):
        if len(edges) != PLATFORM_LENGTH:
            raise ValueError("A train must occupy exactly PLATFORM_LENGTH edges.")
        self.id = id
        self.path = edges
        
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
        edge = self.path.pop(0)
        self._railway.signalling.free_edge(edge)
        
    def occupied_edges(self) -> tuple[Edge]:
        return tuple(self.path[:PLATFORM_LENGTH])
    
    def occupies_edge(self, edge: Edge) -> bool:
        return edge in self.occupied_edges()    
    
    def get_max_safe_speed(self) -> float:
        distance = len(self.path) - (PLATFORM_LENGTH) - self.edge_progress - 0.1
        if distance <= 0:
            return 0.0
        # v_max = sqrt(2 * a * s)
        return (2 * self.deceleration * FPS * distance) ** 0.5
    
    def signal_turned_green_ahead(self, path: list[Edge], signal: Signal) -> bool:
        self.path += path
        signal.subscribe(self.signal_turned_green_ahead)