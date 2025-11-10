from core.models.geometry.edge import Edge
from core.models.geometry.pose import Pose
from core.models.train import Train
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

    def add_to_platform(self, platform: frozenset[Edge]) -> int:
        platform = [edge.ordered() for edge in sorted(platform)]
        id = self._generate_id()
        train = Train(id, platform)

        self._trains[id] = train
        self._railway.signalling.lock_path(platform)
        return id
    
    def get_preview_train_on_platform(self, platform: frozenset[Edge]) -> Train:
        platform = [edge.ordered() for edge in sorted(platform)]
        id = -1  # Preview trains have negative IDs
        train = Train(id, platform)
        return train

    # def switch_direction(self, train_id: int) -> None:
        #     locomotive_pose = Pose.from_positions(*platform[-1])
        # path, signal = self._railway.signalling.get_initial_path(locomotive_pose)
    #     train = self._trains[train_id]
    #     self._railway.signalling.free_path(train.path)
    #     edges = [edge.reversed() for edge in reversed(train.occupied_edges())]
    #     locomotive_pose = Pose.from_positions(edges[-1].a, edges[-1].b)

    #     path, signal = self._railway.signalling.get_initial_path(locomotive_pose)
    #     train.switch_direction(edges, path, signal, edge_progress=0.0)

    #     self._railway.signalling.lock_path(edges + path)

    def remove(self, train_id: int) -> None:
        if train_id in self._trains:
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