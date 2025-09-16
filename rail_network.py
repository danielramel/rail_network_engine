import networkx as nx
from models import Point

class RailNetwork:
    def __init__(self):
        self.graph = nx.Graph()

    def get_intersections(self):
        """Return all intersection nodes (degree > 2) in the network."""
        return [node for node in self.graph.nodes if self.graph.degree[node] != 2]

    def get_edges(self):
        """Return all edges in the network as tuples of Points."""
        return list(self.graph.edges)
    
    def add_node(self, pos: Point) -> Point:
        """Add a rail node (station/junction). Uses the Point itself as the node key."""
        self.graph.add_node(pos)
        return pos

    def add_segment(self, start: Point, end: Point, points: list[Point]) -> tuple:
        for pt in points:
            self.add_node(pt)

        # Connect each neighboring pair of points
        for a, b in zip(points[:-1], points[1:]):
            self.graph.add_edge(a, b)
            
    def remove_node_at(self, pos: tuple[int, int]):
        """Remove a node at the given position (if exists)."""
        point = Point(*pos)
        if point not in self.graph:
            raise ValueError("No node at given position")
        
        # Remove leaf nodes connected to this node
        for node in tuple(self.graph.neighbors(point)):
            if self.graph.degree[node] == 1: 
                self.graph.remove_node(node)
                
        self.graph.remove_node(point)
