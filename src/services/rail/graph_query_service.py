import networkx as nx
from config.settings import GRID_SIZE
from models.geometry import Position, Pose
from collections import deque

from models.geometry.edge import Edge


class GraphService:
    def __init__(self, graph: nx.Graph):
        self._graph = graph
        
    @property
    def nodes(self) -> set[Position]:
        return self._graph.nodes
    
    @property
    def edges(self) -> frozenset[Edge]:
        return frozenset((Edge(*edge) for edge in self._graph.edges))
    
    def has_node_at(self, pos: Position) -> bool:
        return pos in self._graph.nodes
    
    def degree_at(self, pos: Position) -> int:
        return self._graph.degree[pos]
    
    def has_edge(self, edge: Edge) -> bool:
        return self._graph.has_edge(*edge)
    
    def edges_with_data(self, key=None) -> dict[Edge, dict]:
        if key:
            return {Edge(*edge): data for *edge, data in self._graph.edges.data(key)}
        
        return {Edge(*edge): data for *edge, data in self._graph.edges.data()}
    
    def is_junction(self, pos: Position) -> bool:
        if self._graph.degree[pos] > 2: return True
        if self._graph.degree[pos] < 2: return False
        
        neighbors = tuple(self._graph.neighbors(pos))
        inbound = neighbors[0].direction_to(pos)
        outbound = pos.direction_to(neighbors[1])
        return tuple(outbound) not in Pose.get_valid_turns(inbound)
    
    @property
    def junctions(self) -> list[Position]:
        return [n for n in self._graph.nodes if self.is_junction(n)]
    

    def get_connections_from_pose(self, pose: Pose, only_straight: bool = False) -> tuple[Pose]:
        connections = []
        for neighbor in self._graph.neighbors(pose.position):
            direction = pose.position.direction_to(neighbor)
            if only_straight and direction != pose.direction:
                continue
            if direction in Pose.get_valid_turns(pose.direction):
                connections.append(Pose(neighbor, direction))
        return tuple(connections)
    
    def remove_segment_at(self, edge: Edge) -> None:
        nodes, edges = self.get_segment(edge)
        if len(nodes) == 0 and len(edges) == 1:
            # Special case: single edge between two intersections
            self._graph.remove_edge(*next(iter(edges)))
            return
        
        for n in nodes:
            self._graph.remove_node(n)
            
    def add_segment(self, points: list[Position], speed: int) -> None:
        for p in points:
            self._graph.add_node(p)
        for a, b in zip(points[:-1], points[1:]):
            self._graph.add_edge(a, b, speed=speed)

    def get_segment(
        self,
        edge: Edge,
        end_on_signal: bool = False,
        only_platforms: bool = False,
        only_straight: bool = False,
        max_nr: int | None = None
    ) -> tuple[frozenset[Position], frozenset[Edge]]:
        
        edges: set[Edge] = set()
        nodes: set[Position] = set()
        stack: deque[Pose] = deque()

        a, b = edge
        if only_platforms and 'station' not in self._graph.edges[edge]: raise ValueError("No platform on the given edge")
        if max_nr is not None and not only_straight: raise ValueError("max_nr can only be used with only_straight=True")
        
        edges.add(edge)
        
        a_has_signal = 'signal' in self._graph[a]
        b_has_signal = 'signal' in self._graph[b]
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
                                
                if 'station' in self._graph.edges[edge] and not only_platforms:
                    nodes.remove(pose.position) # ezt nézd át, miért csak itt van
                    continue
                
                if only_platforms and 'station' not in self._graph.edges[edge]:
                    continue
                
                edges.add(edge)

                if max_nr is not None and only_straight and edge.length * len(edges) >= max_nr * GRID_SIZE:
                    return frozenset(nodes), frozenset(edges)
                
                # skip conditions
                if neighbor in nodes or neighbor in {s.position for s in stack}:
                    continue
                
                if self.is_junction(neighbor):
                    continue
                
                if end_on_signal and 'signal' in self._graph[neighbor]:
                    continue
                
                stack.append(Pose(neighbor, direction))
        
        return frozenset(nodes), frozenset(edges)
    
    
    def to_dict(self) -> dict:
        graph_data = nx.node_link_data(self._graph)
        
        # convert Position objects in node attributes to dicts
        for node in graph_data['nodes']:
            node['id'] = node['id'].to_dict()
            
        for link in graph_data['links']:
            link["source"] = link["source"].to_dict()
            link["target"] = link["target"].to_dict()
            if 'station' in link:
                link['station'] = link['station'].id
        
        return graph_data
    
    

    def from_dict(self, graph_data: dict) -> None:
        for node in graph_data['nodes']:
            node['id'] = Position.from_dict(node['id'])
            if 'signal' in node:
                node['signal'] = tuple(node['signal'])
            
        for link in graph_data['links']:
            for key in ('source', 'target'):
                link[key] = Position.from_dict(link[key])

        temp_graph = nx.node_link_graph(graph_data)
        
        self._graph.clear()
        self._graph.add_nodes_from(temp_graph.nodes(data=True))
        self._graph.add_edges_from(temp_graph.edges(data=True))