from core.models.geometry import Position, Pose, Edge
import heapq

from typing import TYPE_CHECKING

from core.models.geometry.direction import Direction
if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem


class PathService:
    def __init__(self, railway: 'RailwaySystem'):
        self._railway = railway


        
    def find_grid_path(self, start: Pose, end: Position) -> tuple[Position, ...]:
        def is_pose_blocked(pose: Pose) -> bool:
            if self._railway.stations.is_within_any(pose.position):
                return True
            
            if pose.direction == Direction(0,0):
                return False
            if self._railway.signals.has_signal_at(pose.position):
                signal = self._railway.signals.get(pose.position)
                if pose not in (signal.pose, signal.pose.opposite()):
                    return True
            return False
        
        def is_edge_blocked(edge: Edge) -> bool:
            if self._railway.stations.is_platform_at(edge.a):
                neighbors = self._railway.graph.neighbors(edge.a)
                if len(neighbors) == 2 and edge.b not in neighbors:
                    return True
                
            if self._railway.stations.is_platform_at(edge.b):
                neighbors = self._railway.graph.neighbors(edge.b)
                if len(neighbors) == 2 and edge.a not in neighbors:
                    return True
            
            # check for diagonal platform cutting
            if not edge.direction.is_diagonal():
                return False

            return self._railway.stations.is_edge_platform(Edge(Position(edge.a.x, edge.b.y), Position(edge.b.x, edge.a.y)))
    
            
        if is_pose_blocked(start) or is_pose_blocked(Pose(end, Direction(0,0))):
            raise ValueError("Start or end position is blocked")

        if start.position == end:
            return (start.position,)

        priority_queue: list[tuple[float, Pose]] = []
        came_from: dict[Pose, Pose] = {}
        g_score: dict[Pose, float] = {}
        f_score: dict[Pose, float] = {}

        g_score[start] = 0
        f_score[start] = start.position.heuristic_to(end)
        heapq.heappush(priority_queue, (f_score[start], start))

        while priority_queue:
            _, current_pose = heapq.heappop(priority_queue)

            if current_pose.position == end:
                path = [current_pose.position]

                while current_pose in came_from:
                    current_pose = came_from[current_pose]
                    path.append(current_pose.position)

                return tuple(reversed(path))

            for neighbor_pose, cost in current_pose.get_neighbors_in_direction():
                if is_pose_blocked(neighbor_pose):
                    continue
                
                if is_edge_blocked(Edge(current_pose.position, neighbor_pose.position)):
                    continue                    

                tentative_g_score = g_score[current_pose] + cost

                if neighbor_pose not in g_score or tentative_g_score < g_score[neighbor_pose]:
                    came_from[neighbor_pose] = current_pose
                    g_score[neighbor_pose] = tentative_g_score
                    f_score[neighbor_pose] = tentative_g_score + neighbor_pose.position.heuristic_to(end)

                    heapq.heappush(priority_queue, (f_score[neighbor_pose], neighbor_pose))

        return ()  # No path found