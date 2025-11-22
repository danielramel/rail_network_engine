from core.models.geometry.edge import Edge
from core.models.geometry.node import Node
from core.models.geometry.pose import Pose
import heapq

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem


class PathService:
    def __init__(self, railway: 'RailwaySystem'):
        self._railway = railway
        
    def find_grid_path(self, start: Pose, end: Node) -> tuple[Node]:
        def is_pose_blocked(pose: Pose) -> bool:
            if self._railway.stations.is_within_any(pose.node):
                return True
            
            if self._railway.signals.has_signal_at(pose.node):
                signal = self._railway.signals.get(pose.node)
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

            if edge.is_diagonal() and self._railway.stations.is_edge_platform(Edge(Node(edge.a.x, edge.b.y), Node(edge.b.x, edge.a.y))):
                return True
            return False
        
        if is_pose_blocked(start) or self._railway.stations.is_within_any(end):
            raise ValueError("Start or end node is blocked")

        if start.node == end:
            return (start.node,)

        priority_queue: list[tuple[float, Pose]] = []
        came_from: dict[Pose, Pose] = {}
        g_score: dict[Pose, float] = {}
        f_score: dict[Pose, float] = {}

        g_score[start] = 0
        f_score[start] = start.node.heuristic_to(end)
        heapq.heappush(priority_queue, (f_score[start], start))

        while priority_queue:
            _, current_pose = heapq.heappop(priority_queue)

            if current_pose.node == end:
                path = [current_pose.node]

                while current_pose in came_from:
                    current_pose = came_from[current_pose]
                    path.append(current_pose.node)

                return tuple(reversed(path))
            
            if self._railway.signals.has_signal_at(current_pose.node):
                neighbors = [current_pose.get_next_in_direction()]
            else:
                neighbors = current_pose.get_valid_turns()
                

            for neighbor_pose in neighbors:
                if is_pose_blocked(neighbor_pose):
                    continue
                
                if is_edge_blocked(Edge(current_pose.node, neighbor_pose.node)):
                    continue                    
                
                cost = 1.0 if current_pose.direction == neighbor_pose.direction else 1.01 # slight penalty for turning
                tentative_g_score = g_score[current_pose] + cost

                if neighbor_pose not in g_score or tentative_g_score < g_score[neighbor_pose]:
                    came_from[neighbor_pose] = current_pose
                    g_score[neighbor_pose] = tentative_g_score
                    f_score[neighbor_pose] = tentative_g_score + neighbor_pose.node.heuristic_to(end)

                    heapq.heappush(priority_queue, (f_score[neighbor_pose], neighbor_pose))

        return ()  # No path found