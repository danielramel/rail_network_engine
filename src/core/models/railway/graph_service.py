from core.config.settings import GRID_SIZE, PLATFORM_LENGTH
from core.models.geometry import Position, Pose
from collections import deque
from core.models.geometry.edge import Edge
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem

class GraphService:
    def __init__(self, railway: 'RailwaySystem'):
        self._railway = railway

    def is_junction(self, pos: Position) -> bool:
        if self._railway.graph.degree_at(pos) > 2: return True
        if self._railway.graph.degree_at(pos) < 2: return False

        neighbors = self._railway.graph.neighbors(pos)
        inbound = neighbors[0].direction_to(pos)
        outbound = pos.direction_to(neighbors[1])
        return outbound not in inbound.get_valid_turns()
    
    def is_curve(self, pos: Position) -> bool:
        if self._railway.graph.degree_at(pos) != 2:
            return False
        
        neighbors = self._railway.graph.neighbors(pos)
        return neighbors[0].direction_to(pos) != pos.direction_to(neighbors[1])
        
    
    @property
    def junctions(self) -> list[Position]:
        return [n for n in self._railway.graph.nodes if self.is_junction(n)]
    
    def get_connections_from_pose(self, pose: Pose) -> tuple[Pose]:
        connections = []
        for neighbor in self._railway.graph.neighbors(pose.position):
            direction = pose.position.direction_to(neighbor)
            
            if direction in pose.direction.get_valid_turns():
                connections.append(Pose(neighbor, direction))
        return tuple(connections)

    def remove_segment(self, edges: list[Edge]) -> None:      
        for edge in edges:
            self._railway.graph.remove_edge(edge)

        for node in list(self._railway.graph.nodes):
            if self._railway.graph.degree_at(node) == 0:
                self._railway.graph.remove_node(node)
            elif self._railway.graph.degree_at(node) == 1 and self._railway.signals.has_signal_at(node):
                self._railway.signals.set(Pose(node, (self._railway.graph.neighbors(node)[0]).direction_to(node)))

    def add_segment(self, points: list[Position], speed: int, length: int) -> None:
        for p in points:
            self._railway.graph.add_node(p) 
        for a, b in zip(points[:-1], points[1:]):
            self._railway.graph.add_edge(a, b, speed=speed, length=length)

    def get_segment(self, edge: Edge) -> tuple[frozenset[Position], frozenset[Edge]]:
        def is_node_blocked(pos: Position) -> bool:
            if self.is_junction(pos):
                return True
            if self._railway.graph.has_node_attr(pos, 'signal') and self._railway.graph.degree_at(pos) > 1:
                return True
            return False
        
        def is_edge_blocked(edge: Edge) -> bool:
            if is_initial_platform != self._railway.stations.is_edge_platform(edge):
                return True
            if self._railway.graph.get_edge_attr(edge, 'length') != initial_track_length:
                return True
            if self._railway.graph.get_edge_attr(edge, 'speed') != initial_track_speed:
                return True
            return False
        
        initial_track_length = self._railway.graph.get_edge_attr(edge, 'length')
        initial_track_speed = self._railway.graph.get_edge_attr(edge, 'speed')
        is_initial_platform = self._railway.stations.is_edge_platform(edge)
        
        edges: set[Edge] = set()
        nodes: set[Position] = set()
        stack: deque[Pose] = deque()
        edges.add(edge)
        
        a, b = edge
        pose_to_a = Pose.from_positions(b, a)
        pose_to_b = Pose.from_positions(a, b)

        if not is_node_blocked(a):
            stack.append(pose_to_a)

        if not is_node_blocked(b):
            stack.append(pose_to_b)

        while stack:
            pose = stack.popleft()
            connections = self.get_connections_from_pose(pose)
            
            nodes.add(pose.position)

            for neighbor, direction in connections:
                edge = Edge(pose.position, neighbor)
                if is_edge_blocked(edge):
                    continue
                
                edges.add(edge)
                
                if neighbor in nodes or neighbor in {s.position for s in stack}:
                    continue
                
                if is_node_blocked(neighbor):
                    continue
                
                stack.append(Pose(neighbor, direction))
                
        return frozenset(nodes), frozenset(edges)
    
    
    def calculate_platform_preview(self, edge: Edge) -> tuple[bool, frozenset[Edge]]:
        def is_edge_blocked(edge: Edge) -> bool:
            if not self._railway.graph.has_edge(edge):
                return True
            if self._railway.graph.get_edge_attr(edge, 'length') != 50:
                return True
            if self._railway.stations.is_edge_platform(edge):
                return True
            if edge.is_diagonal() and self._railway.graph.has_edge(Edge(Position(edge.a.x, edge.b.y), Position(edge.b.x, edge.a.y))):
                return True
            return False
            
        
        if is_edge_blocked(edge):
            return False, frozenset([edge])
        
        edges: set[Edge] = set()
        stack: deque[Pose] = deque()
        edges.add(edge)
        
        a, b = edge
        pose_to_a = Pose.from_positions(b, a)
        pose_to_b = Pose.from_positions(a, b)

        if not self.is_junction(a):
            stack.append(pose_to_a)

        if not self.is_junction(b):
            stack.append(pose_to_b)

        while stack:
            pose = stack.popleft()
            
            next_pose = pose.get_next_in_direction()
            edge = Edge(pose.position, next_pose.position)

            if is_edge_blocked(edge):
                continue
            
            edges.add(edge)

            if len(edges) >= PLATFORM_LENGTH:
                return True, frozenset(edges)
            
            if self.is_junction(next_pose.position):
                continue
            
            stack.append(next_pose)
                
        return False, frozenset(edges)    
    
    def get_closest_edge_on_grid(self, world_pos: Position, camera_scale) -> Edge | None:        
        min_edge = None
        min_distance = GRID_SIZE / 3 / camera_scale + 1
        for edge in world_pos.get_grid_edges():
            if not self._railway.graph.has_edge(edge):
                continue
            distance = world_pos.distance_to_edge(edge)
            if distance <= min_distance:
                min_distance = distance
                min_edge = edge

        return min_edge