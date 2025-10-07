import networkx as nx
from models.geometry import Position, Pose


class SignalService:
    """Service responsible for adding / toggling / removing signals."""
    def __init__(self, graph: nx.Graph, map):
        self._graph = graph
        self._map = map

    def has_signal_at(self, pos: Position) -> bool:
        return 'signal' in self._graph.nodes[pos]
    
    def get(self, pos: Position) -> Pose | None:
        return Pose(pos, self._graph.nodes[pos]['signal'])

    def add(self, pos: Position) -> None:
        if self._map.is_junction(pos): raise ValueError("Cannot place signal at junction")
        if self.has_signal_at(pos): raise ValueError("Signal already exists at this position")

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

    def all(self) -> tuple[Pose]:
        return tuple(Pose(node, data['signal']) for node, data in self._graph.nodes(data=True) if 'signal' in data)

