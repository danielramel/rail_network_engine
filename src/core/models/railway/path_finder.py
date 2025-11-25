from core.models.geometry.direction import Direction
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
        
    def is_node_blocked(self, node: Node) -> bool:
        return self._railway.stations.is_within_any(node) or self._railway.graph_service.is_tunnel_entry(node)
    
    def find_grid_path(self, start: Pose, end: Node) -> tuple[Node] | None:        
        edge_blocked_cache: dict[Edge, bool] = {}
        def is_edge_blocked(edge: Edge) -> bool:
            def _func(edge: Edge) -> bool:
                if self._railway.graph.has_edge(edge.toggle_level()):
                    return True
                
                if self._railway.signals.has(edge.a):
                    signal = self._railway.signals.get(edge.a)
                    
                    if edge.direction.opposite() not in (signal.direction, signal.direction.opposite()):
                        return True
                    
                if self._railway.signals.has(edge.b):
                    signal = self._railway.signals.get(edge.b)
                    
                    if edge.direction not in (signal.direction, signal.direction.opposite()):
                        return True
                    
                    
                if self._railway.stations.is_node_platform(edge.a):
                    if edge.b not in self._railway.graph.neighbors(edge.a):
                        return True
                    
                if self._railway.stations.is_node_platform(edge.b):
                    if edge.a not in self._railway.graph.neighbors(edge.b):
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
        
        if self.is_node_blocked(start.node) or self.is_node_blocked(end):
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
                if self.is_node_blocked(neighbor_pose.node):
                    continue
                
                if is_edge_blocked(Edge(current_pose.node, neighbor_pose.node)):
                    continue                    
                
                cost = 1.0 if current_pose.direction == neighbor_pose.direction else 1.01 # slight penalty for turning
                tentative_g_score = g_score[current_pose] + cost

                if neighbor_pose not in g_score or tentative_g_score < g_score[neighbor_pose]:
                    came_from[neighbor_pose] = current_pose
                    g_score[neighbor_pose] = tentative_g_score
                    f_score[neighbor_pose] = tentative_g_score + neighbor_pose.node.heuristic_to(end)
                    if f_score[neighbor_pose] > f_score[start] + 20:
                        return None

                    heapq.heappush(priority_queue, (f_score[neighbor_pose], neighbor_pose))

        return None
    
    
    def find_tunnel_path(self, start: Pose, end: Pose) -> tuple[Node] | None:
        def _is_node_blocked(node: Node) -> bool:
            return self._railway.stations.is_within_any(node) or self._railway.graph.has_node(node)
        
        def is_edge_blocked(edge: Edge) -> bool:
            return self._railway.graph.has_edge(edge.surface_level())
        
        entrance = start.get_next_in_direction().tunnel_level()
        
        #length 1 tunnel
        if entrance.node.surface_level() == end.node and entrance.direction == end.direction:
            return tuple([start.node, end.node])
        
        exit = end.get_previous_in_direction().tunnel_level()
        
        if _is_node_blocked(entrance.node) or _is_node_blocked(exit.node):
            return None

        priority_queue: list[tuple[float, Pose]] = []
        came_from: dict[Pose, Pose] = {}
        g_score: dict[Pose, float] = {}
        f_score: dict[Pose, float] = {}

        g_score[entrance] = 0
        f_score[entrance] = entrance.node.heuristic_to(exit.node)
        heapq.heappush(priority_queue, (f_score[entrance], entrance))

        while priority_queue:
            _, current_pose = heapq.heappop(priority_queue)
                        
            if current_pose == exit:
                path = [end.node, current_pose.node]

                while current_pose in came_from:
                    current_pose = came_from[current_pose]
                    path.append(current_pose.node)
                    
                path.append(start.node)

                return tuple(reversed(path))
            
            for neighbor_pose in current_pose.get_connecting_poses():
                if _is_node_blocked(neighbor_pose.node):
                    continue
                edge = Edge(current_pose.node, neighbor_pose.node)
                if is_edge_blocked(edge):
                    continue                    
                
                cost = 1.0
                if current_pose.direction != neighbor_pose.direction:
                    cost += 0.1
                if self._railway.graph.has_edge(edge):
                    cost += 5.0  # heavy penalty for reusing existing track
                    
                tentative_g_score = g_score[current_pose] + cost

                if neighbor_pose not in g_score or tentative_g_score < g_score[neighbor_pose]:
                    came_from[neighbor_pose] = current_pose
                    g_score[neighbor_pose] = tentative_g_score
                    f_score[neighbor_pose] = tentative_g_score + neighbor_pose.node.heuristic_to(exit.node)
                    if f_score[neighbor_pose] > f_score[entrance] + 20:
                        return None  # Path too long

                    heapq.heappush(priority_queue, (f_score[neighbor_pose], neighbor_pose))

        return None