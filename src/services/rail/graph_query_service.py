from networkx import Graph
from models.geometry import Position, Pose
from collections import deque


class GraphQueryService:
    def __init__(self, graph: Graph):
        self._graph = graph
    
    def is_junction(self, pos: Position) -> bool:
        if self._graph.degree[pos] > 2: return True
        if self._graph.degree[pos] < 2: return False
        
        neighbors = tuple(self._graph.neighbors(pos))
        inbound = neighbors[0].direction_to(pos)
        outbound = pos.direction_to(neighbors[1])
        return outbound not in Pose.get_valid_turns(inbound)

    def get_connections_from_pose(self, pose: Pose, only_straight: bool = False) -> tuple[Pose]:
        connections = []
        for neighbor in self._graph.neighbors(pose.position):
            direction = pose.position.direction_to(neighbor)
            if only_straight and direction != pose.direction:
                continue
            if direction in Pose.get_valid_turns(pose.direction):
                connections.append(Pose(neighbor, direction))
        return tuple(connections)

    def get_segment(self, edge: tuple[Position, Position], end_on_signal: bool = False, only_platforms: bool = False, only_straight: bool = False
    ) -> tuple[tuple[Position], tuple[tuple[Position, Position]]]:
        
        
        edges: set[tuple[Position, Position]] = set()
        nodes: set[Position] = set()
        stack: deque[Pose] = deque()

        a, b = edge
        if only_platforms and 'station' not in self._graph.edges[edge]: raise ValueError("No platform on the given edge")
        
        edges.add((a, b))
        
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
                edge = (pose.position, neighbor)
                edges.add(edge)

                # skip conditions
                if neighbor in nodes or neighbor in {s.position for s in stack}:
                    continue
                
                if self.is_junction(neighbor):
                    continue
                
                if end_on_signal and 'signal' in self._graph[neighbor]:
                    continue
                
                if only_platforms and 'station' not in self._graph.edges[edge]:
                    continue
                
                stack.append(Pose(neighbor, direction))

        return nodes, edges