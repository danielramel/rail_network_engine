from tracemalloc import start
import networkx as nx
from collections import deque
from models.geometry import Point, PointWithDirection
from utils import get_direction_between_points


class RailMap:
    def __init__(self):
        self.graph = nx.Graph()
        self.stations = {}

    def get_intersections(self):
        """Return all intersection nodes (degree > 2) in the network."""
        return [node for node in self.graph.nodes if self.graph.degree[node] > 2]

    def get_edges(self):
        """Return all edges in the network as tuples of Points."""
        return list(self.graph.edges)
    
    def add_node(self, pos: Point) -> Point:
        """Add a rail node. Uses the Point itself as the node key."""
        self.graph.add_node(pos)
        return pos

    def add_segment(self, points: list[Point]) -> tuple:
        for pt in points:
            self.add_node(pt)

        # Connect each neighboring pair of points
        for a, b in zip(points[:-1], points[1:]):
            self.graph.add_edge(a, b)
        
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
        
    def get_signals(self) -> tuple[PointWithDirection]:
        """Return all signals in the network."""
        return tuple(PointWithDirection(point=node, direction=data['signal']) for node, data in self.graph.nodes(data=True) if 'signal' in data)

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
        
    def add_station_at(self, pos: Point, name: str):
        if pos in self.stations:
            raise ValueError("Station already exists at this position")
        if name in self.stations.values():
            raise ValueError("Station name must be unique")
        
        self.stations[pos] = name
        
    def remove_station(self, pos: Point):
        if pos not in self.stations:
            raise ValueError("No station at given position")
        
        del self.stations[pos]
        
    
    def get_segments_at(self, start: Point | tuple[Point, Point]) -> tuple[set[Point], set[tuple[Point, Point]]]:
        """Return all nodes and edges in the segment containing the given position."""
        if isinstance(start, Point):
            if start not in self.graph:
                raise ValueError("No node at given position")
        
            pos = start
        elif isinstance(start, tuple) and len(start) == 2:
            if start[0] not in self.graph or start[1] not in self.graph:
                raise ValueError("No node at one of the given positions")
            if not self.graph.has_edge(start[0], start[1]):
                raise ValueError("No edge between the given nodes")
            
            if self.graph.degree[start[0]] > 2 and self.graph.degree[start[1]] > 2:
                return set(), {start}

            pos = start[1] if self.graph.degree[start[0]] > 2 else start[0]
            
        else:
            raise ValueError("start must be a Point or a tuple of two Points")


        nodes = set([pos])
        edges = set()
        stack = deque([pos])
        while stack:
            current = stack.popleft()
            for neighbor in self.graph.neighbors(current):
                edges.add((current, neighbor))
                if neighbor not in stack and neighbor not in nodes:
                    if self.graph.degree[neighbor] == 1:
                        nodes.add(neighbor)
                    elif self.graph.degree[neighbor] == 2:
                        nodes.add(neighbor)
                        stack.append(neighbor)
                    # If all neighbors are in the current segment, add the neighbor
                    elif all(nbh in nodes for nbh in self.graph.neighbors(neighbor)):
                        nodes.add(neighbor)

        return nodes, edges
    
    
    def remove_segment_at(self, pos: Point | tuple[Point, Point]):
        """Remove the entire segment containing the given position."""
        nodes, edges = self.get_segments_at(pos)
        
        if not nodes and len(edges) == 1:
            # Special case: single edge between two intersections
            self.graph.remove_edge(*next(iter(edges)))
            return
        
        for node in nodes:
            self.graph.remove_node(node)