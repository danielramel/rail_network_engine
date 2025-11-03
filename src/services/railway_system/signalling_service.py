import heapq
from typing import Optional
from models.geometry import Position, Edge
from models.signal import Signal
from models.geometry import Pose
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.railway_system import RailwaySystem

class SignallingService:
    def __init__(self, railway: 'RailwaySystem'):
        self._railway = railway
        
    def is_edge_locked(self, edge: Edge) -> bool:
        return self._railway.graph.get_edge_attr(edge, 'locked') is True
    
    

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
                if not self._railway.graph.has_edge(Edge(current_pose.position, neighbor_pose.position)):
                    continue
                if self._railway.graph.get_edge_attr(Edge(current_pose.position, neighbor_pose.position), 'locked'):
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
            self._railway.graph.set_edge_attr(edge, 'locked', True)

    def get_initial_path(self, start_edge: Edge) -> tuple[list[Edge], Optional[Signal]]:
        visited = {start_edge.a, start_edge.b}
        pos = start_edge.b
        path = []
        while True:
            if self._railway.signals.has_signal_at(pos):
                signal = self._railway.signals.get(pos)
                if not signal.is_green:
                    return path, signal

            neighbors = self._railway.graph.neighbors(pos)
            if len(neighbors) == 1:
                path.append(Edge(pos, neighbors[0]))
                visited.add(pos)
                return path, None
            
            if neighbors[0] in visited and neighbors[1] in visited:
                return path, None
            
            next_pos = neighbors[0] if neighbors[0] not in visited else neighbors[1]

            visited.add(next_pos)
            path.append(Edge(pos, next_pos))
            pos = next_pos