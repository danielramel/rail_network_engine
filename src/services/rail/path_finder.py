from config.settings import GRID_SIZE
from models.geometry import Position, Pose
import heapq

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.map import RailMap


class Pathfinder:
    def __init__(self, map: 'RailMap'):
        self._map = map

    def is_blocked(self, pos: Position) -> bool:
        return (self._map.has_node_at(pos) and 
                (self._map.has_signal_at(pos) 
                 or self._map.is_platform_at(pos))) or self._map.is_within_station_rect(pos)

    def is_cutting_through_platform(self, current_state: Pose, neighbor_state: Pose) -> bool:
        if neighbor_state.direction not in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            return False
        # Check for corner cutting
        corner1 = Position(current_state.position.x + neighbor_state.direction[0] * GRID_SIZE, current_state.position.y)
        corner2 = Position(current_state.position.x, current_state.position.y + neighbor_state.direction[1] * GRID_SIZE)
        return self._map.has_edge((corner1, corner2)) and self._map.is_edge_platform((corner1, corner2))

        
    def find_grid_path(self, start: Pose, end: Position) -> tuple[Position, ...]:
        """
        Find optimal path using A* algorithm with 45° turn constraint.
        """
        def get_valid_turn_neighbors(state: Pose) -> list[tuple[Pose, float]]:
            def get_direction_cost(direction: tuple[int, int]) -> float:
                return 1.0 if direction[0] == 0 or direction[1] == 0 else 1.414
            
            neighbors = []
            for dx, dy in Pose.get_valid_turns(state.direction):
                nx = state.position.x + dx * GRID_SIZE
                ny = state.position.y + dy * GRID_SIZE
                new_state = Pose(Position(nx, ny), (dx, dy))
                cost = get_direction_cost((dx, dy))
                neighbors.append((new_state, cost))
            return neighbors

        def heuristic(a: Position, b: Position) -> float:
            return max(abs(a.x - b.x) / GRID_SIZE, abs(a.y - b.y) / GRID_SIZE)
        
        
        if self.is_blocked(end) or self.is_blocked(start.position):
            return ()

        if start.position == end:
            return (start.position,)

        open_set = []
        came_from: dict[Pose, Pose] = {}
        g_score: dict[Pose, float] = {}
        f_score: dict[Pose, float] = {}

        g_score[start] = 0
        f_score[start] = heuristic(start.position, end)
        heapq.heappush(open_set, (f_score[start], g_score[start], start))

        while open_set:
            current_f, current_g, current_state = heapq.heappop(open_set)

            if current_state in g_score and current_g > g_score[current_state]:
                continue

            if current_state.position == end:
                path = [current_state.position]

                while current_state in came_from:
                    current_state = came_from[current_state]
                    path.append(current_state.position)

                return tuple(reversed(path))

            for neighbor_state, cost in get_valid_turn_neighbors(current_state):
                if self.is_blocked(neighbor_state.position):
                    continue
                
                if self.is_cutting_through_platform(current_state, neighbor_state):
                    continue

                tentative_g_score = g_score[current_state] + cost

                if neighbor_state not in g_score or tentative_g_score < g_score[neighbor_state]:
                    came_from[neighbor_state] = current_state
                    g_score[neighbor_state] = tentative_g_score
                    f_score[neighbor_state] = tentative_g_score + heuristic(neighbor_state.position, end)

                    heapq.heappush(open_set, (f_score[neighbor_state], g_score[neighbor_state], neighbor_state))

        return ()  # No path found
    
    def find_network_path(self, start: Position, end: Position) -> tuple[Position, ...]:
        if not (self._map.has_node_at(start) and self._map.has_node_at(end)):
            return ()
        
        
