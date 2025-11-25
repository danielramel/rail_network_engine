from core.models.geometry.edge import Edge
from core.models.train import Train, TrainConfig
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem

class TrainRepository:
    def __init__(self, railway: 'RailwaySystem') -> None:
        self._trains: dict[int, Train] = {}
        self._railway = railway
        self._next_id = 0

    def _generate_id(self) -> int:
        self._next_id += 1
        return self._next_id

    def remove(self, train_id: int) -> None:
        del self._trains[train_id]

    def get_train_on_edge(self, edge: Edge) -> int | None:
        for train_id, train in self._trains.items():
            if train.occupies_edge(edge):
                return train_id
        return None

    def all(self) -> list[Train]:
        return list(self._trains.values())

    def get(self, train_id: int) -> Train:
        return self._trains[train_id]
    
    def add_to_repository(self, train: Train) -> int:
        id = self._generate_id()
        train.id = id
        self._trains[id] = train
        return id
    
    def create_train(self, edges: frozenset[Edge], config: TrainConfig) -> Train:
        sorted_edges = [edge.sorted() for edge in sorted(edges)]
        train = Train(sorted_edges, self._railway, config)
        return train
    
    def to_dict(self) -> dict:
        return {
            'trains': [train.to_dict() for train in self._trains.values()],
            "next_id": self._next_id
        }
        
    @classmethod
    def from_dict(cls, data: dict, railway: 'RailwaySystem') -> 'TrainRepository':
        instance = cls(railway)
        for train_data in data['trains']:
            train = Train.from_dict(train_data, railway)
            instance._trains[train.id] = train
            
        instance._next_id = data["next_id"]
        return instance