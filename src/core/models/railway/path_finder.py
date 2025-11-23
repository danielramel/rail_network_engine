from core.models.geometry.edge import Edge
from core.models.geometry.node import Node
from core.models.geometry.pose import Pose
import heapq

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem


class PathFinder:
    def __init__(self, railway: 'RailwaySystem'):
        self._railway = railway
        
    def find_grid_path(self, start: Pose, end: Node) -> tuple[Node]:
        pose_blocked_cache: dict[Pose, bool] = {}
        edge_blocked_cache: dict[Edge, bool] = {}
        def is_pose_blocked(pose: Pose) -> bool:
                
            if pose in pose_blocked_cache:
                return pose_blocked_cache[pose]
            
            blocked = self._railway.stations.is_within_any(pose.node)
            pose_blocked_cache[pose] = blocked
            return blocked
        
        def is_edge_blocked(edge: Edge) -> bool:
            def _func(edge: Edge) -> bool:
                if self._railway.graph.has_edge(edge.toggle_level()):
                    return True
                
                surface_a = Node(edge.a.x, edge.a.y, z=0)
                if self._railway.signals.has_signal(surface_a):
                    signal = self._railway.signals.get(surface_a)
                    
                    if edge.direction.opposite() not in (signal.direction, signal.direction.opposite()):
                        return True
                    
                surface_b = Node(edge.b.x, edge.b.y, z=0)
                if self._railway.signals.has_signal(surface_b):
                    signal = self._railway.signals.get(surface_b)
                    
                    if edge.direction not in (signal.direction, signal.direction.opposite()):
                        return True
                    
                    
                if self._railway.stations.is_platform_at(edge.a):
                    if self._railway.graph.degree_at(edge.a) == 2 and edge.b not in self._railway.graph.neighbors(edge.a):
                        return True
                    
                if self._railway.stations.is_platform_at(edge.b):
                    if self._railway.graph.degree_at(edge.b) == 2 and edge.a not in self._railway.graph.neighbors(edge.b):
                        return True
                
                # check for diagonal platform cutting
                if edge.is_diagonal() and self._railway.stations.is_edge_platform(Edge(Node(edge.a.x, edge.b.y), Node(edge.b.x, edge.a.y))):
                    return True
                return False
            
            if edge in edge_blocked_cache:
                return edge_blocked_cache[edge]
            blocked = _func(edge)
            edge_blocked_cache[edge] = blocked
            return blocked
        
        if end.z != start.node.z:
            start = Pose(Node(start.node.x, start.node.y, end.z), start.direction)
        
        if is_pose_blocked(start) or self._railway.stations.is_within_any(end):
            raise ValueError("Start or end node is blocked")

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
            
            for neighbor_pose in current_pose.get_connecting_poses():
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
                    if f_score[neighbor_pose] > f_score[start] + 10:
                        return ()  # Path too long

                    heapq.heappush(priority_queue, (f_score[neighbor_pose], neighbor_pose))

        return ()  # No path found