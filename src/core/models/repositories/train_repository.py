from core.models.geometry.edge import Edge
from core.models.geometry.pose import Pose
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
        platform = [edge.ordered() for edge in sorted(platform)]
        locomotive_pose = Pose.from_positions(*platform[-1])
        path, signal = self._railway.signalling.get_initial_path(locomotive_pose)
        
        train = Train(self._railway, platform, path, signal)
        
        self.add(train)
        self._railway.signalling.lock_path(platform + path)
        
    def switch_direction(self, train: Train) -> None:
        self._railway.signalling.free_path(train.path)
        edges = [edge.reversed() for edge in reversed(train.occupied_edges())]
        locomotive_pose = Pose.from_positions(edges[-1].a, edges[-1].b)
        
        path, signal = self._railway.signalling.get_initial_path(locomotive_pose)
        train.switch_direction(edges, path, signal, edge_progress=0.0)
        
        self._railway.signalling.lock_path(edges+path)

    def remove(self, train: Train) -> None:
        self._trains = [t for t in self._trains if t != train]

    def get_train_on_edge(self, edge: Edge) -> Train | None:
        for train in self._trains:
            if train.occupies_edge(edge):
                return train
        return None

    def all(self) -> list[Train]:
        return self._trains

    def get(self, index: int) -> Train:
        return self._trains[index]