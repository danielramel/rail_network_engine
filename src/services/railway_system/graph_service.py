from typing import Optional
from config.settings import GRID_SIZE, PLATFORM_LENGTH
from models.geometry import Position, Pose
from collections import deque
from models.geometry.edge import Edge
from models.graph_adapter import GraphAdapter

class GraphService:
    def __init__(self, graph: GraphAdapter):
        self._graph = graph

    def is_junction(self, pos: Position) -> bool:
        if self._graph.degree_at(pos) > 2: return True
        if self._graph.degree_at(pos) < 2: return False

        neighbors = self._graph.neighbors(pos)
        inbound = neighbors[0].direction_to(pos)
        outbound = pos.direction_to(neighbors[1])
        return outbound not in inbound.get_valid_turns()
    
    @property
    def junctions(self) -> list[Position]:
        return [n for n in self._graph.nodes if self.is_junction(n)]
    
    def get_connections_from_pose(self, pose: Pose, only_straight: bool = False) -> tuple[Pose]:
        connections = []
        for neighbor in self._graph.neighbors(pose.position):
            direction = pose.position.direction_to(neighbor)
            if only_straight and direction != pose.direction:
                continue
            if direction in pose.direction.get_valid_turns():
                connections.append(Pose(neighbor, direction))
        return tuple(connections)
    
    def remove_segment_at(self, edge: Edge) -> None:
        nodes, edges = self.get_segment(edge)
        if len(nodes) == 0 and len(edges) == 1:
            # Special case: single edge between two intersections
            self._graph.remove_edge(next(iter(edges)))
            return
        
        for n in nodes:
            self._graph.remove_node(n)

    def add_segment(self, points: list[Position], speed: int, length: int) -> None:
        for p in points:
            self._graph.add_node(p)
        for a, b in zip(points[:-1], points[1:]):
            self._graph.add_edge(a, b, speed=speed, length=length)
            
    def get_platform_preview(self, edge: Edge) -> tuple[frozenset[Position], frozenset[Edge]]:
        return self.get_segment(edge, only_platforms=True, only_straight=True, max_nr=5)

    def get_segment(self, edge: Edge, end_on_signal: bool = False, only_platforms: bool = False, only_straight: bool = False, max_nr: Optional[int] = None
    ) -> tuple[frozenset[Position], frozenset[Edge]]:
        
        edges: set[Edge] = set()
        nodes: set[Position] = set()
        stack: deque[Pose] = deque()

        a, b = edge
        if max_nr is not None and not only_straight: raise ValueError("max_nr can only be used with only_straight=True")
        
        edges.add(edge)
        
        a_has_signal = self._graph.has_node_attr(a, 'signal')
        b_has_signal = self._graph.has_node_attr(b, 'signal')
        is_a_junction = self.is_junction(a)
        is_b_junction = self.is_junction(b)
        pose_to_a = Pose.from_positions(b, a)
        pose_to_b = Pose.from_positions(a, b)


        if not (is_a_junction or (end_on_signal and a_has_signal)):
            stack.append(pose_to_a)

        if not (is_b_junction or (end_on_signal and b_has_signal)):
            stack.append(pose_to_b)

        while stack:
            pose = stack.popleft()
            connections = self.get_connections_from_pose(pose, only_straight=only_straight)
            
            nodes.add(pose.position)

            for neighbor, direction in connections:
                edge = Edge(pose.position, neighbor)

                if self._graph.has_edge_attr(edge, 'station') and not only_platforms:
                    nodes.remove(pose.position) # ezt nézd át, miért csak itt van
                    continue

                if only_platforms and not self._graph.has_edge_attr(edge, 'station'):
                    continue
                
                edges.add(edge)

                if max_nr is not None and only_straight and edge.length * len(edges) >= max_nr * GRID_SIZE:
                    return frozenset(nodes), frozenset(edges)
                
                # skip conditions
                if neighbor in nodes or neighbor in {s.position for s in stack}:
                    continue
                
                if self.is_junction(neighbor):
                    continue

                if end_on_signal and self._graph.has_node_attr(neighbor, 'signal'):
                    continue
                
                stack.append(Pose(neighbor, direction))
        
        return frozenset(nodes), frozenset(edges)
    
    
    def calculate_platform_preview(self, edge: Edge) -> tuple[bool, frozenset[Edge]]:
        _, edges = self.get_segment(edge, only_straight=True, max_nr=PLATFORM_LENGTH)
        for edge in edges:
            # TODO check for platform corner cutting
            pass

        edge = next(iter(edges))
        return edge.length * len(edges) >= PLATFORM_LENGTH * GRID_SIZE, edges