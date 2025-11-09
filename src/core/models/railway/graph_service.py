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
    
    @property
    def junctions(self) -> list[Position]:
        return [n for n in self._railway.graph.nodes if self.is_junction(n)]
    
    def get_connections_from_pose(self, pose: Pose, only_straight: bool = False) -> tuple[Pose]:
        connections = []
        for neighbor in self._railway.graph.neighbors(pose.position):
            direction = pose.position.direction_to(neighbor)
            if only_straight and direction != pose.direction:
                continue
            if direction in pose.direction.get_valid_turns():
                connections.append(Pose(neighbor, direction))
        return tuple(connections)

    def remove_segment(self, nodes: list[Position], edges: list[Edge]) -> None:      
        for edge in edges:
            self._railway.graph.remove_edge(edge)

        for node in list(self._railway.graph.nodes):
            if self._railway.graph.degree_at(node) == 0:
                self._railway.graph.remove_node(node)

    def add_segment(self, points: list[Position], speed: int, length: int) -> None:
        for p in points:
            self._railway.graph.add_node(p) 
        for a, b in zip(points[:-1], points[1:]):
            self._railway.graph.add_edge(a, b, speed=speed, length=length)

    def get_segment(self, edge: Edge, preferred_nr: int = None) -> tuple[frozenset[Position], frozenset[Edge]]:
        def should_stop_at_node(pos: Position) -> bool:
            if self.is_junction(pos):
                return True
            if not preferred_nr and self._railway.graph.has_node_attr(pos, 'signal') and self._railway.graph.degree_at(pos) > 1:
                return True
            
            return False
        
        def should_stop_at_edge(edge: Edge) -> bool:
            if is_initial_platform != self._railway.stations.is_edge_platform(edge):
                return True
            
            if preferred_nr:
                return False
            
            if self._railway.graph.get_edge_attr(edge, 'length') != initial_track_length:
                return True
            
            if self._railway.graph.get_edge_attr(edge, 'speed') != initial_track_speed:
                return True
            
            return False
        
        
        edges: set[Edge] = set()
        nodes: set[Position] = set()
        stack: deque[Pose] = deque()

        a, b = edge
        
        edges.add(edge)
        
        
        initial_track_length = self._railway.graph.get_edge_attr(edge, 'length')
        initial_track_speed = self._railway.graph.get_edge_attr(edge, 'speed')
        is_initial_platform = self._railway.stations.is_edge_platform(edge)

        pose_to_a = Pose.from_positions(b, a)
        pose_to_b = Pose.from_positions(a, b)

        if not should_stop_at_node(a):
            stack.append(pose_to_a)

        if not should_stop_at_node(b):
            stack.append(pose_to_b)

        while stack:
            pose = stack.popleft()
            connections = self.get_connections_from_pose(pose, only_straight=preferred_nr is not None)
            
            nodes.add(pose.position)

            for neighbor, direction in connections:
                edge = Edge(pose.position, neighbor)
                if should_stop_at_edge(edge):
                    continue
                
                edges.add(edge)

                if preferred_nr is not None and len(edges) >= preferred_nr:
                    return frozenset(nodes), frozenset(edges)
                
                if neighbor in nodes or neighbor in {s.position for s in stack}:
                    continue
                
                if should_stop_at_node(neighbor):
                    continue
                
                stack.append(Pose(neighbor, direction))
                
        return frozenset(nodes), frozenset(edges)
    
    
    def calculate_platform_preview(self, edge: Edge) -> tuple[bool, frozenset[Edge]]:
        _, edges = self.get_segment(edge, preferred_nr=PLATFORM_LENGTH)
        for edge in edges:
            # TODO check for platform corner cutting
            pass

        return len(edges) >= PLATFORM_LENGTH, edges