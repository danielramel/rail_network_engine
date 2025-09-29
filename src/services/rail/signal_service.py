from networkx import Graph
from models.position import Position, PositionWithDirection


class SignalService:
    """Service responsible for adding / toggling / removing signals."""
    def __init__(self, graph: Graph):
        self._graph = graph

    def has_signal_at(self, pos: Position) -> bool:
        if not self._graph.has_node(pos):
            return False
        return 'signal' in self._graph.nodes[pos]

    def add_signal(self, signal: PositionWithDirection) -> None:
        if self._graph.degree(signal.position) > 2: raise ValueError("Cannot place signal at intersection")
        if self.has_signal_at(signal.position): raise ValueError("Signal already exists at this position")

        self._graph.nodes[signal.position]['signal'] = signal.direction

    def remove_signal(self, pos: Position) -> None:
        del self._graph.nodes[pos]['signal']

    def toggle_signal(self, pos: Position) -> None:
        current_direction = self._graph.nodes[pos]['signal']
        neighbors = tuple(self._graph.neighbors(pos))
        if len(neighbors) < 2: raise ValueError("Cannot toggle signal at dead end")

        if pos.direction_to(neighbors[0]) == current_direction:
            self._graph.nodes[pos]['signal'] = pos.direction_to(neighbors[1])
        else:
            self._graph.nodes[pos]['signal'] = pos.direction_to(neighbors[0])

    def get_all_signals(self) -> tuple[PositionWithDirection]:
        return tuple(PositionWithDirection(node, data['signal']) for node, data in self._graph.nodes(data=True) if 'signal' in data)

