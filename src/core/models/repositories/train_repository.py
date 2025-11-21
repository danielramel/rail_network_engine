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
    
    def add_to_platform_edge(self, edge: Edge, config: TrainConfig) -> int:
        platform = [edge.ordered() for edge in sorted(self._railway.stations.get_platform_from_edge(edge))]
        id = self._generate_id()
        train = Train(id, platform, self._railway, config)

        self._trains[id] = train
        self._railway.signalling.lock_path(platform)
        return id
    
    def get_preview_train_on_platform_edge(self, edge: Edge, config: TrainConfig) -> Train:
        platform = [edge.ordered() for edge in sorted(self._railway.stations.get_platform_from_edge(edge))]
        id = -1  # Preview trains have negative IDs
        train = Train(id, platform, self._railway, config)
        return train