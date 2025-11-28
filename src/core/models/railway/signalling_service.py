import heapq
from core.models.geometry.edge import Edge
from core.models.geometry.node import Node
from core.models.geometry.pose import Pose
from core.models.signal import Signal
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem

class SignallingService:
    auto_signals: dict[Pose, Signal, tuple[Edge]] = {}
    def __init__(self, railway: 'RailwaySystem'):
        self._railway = railway
        
    def reset(self) -> None:
        self.auto_signals.clear()
        
    def lock_path(self, edges: list[Edge]) -> None:
        for edge in edges:
            self._railway.graph.set_edge_lock(edge, True)
            
    def release_path(self, edges: list[Edge]) -> None:
        if not edges:
            return
        for edge in edges:
            if self._railway.signals.has_with_pose(Pose.from_nodes(edge.a, edge.b).get_previous_in_direction()):
                return
            self._railway.graph.set_edge_lock(edge, False)
    
    def passed(self, edge: Edge):
        self._railway.graph.set_edge_lock(edge, False)
        signal = self._railway.signals.get(edge.b)
        if signal is not None and signal.direction == edge.direction:
            signal.passed()
        
    def reached(self, edge: Edge):
        signal = self._railway.signals.get(edge.a)
        if signal is not None:
            signal.reached()
            
    def lock_paths_under_trains(self) -> None:
        for train in self._railway.trains.all():
            for rail in train.get_occupied_rails():
                self._railway.graph.set_edge_lock(rail.edge, True)
                
    def unlock_all_paths(self) -> None:
        for edge in self._railway.graph.edges:
            self._railway.graph.set_edge_lock(edge, False)
        
    def is_edge_locked(self, edge: Edge) -> bool:
        return self._railway.graph.get_edge_attr(edge, 'locked') is True
    
    def is_node_locked(self, node: Node) -> bool:
        return any(self.is_edge_locked(Edge(node, neighbor)) for neighbor in self._railway.graph.neighbors(node))

    def drop_signal(self, signal: Signal) -> None:
        for edge in signal.path:
            self._railway.graph.set_edge_lock(edge, False)
        signal.drop()
        if signal.pose in self.auto_signals:
            del self.auto_signals[signal.pose]
    
    def get_path_preview(self, start: Signal, end: Signal) -> list[Edge]:
        while start.next_signal is not None:
            start = start.next_signal
        poses = self.find_path(start.pose, end.pose)
        if poses is None:
            return [], False
        edges = [Edge(poses[i].node, poses[i+1].node) for i in range(len(poses)-1)]
        return edges
            
    def connect_signals(self, from_signal: Signal, to_signal: Signal) -> bool:
        while from_signal.next_signal is not None:
            from_signal = from_signal.next_signal
        poses = self.find_path(from_signal.pose, to_signal.pose)
        if poses is None:
            return False
        
        if any(self.is_node_locked(pose.node) for pose in poses[1:-1]):
            return False
        
        edges = [Edge(poses[i].node, poses[i+1].node) for i in range(len(poses)-1)]
        current_signal = from_signal
        current_signal_index = 0
        for i, pose in enumerate(poses[1:], start=1):

            if self._railway.signals.has_with_pose(pose):
                signal = self._railway.signals.get(pose.node)
                current_signal.connect(edges[current_signal_index:i], signal)
                current_signal = signal
                current_signal_index = i
                
        self.lock_path(edges)
        
        return True
        
    def auto_connect_signals(self, from_signal: Signal, to_signal: Signal) -> str | None:
        poses = self.find_path(from_signal.pose, to_signal.pose, ignore_locks=True)
        if poses is None:
            return "No path found between signals."
        
        if any(self._railway.graph_service.is_junction(pose.node) for pose in poses):
            return "Cannot connect auto-signals through junctions."
        
        edges = [Edge(poses[i].node, poses[i+1].node) for i in range(len(poses)-1)]
        current_signal = from_signal
        current_signal_index = 0
        is_occupied = False
        for i, pose in enumerate(poses[1:], start=1):
            if self.is_node_locked(pose.node):
                is_occupied = True
            if self._railway.signals.has_with_pose(pose):
                signal = self._railway.signals.get(pose.node)
                if not is_occupied:
                    #only connect right now if the path is not locked
                    current_signal.connect(edges[current_signal_index:i], signal)
                self.auto_signals[current_signal.pose] = (signal, edges[current_signal_index:i])
                signal.passed_subscribe(self._create_auto_reconnect_callback(current_signal))
                current_signal = signal
                current_signal_index = i
                is_occupied = False
                
        self.lock_path(edges)
        
    def _create_auto_reconnect_callback(self, signal: Signal) -> Callable:
        def callback():
            if signal.pose in self.auto_signals:
                next_signal, path = self.auto_signals[signal.pose]
                signal.connect(path, next_signal)
                self.lock_path(path)
        return callback

    def set_initial_path(self, train_pose: Pose) -> tuple[list[Edge], Signal]:
        def get_initial_path(start_pose: Pose) -> tuple[list[Edge], Signal]:
            visited = set[Node]()
            pose = start_pose
            path = []
            while True:
                visited.add(pose.node)
                if self._railway.signals.has_with_pose(pose):
                    return path, self._railway.signals.get(pose.node)
                    
                neighbors = self._railway.graph_service.get_turn_neighbors(pose)
                if len(neighbors) == 0:
                    return path, None
                
                # if multiple connections, pick the first one
                connection = neighbors[0]
                if connection.node in visited:
                    raise ValueError("Loop encountered in railway graph.")

                edge = Edge(pose.node, connection.node)
                if self.is_edge_locked(edge):
                    return path, None
                path.append(edge)
                pose = connection
                
        path, signal = get_initial_path(train_pose)
        self.lock_path(path)
        return path, signal
    
    
            
            
    def find_path(self, start: Pose, end: Pose, ignore_locks: bool = False) -> list[Pose] | None:
        def is_node_blocked(node: Node) -> bool:
            if self._railway.graph.get_node_attr(node, "blocked"):
                return True
            
            if not ignore_locks and self.is_node_locked(node):
                return True
            return False
            
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
                          
                if is_node_blocked(neighbor_pose.node):
                    continue
                
                cost = 1.0 if current_pose.direction == neighbor_pose.direction else 1.01 # slight penalty for turning
                tentative_g_score = g_score[current_pose] + cost

                if neighbor_pose not in g_score or tentative_g_score < g_score[neighbor_pose]:
                    came_from[neighbor_pose] = current_pose
                    g_score[neighbor_pose] = tentative_g_score
                    f_score = tentative_g_score + neighbor_pose.node.heuristic_to(end.node)

                    heapq.heappush(priority_queue, (f_score, neighbor_pose))

        return None