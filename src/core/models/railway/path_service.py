from core.config.settings import GRID_SIZE
from core.models.geometry import Position, Pose, Edge
import heapq

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem


class PathService:
    def __init__(self, railway: 'RailwaySystem'):
        self._railway = railway

    def is_blocked(self, pos: Position) -> bool:
        return self._railway.stations.is_within_any(pos)

    def is_cutting_through_platform(self, current_state: Pose, neighbor_state: Pose) -> bool:
        if neighbor_state.direction not in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            return False
        # Check for corner cutting
        corner1 = Position(current_state.position.x + neighbor_state.direction[0] * GRID_SIZE, current_state.position.y)
        corner2 = Position(current_state.position.x, current_state.position.y + neighbor_state.direction[1] * GRID_SIZE)
        return self._railway.stations.is_edge_platform(Edge(corner1, corner2))

        
    def find_grid_path(self, start: Pose, end: Position) -> tuple[Position, ...]:
        """
        Find optimal path using A* algorithm with 45° turn constraint. #TODO a* is not good here because of the bad heuristic
        """
        if self.is_blocked(end) or self.is_blocked(start.position):
            return ()

        if start.position == end:
            return (start.position,)

        priority_queue: list[tuple[float, float, Pose]] = []
        came_from: dict[Pose, Pose] = {}
        g_score: dict[Pose, float] = {}
        f_score: dict[Pose, float] = {}

        g_score[start] = 0
        f_score[start] = start.position.heuristic_to(end)
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

            for neighbor_pose, cost in current_pose.get_neighbors_in_direction():
                if self.is_blocked(neighbor_pose.position):
                    continue
                
                if self.is_cutting_through_platform(current_pose, neighbor_pose):
                    continue
                
                if self._railway.signals.has_signal_at(neighbor_pose.position):
                    #TODO: enforece this on start_pose as well
                    signal = self._railway.signals.get(neighbor_pose.position)
                    if neighbor_pose.direction not in (signal.direction, signal.direction.opposite()):
                        continue
                
                if not self._railway.graph.has_edge(Edge(current_pose.position, neighbor_pose.position)):
                    platform1 = self._railway.graph.has_node_at(current_pose.position) and self._railway.stations.get_platform_at(current_pose.position)
                    platform2 = self._railway.graph.has_node_at(neighbor_pose.position) and self._railway.stations.get_platform_at(neighbor_pose.position)
                    if platform1 or platform2 and platform1 != platform2:
                        continue
                    

                tentative_g_score = g_score[current_pose] + cost

                if neighbor_pose not in g_score or tentative_g_score < g_score[neighbor_pose]:
                    came_from[neighbor_pose] = current_pose
                    g_score[neighbor_pose] = tentative_g_score
                    f_score[neighbor_pose] = tentative_g_score + neighbor_pose.position.heuristic_to(end)

                    heapq.heappush(priority_queue, (f_score[neighbor_pose], g_score[neighbor_pose], neighbor_pose))

        return ()  # No path found