import networkx as nx
from models.geometry import Position, Pose
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.simulation import Simulation

class SignalService:
    """Service responsible for adding / toggling / removing signals."""
    def __init__(self, graph: nx.Graph):
        self._graph = graph

    def has_signal_at(self, pos: Position) -> bool:
        return 'signal' in self._graph.nodes[pos]
    
    def get(self, pos: Position) -> Pose | None:
        return Pose(pos, self._graph.nodes[pos]['signal'])

    def add(self, pos: Position) -> None:
        self._graph.nodes[pos]['signal'] = pos.direction_to(next(self._graph.neighbors(pos)))

    def remove(self, pos: Position) -> None:
        del self._graph.nodes[pos]['signal']

    def toggle(self, pos: Position) -> None:
        current_direction = self._graph.nodes[pos]['signal']
        neighbors = tuple(self._graph.neighbors(pos))
        if len(neighbors) < 2: raise ValueError("Cannot toggle signal at dead end")

        if pos.direction_to(neighbors[0]) == current_direction:
            self._graph.nodes[pos]['signal'] = pos.direction_to(neighbors[1])
        else:
            self._graph.nodes[pos]['signal'] = pos.direction_to(neighbors[0])

    def all(self) -> set[Pose]:
        return {Pose(node, data['signal']) for node, data in self._graph.nodes(data=True) if 'signal' in data}

