import heapq
from typing import Optional
from core.models.geometry.edge import Edge
from core.models.geometry.node import Node
from core.models.geometry.pose import Pose
from core.models.signal import Signal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem

class SignallingService:
    def __init__(self, railway: 'RailwaySystem'):
        self._railway = railway
        
    def lock_path(self, edges: list[Edge]) -> None:
        for edge in edges:
            self._railway.graph.set_edge_attr(edge, 'locked', True)
            self._railway.graph.set_node_attr(edge.a, 'locked', True)
            
    def unlock_path(self, edges: list[Edge]) -> None:
        for edge in edges:
            if self._railway.signals.has_signal_with_pose_at(Pose(edge.a, edge.a.direction_to(edge.b))):
                return
            self._railway.graph.set_edge_attr(edge, 'locked', False)
            self._railway.graph.set_node_attr(edge.a, 'locked', False)
    
    def cleared(self, edge: Edge):
        self._railway.graph.set_edge_attr(edge, 'locked', False)
        self._railway.graph.set_node_attr(edge.a, 'locked', False)
        
    def passed(self, node: Node):
        signal = self._railway.signals.get(node)
        if signal is not None:
            signal.passed()
            

        
    def is_edge_locked(self, edge: Edge) -> bool:
        return self._railway.graph.get_edge_attr(edge, 'locked') is True
    
    def is_node_locked(self, node: Node) -> bool:
        return self._railway.graph.get_node_attr(node, 'locked') is True

    def find_path(self, start: Pose, end: Pose) -> list[Pose] | None:
        if start.node == end.node:
            return None
        
        priority_queue: list[tuple[float, Pose]] = []
        came_from: dict[Pose, Pose] = {}
        g_score: dict[Pose, float] = {}

        g_score[start] = 0
        f_score = start.node.heuristic_to(end.node)
        heapq.heappush(priority_queue, (f_score, start))

        while priority_queue:
            _, current_pose = heapq.heappop(priority_queue)
            for neighbor_pose in self._railway.graph_service.get_turn_neighbors(current_pose):
                if neighbor_pose == end:
                    came_from[neighbor_pose] = current_pose
                    path = [neighbor_pose, current_pose]

                    while current_pose in came_from:
                        current_pose = came_from[current_pose]
                        path.append(current_pose)

                    return tuple(reversed(path))
                          
                if self.is_node_locked(neighbor_pose.node):
                    continue
                
                cost = 1.0 if current_pose.direction == neighbor_pose.direction else 1.01 # slight penalty for turning
                tentative_g_score = g_score[current_pose] + cost

                if neighbor_pose not in g_score or tentative_g_score < g_score[neighbor_pose]:
                    came_from[neighbor_pose] = current_pose
                    g_score[neighbor_pose] = tentative_g_score
                    f_score = tentative_g_score + neighbor_pose.node.heuristic_to(end.node)

                    heapq.heappush(priority_queue, (f_score, neighbor_pose))

        return None

    def disconnect_signal_at(self, a) -> None:
        return
        # TODO implement disconnecting signals
    
    def get_path_preview(self, start: Signal, end: Signal) -> list[Edge] | None:
        poses = self.find_path(start.pose, end.pose)
        if poses is None:
            return None
        edges = [Edge(poses[i].node, poses[i+1].node) for i in range(len(poses)-1)]
        return edges
            
    def connect_signals(self, from_signal: Signal, to_signal: Signal) -> None:
        poses = self.find_path(from_signal.pose, to_signal.pose)
        if poses is None:
            return None

        edges = [Edge(poses[i].node, poses[i+1].node) for i in range(len(poses)-1)]
        current_signal = from_signal
        current_signal_index = 0
        for i, pose in enumerate(poses[1:], start=1):
            if self._railway.signals.has_signal_with_pose_at(pose):
                signal = self._railway.signals.get(pose.node)
                current_signal.connect(edges[current_signal_index:i], signal)
                current_signal = signal
                current_signal_index = i
                
        self.lock_path(edges)

    def get_initial_path(self, start_pose: Pose) -> tuple[list[Edge], Optional[Signal]]:
        visited = set[Node]()
        pose = start_pose
        path = []
        while True:
            visited.add(pose.node)
            if self._railway.signals.has_signal_with_pose_at(pose):
                return path, self._railway.signals.get(pose.node)
                
            neighbors = self._railway.graph_service.get_turn_neighbors(pose)
            if len(neighbors) == 0:
                raise ValueError("Dead-end encountered. There should be a signal here.")
            
            # if multiple connections, pick the first one
            connection = neighbors[0]

            path.append(Edge(pose.node, connection.node))
            pose = connection