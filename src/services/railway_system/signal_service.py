import networkx as nx
from models.geometry import Position, Edge
from models.signal import Signal
from models.geometry import Pose
import heapq


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
        """
        priority_queue: list[tuple[float, float, Pose]] = []
        came_from: dict[Pose, Pose] = {}
        g_score: dict[Pose, float] = {}
        f_score: dict[Pose, float] = {}

        g_score[start] = 0
        f_score[start] = start.position.heuristic_to(end.position)
        heapq.heappush(priority_queue, (f_score[start], g_score[start], start))

        while priority_queue:
            current_f, current_g, current_pose = heapq.heappop(priority_queue)

            if current_pose in g_score and current_g > g_score[current_pose]:
                continue

            if current_pose.position == end:
                path = [current_pose.position]

                while current_pose in came_from:
                    current_pose = came_from[current_pose]
                    path.append(current_pose.position)

                return tuple(reversed(path))

            for neighbor_state, cost in current_pose.get_valid_neighbors():             
                tentative_g_score = g_score[current_pose] + cost

                if neighbor_state not in g_score or tentative_g_score < g_score[neighbor_state]:
                    came_from[neighbor_state] = current_pose
                    g_score[neighbor_state] = tentative_g_score
                    f_score[neighbor_state] = tentative_g_score + neighbor_state.position.heuristic_to(end.position)

                    heapq.heappush(priority_queue, (f_score[neighbor_state], g_score[neighbor_state], neighbor_state))

        return ()  # No path found
        """
    
        path = nx.shortest_path(self._graph, start.position, end.position)
        edges = [Edge(path[i], path[i+1]) for i in range(len(path)-1)]
        return edges
    
    def lock_path(self, path: list[Edge]) -> None:
        for edge in path:
            self._graph.edges[edge.a, edge.b]['locked'] = True