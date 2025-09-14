from dataclasses import dataclass, field
from math import sqrt
from typing import List, Tuple, Optional


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class RailNode:
    id: int
    pos: Point


@dataclass(frozen=True)
class RailSegment:
    start: RailNode
    end: RailNode
    points: Tuple[Point, ...]
    length: float = field(init=False, compare=False)

    def __post_init__(self):
        object.__setattr__(self, "length", self.calculate_length())

    def calculate_length(self) -> float:
        length = 0.0
        for i in range(1, len(self.points)):
            x1, y1 = self.points[i-1].x, self.points[i-1].y
            x2, y2 = self.points[i].x, self.points[i].y
            length += sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return length


class RailNetwork:
    def __init__(self):
        self.nodes: dict[int, RailNode] = {}
        self.segments: List[RailSegment] = []

    def add_node(self, pos: Point) -> RailNode:
        existing_node = self.find_node_at(pos)
        if existing_node:
            return existing_node

        node_id = len(self.nodes)
        node = RailNode(node_id, pos)
        self.nodes[node_id] = node
        return node

    def find_node_at(self, pos: Point) -> Optional[RailNode]:
        for node in self.nodes.values():
            if node.pos == pos:
                return node
        return None

    def add_segment(self, start_id: int, end_id: int, points: List[Point]) -> Optional[RailSegment]:
        if self.find_segment(start_id, end_id):
            return None

        start_node = self.nodes[start_id]
        end_node = self.nodes[end_id]
        segment = RailSegment(start_node, end_node, tuple(points))
        print(f"Added segment: {segment}")
        self.segments.append(segment)
        return segment

    def find_segment(self, start_id: int, end_id: int, points: Optional[List[Point]] = None) -> Optional[RailSegment]:
        for seg in self.segments:
            if seg.start.id == start_id and seg.end.id == end_id or \
               seg.start.id == end_id and seg.end.id == start_id:
                if points is None:
                    return seg
                # Since RailSegment is a dataclass, we can compare directly
                start_node = self.nodes[start_id]
                end_node = self.nodes[end_id]
                candidate1 = RailSegment(start_node, end_node, tuple(points))
                candidate2 = RailSegment(end_node, start_node, tuple(reversed(points)))
                if seg == candidate1 or seg == candidate2:
                    return seg
        return None

    def get_connections(self, node_id: int) -> List[RailSegment]:
        return [seg for seg in self.segments if seg.start.id == node_id or seg.end.id == node_id]
