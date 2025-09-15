import networkx as nx
from models import Point

class RailNetwork:
    def __init__(self):
        self.graph = nx.Graph()

    def get_nodes(self):
        """Return all nodes in the network."""
        return list(self.graph.nodes)

    def get_segments(self):
        """Return all segments in the network with their data."""
        return list(self.graph.edges(data=True))
    
    def add_node(self, pos: Point) -> Point:
        """Add a rail node (station/junction). Uses the Point itself as the node key."""
        self.graph.add_node(pos)
        return pos

    def add_segment(self, start: Point, end: Point, points: list[Point]) -> tuple:
        """Add a rail segment between two nodes, storing geometry as a tuple of points."""
        # Ensure nodes exist
        self.add_node(start)
        self.add_node(end)

        segment = tuple(points)
        self.graph.add_edge(start, end, geometry=segment)
        return segment

    def find_segment(self, start: Point, end: Point) -> tuple | None:
        """Return the segment (tuple of points) between two nodes, if it exists."""
        if self.graph.has_edge(start, end):
            return self.graph.edges[start, end]['geometry']
        return None

    def get_connections(self, node: Point) -> list[tuple]:
        """Return all connected segments for a node."""
        return [
            self.graph.edges[node, neighbor]['geometry']
            for neighbor in self.graph.neighbors(node)
        ]

    def find_cycles(self) -> list[list[Point]]:
        """Return all cycles in the network as lists of Points."""
        return list(nx.cycle_basis(self.graph))
