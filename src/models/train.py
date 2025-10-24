from dataclasses import dataclass
from models.geometry.edge import Edge

@dataclass
class Train:
    id: int
    code: str
    edges: list[Edge]
    direction: tuple[int, int]
    
        
        
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