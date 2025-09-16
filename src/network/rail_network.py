import networkx as nx
from network import Point, PointWithDirection
from utils import get_direction_between_points

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
        """Add a rail node. Uses the Point itself as the node key."""
        self.graph.add_node(pos)
        return pos

    def add_segment(self, start: Point, end: Point, points: list[Point]) -> tuple:
        for pt in points:
            self.add_node(pt)

        # Connect each neighboring pair of points
        for a, b in zip(points[:-1], points[1:]):
            self.graph.add_edge(a, b)
            
    def remove_node_at(self, pos: Point):
        """Remove a node at the given position."""
        if pos not in self.graph:
            raise ValueError("No node at given position")
        
        # Remove leaf nodes connected to this node
        for node in tuple(self.graph.neighbors(pos)):
            if self.graph.degree[node] == 1: 
                self.graph.remove_node(node)
                
        self.graph.remove_node(pos)
        
    def add_signal_at(self, signal: PointWithDirection):
        """Add a signal at the given position."""
        if signal.point not in self.graph:
            raise ValueError("No node at given position")
        if self.graph.degree[signal.point] > 2:
            raise ValueError("Cannot place signal at intersection")
        if 'signal' in self.graph.nodes[signal.point]:
            raise ValueError("Signal already exists at this position")
        
        # Signals can be represented as a special attribute on the node
        self.graph.nodes[signal.point]['signal'] = signal.direction
        
    def get_signals(self) -> list[PointWithDirection]:
        """Return all signals in the network."""
        signals = []
        for node, data in self.graph.nodes(data=True):
            if 'signal' in data:
                signals.append(PointWithDirection(point=node, direction=data['signal']))
        return signals
    
    def toggle_signal_at(self, pos: Point):
        if pos not in self.graph:
            raise ValueError("No node at given position")
        
        if 'signal' not in self.graph.nodes[pos]:
            raise ValueError("No signal at given position")
        
        current_direction = self.graph.nodes[pos]['signal']
        neighbors = tuple(self.graph.neighbors(pos))
        if get_direction_between_points(pos, neighbors[0]) == current_direction:
            self.graph.nodes[pos]['signal'] = get_direction_between_points(pos, neighbors[1])
        else:
            self.graph.nodes[pos]['signal'] = get_direction_between_points(pos, neighbors[0])
            
    def remove_signal_at(self, pos: Point):
        if pos not in self.graph:
            raise ValueError("No node at given position")
        if 'signal' not in self.graph.nodes[pos]:
            raise ValueError("No signal at given position")
        
        del self.graph.nodes[pos]['signal']

        
