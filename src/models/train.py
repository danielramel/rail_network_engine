from dataclasses import dataclass
from models.geometry.position import Position
from config.settings import TRAIN_LENGTH

@dataclass
class Train:
    id: int
    code: str
    path: list[tuple[Position, Position]]  # the order of the positions matters
    edge_progress : float = 0.0
    max_speed: int = 100  # in km/h, default 100
    acceleration: float = 1
    speed : int = 0  # in km/h, current speed
    
    def direction(self) -> tuple[int, int]:
        return (self.path[TRAIN_LENGTH][1].x - self.path[TRAIN_LENGTH][0].x, self.path[TRAIN_LENGTH][1].y - self.path[TRAIN_LENGTH][0].y)
        
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
        
    def occupied_edges(self) -> tuple[tuple[Position, Position]]:
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