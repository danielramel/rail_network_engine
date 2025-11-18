import heapq
from typing import Optional
from core.models.geometry import Position, Edge
from core.models.signal import Signal
from core.models.geometry import Pose
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem

class SignallingService:
    def __init__(self, railway: 'RailwaySystem'):
        self._railway = railway
        
    def lock_path(self, edges: list[Edge]) -> None:
        for edge in edges:
            self._railway.graph.set_edge_attr(edge, 'locked', True)
            self._railway.graph.set_node_attr(edge.b, 'locked', True)
            
    def unlock_path(self, edges: list[Edge]):
        for edge in edges:
            self._railway.graph.set_edge_attr(edge, 'locked', False)
            self._railway.graph.set_node_attr(edge.b, 'locked', False)
            self._railway.graph.set_node_attr(edge.a, 'locked', False)
    
    def passed(self, edge: Edge):
        if self._railway.signals.has_signal_with_pose_at(Pose.from_edge(edge)):
            signal = self._railway.signals.get(edge.b)
            signal.passed()
        
        
    def is_edge_locked(self, edge: Edge) -> bool:
        return self._railway.graph.get_edge_attr(edge, 'locked') is True
    
    def is_node_locked(self, node: Position) -> bool:
        return self._railway.graph.get_node_attr(node, 'locked') is True

    def find_path(self, start: Pose, end: Pose) -> list[Pose] | None:
        if start.position == end.position:
            return None
        
        priority_queue: list[tuple[float, Pose]] = []
        came_from: dict[Pose, Pose] = {}
        g_score: dict[Pose, float] = {}

        g_score[start] = 0
        f_score = start.position.heuristic_to(end.position)
        heapq.heappush(priority_queue, (f_score, start))

        while priority_queue:
            _, current_pose = heapq.heappop(priority_queue)
            
            if current_pose == end:
                path = [current_pose]

                while current_pose in came_from:
                    current_pose = came_from[current_pose]
                    path.append(current_pose)

                return tuple(reversed(path))

            for neighbor_pose in current_pose.get_neighbors_in_direction():
                if not self._railway.graph.has_edge(Edge(current_pose.position, neighbor_pose.position)):
                    continue
                
                
                if self.is_node_locked(neighbor_pose.position):
                    continue
                
                cost = 1.0 if current_pose.direction == neighbor_pose.direction else 1.01 # slight penalty for turning
                tentative_g_score = g_score[current_pose] + cost

                if neighbor_pose not in g_score or tentative_g_score < g_score[neighbor_pose]:
                    came_from[neighbor_pose] = current_pose
                    g_score[neighbor_pose] = tentative_g_score
                    f_score = tentative_g_score + neighbor_pose.position.heuristic_to(end.position)

                    heapq.heappush(priority_queue, (f_score, neighbor_pose))

        return None

    def get_path_preview(self, start: Signal, end: Signal) -> list[Edge] | None:
        poses = self.find_path(start.pose, end.pose)
        if poses is None:
            return None
        edges = [Edge(poses[i].position, poses[i+1].position) for i in range(len(poses)-1)]
        return edges
            
    def connect_signals(self, from_signal: Signal, to_signal: Signal) -> None:
        poses = self.find_path(from_signal.pose, to_signal.pose)
        if poses is None:
            return None

        edges = [Edge(poses[i].position, poses[i+1].position) for i in range(len(poses)-1)]
        current_signal = from_signal
        current_signal_index = 0
        for i, pose in enumerate(poses[1:], start=1):
            if self._railway.signals.has_signal_with_pose_at(pose):
                signal = self._railway.signals.get(pose.position)
                current_signal.connect(edges[current_signal_index:i], signal)
                signal.subscribe_to_passage(lambda idx=current_signal_index, end=i: self.unlock_path(edges[idx:end]))
                current_signal = signal
                current_signal_index = i
                
        self.lock_path(edges)

    def get_initial_path(self, start_pose: Pose) -> tuple[list[Edge], Optional[Signal]]:
        visited = set[Position]()
        pose = start_pose
        path = []
        while True:
            visited.add(pose.position)
            if self._railway.signals.has_signal_with_pose_at(pose):
                return path, self._railway.signals.get(pose.position)
                
            neighbors = self._railway.graph_service.get_connections_from_pose(pose)
            if len(neighbors) != 1:
                raise ValueError("Branching or dead-end encountered. Cannot determine initial path.")
            
            connection = neighbors[0]

            path.append(Edge(pose.position, connection.position))
            pose = connection
            
    def occupy_segment(self, edge: Edge) -> None:
        path1, signal1 = self.get_initial_path(Pose.from_edge(edge))
        path2, signal2 = self.get_initial_path(Pose.from_edge(edge.reversed()))
        
        full_path = path1 + [edge] + path2
        self.lock_path(full_path)
        signal1.subscribe_to_passage(lambda: self.unlock_path(full_path))
        signal2.subscribe_to_passage(lambda: self.unlock_path(full_path))