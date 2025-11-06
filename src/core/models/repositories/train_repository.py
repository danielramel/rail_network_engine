from core.models.geometry.edge import Edge
from core.models.geometry.pose import Pose
from core.models.geometry.position import Position
from core.models.train import Train
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem


class TrainRepository:
    def __init__(self, railway: 'RailwaySystem') -> None:
        self._trains : list[Train] = []
        self._railway = railway

    def add(self, train: Train) -> None:
        self._trains.append(train)
        
    def add_to_platform(self, platform: frozenset[Edge]) -> None:
        platform = sorted(platform)
        locomotive_pose = Pose.from_positions(platform[-1].a, platform[-1].b)
        path, signal = self._railway.signalling.get_initial_path(locomotive_pose)
        train = Train(platform, path, signal)
        self.add(train)
        
    def switch_direction(self, train: Train) -> None:
        return
        path, signal = self._railway.signalling.get_initial_path(occupied_edges, locomotive_pos)
        train.switch_direction(tuple(reversed(occupied_edges)), path, signal)

    def remove(self, id: int) -> None:
        self._trains = [train for train in self._trains if train.id != id]
        
    def is_edge_occupied(self, edge: Edge) -> bool:
        for train in self._trains:
            if train.occupies_edge(edge):
                return True
        return False
        
    
    def get_train_on_edge(self, edge: Edge) -> Train | None:
        for train in self._trains:
            if train.occupies_edge(edge):
                return train
        return None

    def all(self) -> list[Train]:
        return self._trains

    def get(self, index: int) -> Train:
        return self._trains[index]