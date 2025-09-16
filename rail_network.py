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

