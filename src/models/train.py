from dataclasses import dataclass
from models.geometry.position import Position
from config.settings import TRAIN_LENGTH

@dataclass
class Train:
    id: int
    code: str
    edges: list[tuple[Position, Position]]  # the order of the positions matters
    edge_progress : float = 0.0
    max_speed: int = 100  # in km/h, default 100

    def get_direction(self) -> tuple[int, int]:
        return self.edges[0][0].direction_to(self.edges[0][1])

    def tick(self):
        edge_progress = self.edge_progress + self.max_speed/1000
        if edge_progress < 1:
            self.edge_progress = edge_progress
            return
        
        edge_progress -= 1
        self.edges.pop(0)
        
        
    def occupied_edges(self) -> tuple[tuple[Position, Position]]:
        """Get the list of edges currently occupied by the train based on its position."""
        return tuple(reversed(self.edges[:TRAIN_LENGTH]))
        
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