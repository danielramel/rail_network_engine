from networkx import Graph
from models.position import Position, PositionWithDirection
from collections import deque


class SegmentFinder:
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
        return SegmentFinder.VALID_TURNS[direction]

    def _compute_initial_state_for_edge(self, start_node: Position, end_node: Position, end_on_signal: bool) -> PositionWithDirection | None:
        if self._graph.degree(start_node) > 2 and self._graph.degree(end_node) > 2:
            return None

        start_has_signal = 'signal' in self._graph[start_node]
        end_has_signal = 'signal' in self._graph[end_node]

        if end_on_signal and start_has_signal and end_has_signal:
            return None

        if (self._graph.degree(start_node) > 2) or (end_on_signal and start_has_signal):
            direction = start_node.direction_to(end_node)
            return PositionWithDirection(end_node, direction)

        if (self._graph.degree(end_node) > 2) or (end_on_signal and end_has_signal):
            direction = end_node.direction_to(start_node)
            return PositionWithDirection(start_node, direction)

        return PositionWithDirection(start_node, (0, 0))

    def find_segment(
        self,
        start: Position | tuple[Position, Position],
        end_on_signal: bool = False,
        only_platforms: bool = False
    ) -> tuple[tuple[Position], tuple[tuple[Position, Position]]]:
        0
        edges: set[tuple[Position, Position]] = set()

        # initial state discovery
        if isinstance(start, Position):
            if only_platforms and 'platform' not in self._graph[start]: raise ValueError("No platform at the given node")
            initial = PositionWithDirection(start, (0, 0))
            
        elif isinstance(start, tuple) and len(start) == 2:
            a, b = start
            if only_platforms and 'platform' not in self._graph[a, b]: raise ValueError("No platform on the given edge")

            initial = self._compute_initial_state_for_edge(a, b, end_on_signal)
            if initial is None:
                return (set(), ((a, b),))

            edges.add((a, b))

        nodes: set[Position] = {initial.position}
        stack: deque[PositionWithDirection] = deque([initial])

        while stack:
            state = stack.popleft()
            valid_turns = SegmentFinder.get_valid_turns(state.direction)

            # create a set view of positions currently in the stack for quick membership
            stack_positions = {s.position for s in stack}

            for neighbor in self._graph.neighbors(state.position):
                new_direction = state.position.direction_to(neighbor)
                if new_direction not in valid_turns:
                    continue

                edge = (state.position, neighbor)
                edges.add(edge)

                # skip conditions
                if neighbor in stack_positions or neighbor in nodes:
                    continue
                if end_on_signal and 'signal' in self._graph[neighbor]:
                    continue
                if only_platforms and 'platform' not in self._graph[neighbor]:
                    continue

                deg = self._graph.degree(neighbor)
                if deg == 1:
                    nodes.add(neighbor)
                elif deg == 2:
                    nodes.add(neighbor)
                    stack.append(PositionWithDirection(neighbor, new_direction))
                else:
                    # degree > 2: add only if all neighbors already in nodes
                    if all(n in nodes for n in self._graph.neighbors(neighbor)):
                        nodes.add(neighbor)

        return nodes, edges