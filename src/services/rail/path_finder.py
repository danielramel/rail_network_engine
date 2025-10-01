from config.settings import GRID_SIZE
from models.geometry import Position, Pose
import heapq


class Pathfinder:
    def __init__(self, map):
        self._map = map

    def get_direction_cost(self, direction: tuple[int, int]) -> float:
        return 1.0 if direction[0] == 0 or direction[1] == 0 else 1.414

    def get_valid_turn_neighbors(self, state: Pose) -> list[tuple[Pose, float]]:
        """
        Get valid neighboring states from current state, respecting 45° turn limit.
        """
        neighbors = []
        valid_directions = Pose.get_valid_turns(state.direction)
        for dx, dy in valid_directions:
            nx = state.position.x + dx * GRID_SIZE
            ny = state.position.y + dy * GRID_SIZE
            new_state = Pose(Position(nx, ny), (dx, dy))
            cost = self.get_direction_cost((dx, dy))
            neighbors.append((new_state, cost))
        return neighbors

    def heuristic(self, a: Position, b: Position) -> float:
        """
        Calculate heuristic distance between two points.
        Uses Chebyshev distance for 8-directional movement.
        """
        dx = abs(a.x - b.x) / GRID_SIZE
        dy = abs(a.y - b.y) / GRID_SIZE
        return max(dx, dy)

    def reconstruct_path(self, came_from: dict[Pose, Pose], current_state: Pose) -> tuple[Position, ...]:
        """Reconstruct and simplify the path from states."""
        path = [current_state.position]

        while current_state in came_from:
            current_state = came_from[current_state]
            path.append(current_state.position)

        return tuple(reversed(path))

    def is_blocked(self, pos: Position) -> bool:
        return (self._map.has_node_at(pos)
            and (self._map.has_signal_at(pos) or self._map.is_platform_at(pos)))

    def find_path(self, start: Pose, end: Position) -> tuple[Position, ...]:
        """
        Find optimal path using A* algorithm with 45° turn constraint.
        """
        if self.is_blocked(end) or self.is_blocked(start.position):
            return ()

        if start.position == end:
            return (start.position,)

        open_set = []
        came_from: dict[Pose, Pose] = {}
        g_score: dict[Pose, float] = {}
        f_score: dict[Pose, float] = {}

        g_score[start] = 0
        f_score[start] = self.heuristic(start.position, end)
        heapq.heappush(open_set, (f_score[start], g_score[start], start))

        while open_set:
            current_f, current_g, current_state = heapq.heappop(open_set)

            if current_state in g_score and current_g > g_score[current_state]:
                continue

            if current_state.position == end:
                return self.reconstruct_path(came_from, current_state)

            for neighbor_state, cost in self.get_valid_turn_neighbors(current_state):
                if self.is_blocked(neighbor_state.position):
                    continue

                tentative_g_score = g_score[current_state] + cost

                if neighbor_state not in g_score or tentative_g_score < g_score[neighbor_state]:
                    came_from[neighbor_state] = current_state
                    g_score[neighbor_state] = tentative_g_score
                    f_score[neighbor_state] = tentative_g_score + self.heuristic(neighbor_state.position, end)

                    heapq.heappush(open_set, (f_score[neighbor_state], g_score[neighbor_state], neighbor_state))

        return ()  # No path found
