import heapq
from typing import Optional
from core.models.geometry import Position, Edge
from core.models.signal import Signal
from core.models.geometry import Pose
from typing import TYPE_CHECKING

from core.models.train import Train
if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem

class SignallingService:
    def __init__(self, railway: 'RailwaySystem'):
        self._railway = railway
        
    # def free_edge(self, edge: Edge) -> None:
    #     self._railway.graph.set_edge_attr(edge, 'locked', False)
    #     self._railway.graph.set_node_attr(edge.b, 'locked', False)
    #     if self._railway.signals.has_signal_with_pose_at(Pose.from_positions(*edge)):
    #         signal = self._railway.signals.get(edge.b)
    #         signal.disconnect()
        
    def lock_path(self, edges: list[Edge]):
        for edge in edges:
            self._railway.graph.set_edge_attr(edge, 'locked', True)
            self._railway.graph.set_node_attr(edge.b, 'locked', True) #dont look the very first node
    
    def free(self, edges: list[Edge]):
        for edge in edges:
            self._railway.graph.set_edge_attr(edge, 'locked', False)
            self._railway.graph.remove_node_attr(edge.a, 'locked')                
            self._railway.graph.remove_node_attr(edge.b, 'locked')
            
            if self._railway.signals.has_signal_with_pose_at(Pose.from_edge(edge)):
                signal = self._railway.signals.get(edge.b)
                signal.disconnect()
            
        
    def is_edge_locked(self, edge: Edge) -> bool:
        return self._railway.graph.get_edge_attr(edge, 'locked') is True
    
    def is_node_locked(self, node: Position) -> bool:
        return self._railway.graph.get_node_attr(node, 'locked') is True
    
    def disconnect_signal_at(self, position: Position) -> None:
        signal = self._railway.signals.get(position)
        for edge in signal.path:
            self._railway.graph.set_edge_attr(edge, 'locked', False)
            self._railway.graph.remove_node_attr(edge.b, 'locked') # the first node is never locked, so we can always use b
            
        signal.disconnect()

    def find_path(self, start: Pose, end: Pose) -> list[Pose] | None:
        priority_queue: list[tuple[float, float, Pose]] = []
        came_from: dict[Pose, Pose] = {}
        g_score: dict[Pose, float] = {}
        f_score: dict[Pose, float] = {}

        g_score[start] = 0
        f_score[start] = start.position.heuristic_to(end.position)
        heapq.heappush(priority_queue, (f_score[start], g_score[start], start))

        while priority_queue:
            current_f, current_g, current_pose = heapq.heappop(priority_queue)

            if current_pose in g_score and current_g > g_score[current_pose]:
                continue

            if current_pose == end:
                path = [current_pose]

                while current_pose in came_from:
                    current_pose = came_from[current_pose]
                    path.append(current_pose)

                return tuple(reversed(path))

            for neighbor_pose, cost in current_pose.get_neighbors_in_direction():
                if not self._railway.graph.has_edge(Edge(current_pose.position, neighbor_pose.position)):
                    continue
                
                if self._railway.graph.get_node_attr(neighbor_pose.position, 'locked'):
                    continue
                
                tentative_g_score = g_score[current_pose] + cost

                if neighbor_pose not in g_score or tentative_g_score < g_score[neighbor_pose]:
                    came_from[neighbor_pose] = current_pose
                    g_score[neighbor_pose] = tentative_g_score
                    f_score[neighbor_pose] = tentative_g_score + neighbor_pose.position.heuristic_to(end.position)

                    heapq.heappush(priority_queue, (f_score[neighbor_pose], g_score[neighbor_pose], neighbor_pose))

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
                current_signal = signal
                current_signal_index = i
                
        for edge in edges:
            self._railway.graph.set_edge_attr(edge, 'locked', True)
        for pose in poses[1:]:
            self._railway.graph.set_node_attr(pose.position, 'locked', True)

    def set_inital_train_path(self, start_pose: Pose) -> tuple[list[Edge], Optional[Signal]]:
        visited = set[Position]()
        pose = start_pose
        path = []
        while True:
            visited.add(pose.position)
            if self._railway.signals.has_signal_with_pose_at(pose):
                signal = self._railway.signals.get(pose.position)
                self.lock_path(path)
                while signal.next_signal is not None:
                    path.extend(signal.path)
                    signal = signal.next_signal
                return path, signal
                
            neighbors = self._railway.graph_service.get_connections_from_pose(pose)
            if len(neighbors) == 0:
                raise RuntimeError("No signal found.")
            
            if len(neighbors) > 1:
                raise NotImplementedError("Branching paths are not supported in initial path generation.")
            
            connection = neighbors[0]
            if connection.position in visited:
                raise RuntimeError("No signal found.")

            path.append(Edge(pose.position, connection.position))
            pose = connection