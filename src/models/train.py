from dataclasses import dataclass
from models.geometry import Edge
from config.settings import TRAIN_LENGTH
from models.geometry.direction import Direction

@dataclass
class Train:
    id: int
    code: str
    path: list[Edge]
    edge_progress : float = 0.0
    max_speed: int = 100  # in km/h, default 100
    acceleration: float = 1
    speed : int = 0  # in km/h, current speed
    
    def direction(self) -> Direction:
        return self.path[TRAIN_LENGTH].direction
        
    def tick(self):
        if self.speed < self.max_speed:
            # scale acceleration down as speed approaches max_speed (more realistic)
            ratio = (self.speed / self.max_speed)
            scaled_acc = self.acceleration * (1 - ratio)
            # ensure a small minimal acceleration so it still approaches max (adjust factor as needed)
            delta = scaled_acc / 7.0
            self.speed = min(self.speed + delta, self.max_speed)
            
        edge_progress = round(self.edge_progress + self.speed/1000, 4)
        
        if edge_progress < 1:
            self.edge_progress = edge_progress
            return
        
        self.edge_progress = edge_progress - 1
        self.path.pop(0)
        
    def occupied_edges(self) -> tuple[Edge]:
        return tuple(reversed(self.path[:TRAIN_LENGTH]))
        
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
    
    
    
"""
# using u^2 = v^2 - 2as
            distance_to_next_semaphore = sqrt(abs(self.next_semaphore.point._x-self._x)**2+abs(self.next_semaphore.point._y-self._y)**2)

            optimal_speed = sqrt(self.target_speed**2 + 2*self.deceleration*abs(distance_to_next_semaphore-0.02)/GAME_SPEED)-self.deceleration*0.6

            if optimal_speed < self.current_speed - self.deceleration:
                raise ValueError("The train is going too fast to stop at the next semaphore!")
            
            if optimal_speed < self.current_speed:
                self.current_speed = max(0, optimal_speed)

            else:
                self.current_speed = min(optimal_speed, self.current_speed + self.acceleration, self.max_allowed_speed)


"""