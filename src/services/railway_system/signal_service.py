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

    def add(self, pose: Pose) -> None:
        self._graph.nodes[pose.position]['signal'] = Signal(pose)

    def remove(self, pos: Position) -> None:
        del self._graph.nodes[pos]['signal']

    def toggle(self, pose: Pose) -> None:
        self.remove(pose.position)
        self.add(pose)

    def all(self) -> tuple[Signal]:
        return tuple(data["signal"] for node, data in self._graph.nodes(data=True) if 'signal' in data)

    def _calculate_optimal_route(self, start: Pose, end: Pose) -> list[Position]:

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

            if current_pose == end:
                path = [current_pose.position]

                while current_pose in came_from:
                    current_pose = came_from[current_pose]
                    path.append(current_pose.position)

                return tuple(reversed(path))

            for neighbor_pose, cost in current_pose.get_neighbors_in_direction():
                if not self._graph.has_edge(current_pose.position, neighbor_pose.position):
                    continue
                
                tentative_g_score = g_score[current_pose] + cost

                if neighbor_pose not in g_score or tentative_g_score < g_score[neighbor_pose]:
                    came_from[neighbor_pose] = current_pose
                    g_score[neighbor_pose] = tentative_g_score
                    f_score[neighbor_pose] = tentative_g_score + neighbor_pose.position.heuristic_to(end.position)

                    heapq.heappush(priority_queue, (f_score[neighbor_pose], g_score[neighbor_pose], neighbor_pose))

        return None
        
    def find_path(self, start: Signal, end: Signal) -> list[Edge] | None:
        path = self._calculate_optimal_route(start.pose, end.pose)
        if path is None:
            return None
        edges = [Edge(path[i], path[i+1]) for i in range(len(path)-1)]
        return edges
    
    def lock_path(self, path: list[Edge]) -> None:
        for edge in path:
            self._graph.edges[edge.a, edge.b]['locked'] = True