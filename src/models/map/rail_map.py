from tracemalloc import start
import networkx as nx
from collections import deque
from models.position import Position, PositionWithDirection


class RailMap:
    def __init__(self):
        self.graph = nx.Graph()
        self.stations : dict[Position, str] = {}

    def get_intersections(self):
        """Return all intersection nodes (degree > 2) in the network."""
        return [node for node in self.graph.nodes if self.graph.degree[node] > 2]

    def get_edges(self):
        """Return all edges in the network as tuples of Points."""
        return list(self.graph.edges)
    
    def add_node(self, pos: Position) -> Position:
        """Add a rail node. Uses the Point itself as the node key."""
        self.graph.add_node(pos)
        return pos

    def add_segment(self, points: list[Position]) -> tuple:
        for pt in points:
            self.add_node(pt)

        # Connect each neighboring pair of points
        for a, b in zip(points[:-1], points[1:]):
            self.graph.add_edge(a, b)
        
    def add_signal_at(self, signal: PositionWithDirection):
        """Add a signal at the given position."""
        if signal.position not in self.graph:
            raise ValueError("No node at given position")
        if self.graph.degree[signal.position] > 2:
            raise ValueError("Cannot place signal at intersection")
        if 'signal' in self.graph.nodes[signal.position]:
            raise ValueError("Signal already exists at this position")
        
        # Signals can be represented as a special attribute on the node
        self.graph.nodes[signal.position]['signal'] = signal.direction
        
    def get_signals(self) -> tuple[PositionWithDirection]:
        """Return all signals in the network."""
        return tuple(PositionWithDirection(position=node, direction=data['signal']) for node, data in self.graph.nodes(data=True) if 'signal' in data)

    def toggle_signal_at(self, pos: Position):
        if pos not in self.graph:
            raise ValueError("No node at given position")
        
        if 'signal' not in self.graph.nodes[pos]:
            raise ValueError("No signal at given position")
        
        current_direction = self.graph.nodes[pos]['signal']
        neighbors = tuple(self.graph.neighbors(pos))
        if pos.direction_to(neighbors[0]) == current_direction:
            self.graph.nodes[pos]['signal'] = pos.direction_to(neighbors[1])
        else:
            self.graph.nodes[pos]['signal'] = pos.direction_to(neighbors[0])

    def remove_signal_at(self, pos: Position):
        if pos not in self.graph:
            raise ValueError("No node at given position")
        if 'signal' not in self.graph.nodes[pos]:
            raise ValueError("No signal at given position")
        
        del self.graph.nodes[pos]['signal']
        
    def add_station_at(self, pos: Position, name: str):
        if pos in self.stations:
            raise ValueError("Station already exists at this position")
        if name in self.stations.values():
            raise ValueError("Station name must be unique")
        
        self.stations[pos] = name
        
    def remove_station(self, pos: Position):
        if pos not in self.stations:
            raise ValueError("No station at given position")
        
        del self.stations[pos]
        
    
    def get_segments_at(self, start: Position | tuple[Position, Position], endOnSignal: bool = False) -> tuple[set[Position], set[tuple[Position, Position]]]:
        """Return all nodes and edges in the segment containing the given position."""
        def has_signal(node):
            if not endOnSignal:
                return False
            return 'signal' in self.graph.nodes[node]

        def is_intersection(node):
            return self.graph.degree[node] > 2
        
        if isinstance(start, Position):
            if start not in self.graph:
                raise ValueError("No node at given position")
        
            pos = start
        elif isinstance(start, tuple) and len(start) == 2:
            if start[0] not in self.graph or start[1] not in self.graph:
                raise ValueError("No node at one of the given positions")
            if not self.graph.has_edge(start[0], start[1]):
                raise ValueError("No edge between the given nodes")

            start_node, end_node = start
            if (is_intersection(start_node) or has_signal(start_node)) and (is_intersection(end_node) or has_signal(end_node)):
                return set(), {start}

            pos = end_node if (is_intersection(start_node) or has_signal(start_node)) else start_node
            
        else:
            raise ValueError("start must be a Point or a tuple of two Points")


        nodes = set([pos])
        edges = set()
        stack = deque([pos])
        while stack:
            current = stack.popleft()
            for neighbor in self.graph.neighbors(current):
                edges.add((current, neighbor))
                if neighbor not in stack and neighbor not in nodes and not has_signal(neighbor):
                    if self.graph.degree[neighbor] == 1:
                        nodes.add(neighbor)
                    elif self.graph.degree[neighbor] == 2:
                        nodes.add(neighbor)
                        stack.append(neighbor)
                    # If all neighbors are in the current segment, add the neighbor
                    elif all(nbh in nodes for nbh in self.graph.neighbors(neighbor)):
                        nodes.add(neighbor)

        return nodes, edges
    
    
    def remove_segment_at(self, pos: Position | tuple[Position, Position]):
        """Remove the entire segment containing the given position."""
        nodes, edges = self.get_segments_at(pos)
        
        if not nodes and len(edges) == 1:
            # Special case: single edge between two intersections
            self.graph.remove_edge(*next(iter(edges)))
            return
        
        for node in nodes:
            self.graph.remove_node(node)
            
    def add_platform_on_edges(self, edges: set[tuple[Position, Position]], station: Position):
        for edge in edges:
            if not self.graph.has_edge(*edge):
                raise ValueError("No edge between the given nodes")
            self.graph.edges[edge]['platform'] = station