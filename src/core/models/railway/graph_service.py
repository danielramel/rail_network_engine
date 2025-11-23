from core.config.settings import Config
from core.models.geometry.node import Node
from core.models.geometry.position import Position
from core.models.geometry.pose import Pose
from collections import deque
from core.models.geometry.edge import Edge
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem

class GraphService:
    def __init__(self, railway: 'RailwaySystem'):
        self._railway = railway

    def is_junction(self, node: Node) -> bool:
        if self._railway.graph.degree_at(node) > 2: return True
        if self._railway.graph.degree_at(node) < 2: return False

        neighbors = self._railway.graph.neighbors(node)
        inbound = neighbors[0].direction_to(node)
        outbound = node.direction_to(neighbors[1])
        return outbound not in inbound.get_valid_turns()
    
    def is_curve(self, node: Node) -> bool:
        if self._railway.graph.degree_at(node) != 2:
            return False
        
        neighbors = self._railway.graph.neighbors(node)
        return neighbors[0].direction_to(node) != node.direction_to(neighbors[1])
    
    @property
    def junctions(self) -> list[Node]:
        return [n for n in self._railway.graph.nodes if self.is_junction(n)]
    
    def get_valid_turn_neighbors_from_pose(self, pose: Pose) -> tuple[Pose]:
        connections = []
        graph_neighbors = self._railway.graph.neighbors(pose.node)
        for neighbor_pose in pose.get_connecting_poses():
            if neighbor_pose.node in graph_neighbors:
                connections.append(neighbor_pose)

        return tuple(connections)

    def remove_segment(self, edges: list[Edge]) -> None:      
        for edge in edges:
            self._railway.graph.remove_edge(edge)

        for node in list(self._railway.graph.nodes):
            if self._railway.graph.degree_at(node) == 0:
                self._railway.graph.remove_node(node)
            elif self._railway.graph.degree_at(node) == 1 and self._railway.signals.has_signal(node):
                self._railway.signals.set(Pose(node, (self._railway.graph.neighbors(node)[0]).direction_to(node)))

    def add_segment(self, nodes: list[Node], speed: int, length: int) -> None:
        for a, b in zip(nodes[:-1], nodes[1:]):
            self._railway.graph.add_edge(a, b, speed=speed, length=length)
            
    def add_tunnel_segment(self, nodes: list[Node], speed: int, length: int) -> None:
        for a, b in zip(nodes[:-1], nodes[1:]):
            self._railway.graph.add_edge(a, b, speed=speed, length=length, level=1)
            
    def is_station_blocked_by_node(self, station_pos: Node) -> bool:
        return any(node_pos.is_within_station_rect(station_pos) for node_pos in self._railway.graph.nodes)
    
    def get_closest_edge(self, world_pos: Position, tunnels: bool = False) -> Edge | None:
        min_edge = None
        min_distance = 1.0
        for edge in world_pos.get_grid_edges(tunnels=tunnels):
            if not self._railway.graph.has_edge(edge):
                continue
            distance = world_pos.distance_to_edge(edge)
            if distance < min_distance:
                min_distance = distance
                min_edge = edge

        return min_edge

    def get_segment(self, edge: Edge) -> tuple[frozenset[Node], frozenset[Edge]]:
        def is_node_blocked(node: Node) -> bool:
            if self.is_junction(node):
                return True
            if self._railway.graph.has_node_attr(node, 'signal') and self._railway.graph.degree_at(node) > 1:
                return True
            return False
        
        def is_edge_blocked(edge: Edge) -> bool:
            if is_initial_platform != self._railway.stations.is_edge_platform(edge):
                return True
            if self._railway.graph.get_edge_length(edge) != initial_track_length:
                return True
            if self._railway.graph.get_edge_speed(edge) != initial_track_speed:
                return True
            return False
        
        initial_track_length = self._railway.graph.get_edge_length(edge)
        initial_track_speed = self._railway.graph.get_edge_speed(edge)
        is_initial_platform = self._railway.stations.is_edge_platform(edge)
        
        edges: set[Edge] = set()
        nodes: set[Node] = set()
        stack: deque[Pose] = deque()
        edges.add(edge)
        
        a, b = edge
        pose_to_a = Pose.from_nodes(b, a)
        pose_to_b = Pose.from_nodes(a, b)

        if not is_node_blocked(a):
            stack.append(pose_to_a)

        if not is_node_blocked(b):
            stack.append(pose_to_b)

        while stack:
            pose = stack.popleft()
            connections = self.get_valid_turn_neighbors_from_pose(pose)
            
            nodes.add(pose.node)

            for neighbor, direction in connections:
                edge = Edge(pose.node, neighbor)
                if is_edge_blocked(edge):
                    continue
                
                edges.add(edge)
                
                if neighbor in nodes or neighbor in {s.node for s in stack}:
                    continue
                
                if is_node_blocked(neighbor):
                    continue
                
                stack.append(Pose(neighbor, direction))
                
        return frozenset(nodes), frozenset(edges)
    
    
    def calculate_platform_preview(self, edge: Edge, edge_count: int) -> tuple[bool, frozenset[Edge]]:
        def is_edge_blocked(edge: Edge) -> bool:
            if not self._railway.graph.has_edge(edge):
                return True
            if self._railway.graph.get_edge_length(edge) != Config.SHORT_SEGMENT_LENGTH:
                return True
            if self._railway.stations.is_edge_platform(edge):
                return True
            if edge.is_diagonal() and self._railway.graph.has_edge(Edge(Node(edge.a.x, edge.b.y), Node(edge.b.x, edge.a.y))):
                return True
            return False
            
        
        if is_edge_blocked(edge):
            return False, frozenset([edge])
        
        edges: set[Edge] = set()
        stack: deque[Pose] = deque()
        edges.add(edge)
        
        a, b = edge
        pose_to_a = Pose.from_nodes(b, a)
        pose_to_b = Pose.from_nodes(a, b)

        if not self.is_junction(a):
            stack.append(pose_to_a)

        if not self.is_junction(b):
            stack.append(pose_to_b)

        while stack:
            pose = stack.popleft()
            
            next_pose = pose.get_next_in_direction()
            edge = Edge(pose.node, next_pose.node)

            if is_edge_blocked(edge):
                continue
            
            edges.add(edge)

            if len(edges) >= edge_count:
                return True, frozenset(edges)
            
            if self.is_junction(next_pose.node):
                continue
            
            stack.append(next_pose)
                
        return False, frozenset(edges)