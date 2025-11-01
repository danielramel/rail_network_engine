import networkx as nx
from models.geometry import Position, Edge
from models.signal import Signal


class SignalService:
    """Service responsible for adding / toggling / removing signals."""
    def __init__(self, graph: nx.Graph):
        self._graph = graph

    def has_signal_at(self, pos: Position) -> bool:
        return 'signal' in self._graph.nodes[pos]
    
    def get(self, pos: Position) -> Signal:
        return self._graph.nodes[pos]['signal']

    def add(self, pos: Position) -> None:
        self._graph.nodes[pos]['signal'] = Signal(pos, pos.direction_to(next(self._graph.neighbors(pos))))

    def remove(self, pos: Position) -> None:
        del self._graph.nodes[pos]['signal']

    def toggle_direction(self, pos: Position) -> None:
        current_direction = self._graph.nodes[pos]['signal'].direction
        neighbors = tuple(self._graph.neighbors(pos))
        if len(neighbors) < 2: raise ValueError("Cannot toggle signal at dead end")

        if pos.direction_to(neighbors[0]) == current_direction:
            self._graph.nodes[pos]['signal'].direction = pos.direction_to(neighbors[1])
        else:
            self._graph.nodes[pos]['signal'].direction = pos.direction_to(neighbors[0])

    def all(self) -> tuple[Signal]:
        return tuple(data["signal"] for node, data in self._graph.nodes(data=True) if 'signal' in data)
    
    def find_path(self, start: Signal, end: Signal) -> list[Position]:
        path = nx.shortest_path(self._graph, start.position, end.position)
        edges = [Edge(path[i], path[i+1]) for i in range(len(path)-1)]
        return edges
    
    def lock_path(self, path: list[Edge]) -> None:
        for edge in path:
            self._graph.edges[edge.a, edge.b]['locked'] = True