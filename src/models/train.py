from dataclasses import dataclass
from models.geometry import Edge
from config.settings import FPS, TRAIN_LENGTH
from models.geometry.direction import Direction

@dataclass
class Train:
    id: int
    code: str
    path: list[Edge]
    edge_progress : float = 0.0
    max_speed: int = 100  # in km/h, default 100
    speed : int = 0  # in km/h, current speed
    acceleration: float = 5
    deceleration: int = 10
    
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
        return tuple(reversed(self.path[:TRAIN_LENGTH]))
    
    def get_max_safe_speed(self) -> float:
        distance = len(self.path) - TRAIN_LENGTH - self.edge_progress - 0.5
        if distance <= 0:
            return 0.0
        # v_max = sqrt(2 * a * s)
        return (2 * self.deceleration * FPS * distance) ** 0.5




class TrainRepository:
    def __init__(self):
        self._trains : list[Train] = []

    def add(self, train: Train) -> None:
        self._trains.append(train)

    def remove(self, train: Train) -> None:
        self._trains.remove(train)

    def all(self) -> list[Train]:
        return self._trains

    def get(self, index: int) -> Train:
        return self._trains[index]