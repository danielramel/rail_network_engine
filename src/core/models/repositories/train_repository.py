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
        
    def add_to_platform(self, platform: frozenset[Edge], locomotive_pose: Pose) -> None:
        self._railway.signalling.get_initial_path(platform, locomotive_pose)

    def remove(self, id: int) -> None:
        self._trains = [train for train in self._trains if train.id != id]

    def all(self) -> list[Train]:
        return self._trains

    def get(self, index: int) -> Train:
        return self._trains[index]