from typing import Generator
from networkx import Graph
from models.geometry import Position, Pose
from collections import deque


class NetworkExplorer:
    """Finds a connected segment following traversal rules."""

    VALID_TURNS = {
        (-1, -1): [(-1, -1), (-1, 0), (0, -1)],
        (-1, 1): [(-1, 1), (-1, 0), (0, 1)],
        (1, -1): [(1, -1), (1, 0), (0, -1)],
        (1, 1): [(1, 1), (1, 0), (0, 1)],
        (-1, 0): [(-1, 0), (-1, -1), (-1, 1)],
        (1, 0): [(1, 0), (1, -1), (1, 1)],
        (0, -1): [(0, -1), (-1, -1), (1, -1)],
        (0, 1): [(0, 1), (-1, 1), (1, 1)],
        (0, 0): [
            (-1, -1), (-1, 0), (-1, 1),
            (1, -1), (1, 0), (1, 1),
            (0, -1), (0, 1)
        ]
    }

    def __init__(self, graph: Graph):
        self._graph = graph

    @staticmethod
    def get_valid_turns(direction: tuple[int, int]) -> list[tuple[int, int]]:
        return NetworkExplorer.VALID_TURNS[direction]
    
    def is_junction(self, pose: Pose) -> bool:
        if self._graph.degree(pose.position) > 2: return True
        opposite_direction = (-pose.direction[0], -pose.direction[1])
        for neighbor in self._graph.neighbors(pose.position):
            direction = pose.position.direction_to(neighbor)
            if direction not in self.get_valid_turns(pose.direction) and direction != opposite_direction:
                return True
            
        return False

    def get_connections_from_pose(self, pose: Pose) -> tuple[Pose]:
        connections = []
        for neighbor in self._graph.neighbors(pose.position):
            direction = pose.position.direction_to(neighbor)
            if direction in self.get_valid_turns(pose.direction):
                connections.append(Pose(neighbor, direction))
        return tuple(connections)

    def get_segment(self, edge: tuple[Position, Position], end_on_signal: bool = False, only_platforms: bool = False
    ) -> tuple[tuple[Position], tuple[tuple[Position, Position]]]:
        
        
        edges: set[tuple[Position, Position]] = set()
        nodes: set[Position] = set()
        stack: deque[Pose] = deque()

        a, b = edge
        if only_platforms and 'station' not in self._graph.edges[edge]: raise ValueError("No platform on the given edge")
        
        edges.add((a, b))
        
        a_has_signal = 'signal' in self._graph[a]
        b_has_signal = 'signal' in self._graph[b]
        pose_to_a = Pose.from_positions(b, a)
        pose_to_b = Pose.from_positions(a, b)
        is_a_junction = self.is_junction(pose_to_a)
        is_b_junction = self.is_junction(pose_to_b)



        if not (is_a_junction or (end_on_signal and a_has_signal)):
            stack.append(pose_to_a)

        if not (is_b_junction or (end_on_signal and b_has_signal)):
            stack.append(pose_to_b)

        while stack:
            pose = stack.popleft()
            connections = self.get_connections_from_pose(pose)
            
            nodes.add(pose.position)

            for neighbor, direction in connections:
                edge = (pose.position, neighbor)
                edges.add(edge)

                # skip conditions
                if neighbor in nodes or neighbor in {s.position for s in stack}:
                    continue
                
                pose_to_neighbor = Pose(neighbor, direction)
                if self.is_junction(pose_to_neighbor):
                    continue
                
                if end_on_signal and 'signal' in self._graph[neighbor]:
                    continue
                
                if only_platforms and 'station' not in self._graph.edges[edge]:
                    continue
                
                stack.append(pose_to_neighbor)

        return nodes, edges