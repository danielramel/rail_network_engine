from dataclasses import dataclass
from models.geometry.pose import Pose
from models.geometry.position import Position

@dataclass
class Train:
    id: int
    code: str
    edges: list[tuple[Position, Position]] # the order of the positions matters
    
    def get_direction(self) -> tuple[int, int]:
        return self.edges[0][0].direction_to(self.edges[0][1])
        
        
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