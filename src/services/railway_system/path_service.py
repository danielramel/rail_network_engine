from config.settings import GRID_SIZE
from models.geometry import Position, Pose
import heapq

from typing import TYPE_CHECKING

from models.geometry.direction import Direction
if TYPE_CHECKING:
    from models.railway_system import RailwaySystem


class PathService:
    def __init__(self, railway: 'RailwaySystem'):
        self._railway = railway

    def is_blocked(self, pos: Position) -> bool:
        return (self._railway.graph.has_node_at(pos) and 
                (self._railway.signals.has_signal_at(pos) 
                 or self._railway.platforms.is_platform_at(pos))) or self._railway.stations.is_within_any(pos)

    def is_cutting_through_platform(self, current_state: Pose, neighbor_state: Pose) -> bool:
        if neighbor_state.direction not in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            return False
        # Check for corner cutting
        corner1 = Position(current_state.position.x + neighbor_state.direction[0] * GRID_SIZE, current_state.position.y)
        corner2 = Position(current_state.position.x, current_state.position.y + neighbor_state.direction[1] * GRID_SIZE)
        return self._railway.graph.has_edge((corner1, corner2)) and self._railway.platforms.is_edge_platform((corner1, corner2))

        
    def find_grid_path(self, start: Pose, end: Position) -> tuple[Position, ...]:
        """
        Find optimal path using A* algorithm with 45° turn constraint.
        """
        def get_valid_turn_neighbors(state: Pose) -> list[tuple[Pose, float]]:

            neighbors = []
            for dir in Pose.get_valid_turns(state.direction):
                nx = state.position.x + dir.x * GRID_SIZE
                ny = state.position.y + dir.y * GRID_SIZE
                new_state = Pose(Position(nx, ny), dir)

                neighbors.append((new_state, dir.get_cost()))
            return neighbors

        def heuristic(a: Position, b: Position) -> float:
            return (b.x - a.x) ** 2 + (b.y - a.y) ** 2  # Squared Euclidean distance
        
        
        if self.is_blocked(end) or self.is_blocked(start.position):
            return ()

        if start.position == end:
            return (start.position,)

        priority_queue: list[tuple[float, float, Pose]] = []
        came_from: dict[Pose, Pose] = {}
        g_score: dict[Pose, float] = {}
        f_score: dict[Pose, float] = {}

        g_score[start] = 0
        f_score[start] = heuristic(start.position, end)
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

            for neighbor_state, cost in get_valid_turn_neighbors(current_pose):
                if self.is_blocked(neighbor_state.position):
                    continue
                
                if self.is_cutting_through_platform(current_pose, neighbor_state):
                    continue

                tentative_g_score = g_score[current_pose] + cost

                if neighbor_state not in g_score or tentative_g_score < g_score[neighbor_state]:
                    came_from[neighbor_state] = current_pose
                    g_score[neighbor_state] = tentative_g_score
                    f_score[neighbor_state] = tentative_g_score + heuristic(neighbor_state.position, end)

                    heapq.heappush(priority_queue, (f_score[neighbor_state], g_score[neighbor_state], neighbor_state))

        return ()  # No path found