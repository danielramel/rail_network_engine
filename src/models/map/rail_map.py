import networkx as nx
from collections import deque
from models.position import Position, PositionWithDirection


class RailMap:
    def __init__(self):
        self.graph = nx.Graph()
        self.stations : dict[Position, str] = {}

    def is_intersection(self, pos: Position) -> bool:
        """Check if the given position is an intersection (degree > 2)."""
        return pos in self.graph and self.graph.degree[pos] > 2
    
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
            
    def has_signal_at(self, pos: Position) -> bool:
        """Check if there is a signal at the given position."""
        return pos in self.graph and 'signal' in self.graph.nodes[pos]
        
    def add_signal_at(self, signal: PositionWithDirection):
        """Add a signal at the given position."""
        if signal.position not in self.graph:
            raise ValueError("No node at given position")
        if self.graph.degree[signal.position] > 2:
            raise ValueError("Cannot place signal at intersection")
        if self.has_signal_at(signal.position):
            raise ValueError("Signal already exists at this position")
        
        # Signals can be represented as a special attribute on the node
        self.graph.nodes[signal.position]['signal'] = signal.direction
        
    def get_signals(self) -> tuple[PositionWithDirection]:
        """Return all signals in the network."""
        return tuple(PositionWithDirection(position=node, direction=data['signal']) for node, data in self.graph.nodes(data=True) if 'signal' in data)

    def toggle_signal_at(self, pos: Position):
        if pos not in self.graph:
            raise ValueError("No node at given position")
        
        if not self.has_signal_at(pos):
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
        if not self.has_signal_at(pos):
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


    def get_segments_at(self, start: Position | tuple[Position, Position], endOnSignal: bool = False, onlyPlatforms: bool = False) -> tuple[set[Position], set[tuple[Position, Position]]]:
        """Return all nodes and edges in the segment containing the given position."""
        
        if isinstance(start, Position):
            if start not in self.graph:
                raise ValueError("No node at given position")
            if onlyPlatforms and not self.has_platform_at(start):
                raise ValueError("No platform at the given node")
            pos = start
            
        elif isinstance(start, tuple) and len(start) == 2:
            if start[0] not in self.graph or start[1] not in self.graph:
                raise ValueError("No node at one of the given positions")
            if not self.graph.has_edge(start[0], start[1]):
                raise ValueError("No edge between the given nodes")
            if onlyPlatforms and not self.is_edge_platform(start):
                raise ValueError("No platform on the given edge")

            start_node, end_node = start
            if self.is_intersection(start_node) and self.is_intersection(end_node):
                return set(), {start}
            if endOnSignal and self.has_signal_at(start_node) and self.has_signal_at(end_node):
                return set(), {start}

            if self.is_intersection(start_node)\
                or (endOnSignal and self.has_signal_at(start_node)):
                pos = end_node
            else:
                pos = start_node
            
        else:
            raise ValueError("start must be a Point or a tuple of two Points")


        nodes = set([pos])
        edges = set()
        stack = deque([pos])
        while stack:
            current = stack.popleft()
            for neighbor in self.graph.neighbors(current):
                edges.add((current, neighbor))
                if neighbor in stack or neighbor in nodes\
                    or (endOnSignal and (self.has_signal_at(neighbor)))\
                    or (onlyPlatforms and not self.is_edge_platform((current, neighbor))):
                        continue
                
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

    def has_platform_at(self, pos: Position) -> bool:
        """Check if there is a platform at the given position."""
        return pos in self.graph and 'platform' in self.graph.nodes[pos]
    
    def is_edge_platform(self, edge: tuple[Position, Position]) -> bool:
        """Check if there is a platform on the given edge."""
        return self.graph.has_edge(*edge) and 'platform' in self.graph.edges[edge]
    
    def add_platform(self, nodes: set[Position], edges: set[tuple[Position, Position]], station: Position):
        for node in nodes:
            if node not in self.graph:
                raise ValueError("No node at given position")
            self.graph.nodes[node]['platform'] = station
        
        for edge in edges:
            if not self.graph.has_edge(*edge):
                raise ValueError("No edge between the given nodes")
            self.graph.edges[edge]['platform'] = station
            
    def remove_platform_at(self, pos: Position | tuple[Position, Position]):
        """Remove the entire platform containing the given position."""
        nodes, edges = self.get_segments_at(pos, onlyPlatforms=True)

        for node in nodes:
            if 'platform' in self.graph.nodes[node]:
                del self.graph.nodes[node]['platform']

        for edge in edges:
            if 'platform' in self.graph.edges[edge]:
                del self.graph.edges[edge]['platform']
        
            
    def get_platforms(self) -> dict[tuple[Position, Position], Position]:
        """Return all platforms in the network."""
        return {edge: data['platform'] for edge, data in self.graph.edges.items() if 'platform' in data}