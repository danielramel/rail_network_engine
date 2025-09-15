from dataclasses import dataclass, field
from itertools import count
from typing import List, Tuple, Optional
from models import Point


@dataclass(frozen=True)
class RailNode:
    id: int
    pos: Point
    connections: List[int] = field(default_factory=list)


@dataclass(frozen=True)
class RailSegment:
    id: int
    start: RailNode
    end: RailNode
    points: Tuple[Point, ...]


class RailNetwork:
    def __init__(self):
        self.nodes: dict[int, RailNode] = {}
        self.segments: dict[int, RailSegment] = {}
        self._node_id_gen = count()
        self._segment_id_gen = count()

    def add_node(self, pos: Point) -> RailNode:
        existing_node = self.find_node_at(pos)
        if existing_node:
            return existing_node

        node_id = next(self._node_id_gen)
        node = RailNode(id=node_id, pos=pos)
        self.nodes[node_id] = node
        return node

    def find_node_at(self, pos: Point) -> Optional[RailNode]:
        for node in self.nodes.values():
            if node.pos == pos:
                return node
        return None

    def add_segment(self, start_id: int, end_id: int, points: List[Point]) -> Optional[RailSegment]:
        start_node = self.nodes[start_id]
        end_node = self.nodes[end_id]

        if len(start_node.connections) == 1:
            existing_segment = self.segments[start_node.connections[0]]
            if existing_segment.start.id == start_id:
                updated_segment = RailSegment(
                    id=existing_segment.id,
                    start=end_node,
                    end=existing_segment.end,
                    points=tuple(reversed(points)) + existing_segment.points[1:]
                )
            else:
                updated_segment = RailSegment(
                    id=existing_segment.id,
                    start=existing_segment.start,
                    end=end_node,
                    points=existing_segment.points[:-1] + tuple(reversed(points))
                )
            self.segments[existing_segment.id] = updated_segment
            del self.nodes[start_id]

        # Case 2: Create new segment
        else:
            seg_id = next(self._segment_id_gen)
            segment = RailSegment(id=seg_id, start=start_node, end=end_node, points=tuple(points))
            self.segments[seg_id] = segment

        # Case 3: Merge into existing segment from end node
        if len(end_node.connections) == 1:
            existing_segment = self.segments[end_node.connections[0]]
            if existing_segment.start.id == end_id:
                updated_segment = RailSegment(
                    id=existing_segment.id,
                    start=start_node,
                    end=existing_segment.end,
                    points=segment.points + existing_segment.points[1:]
                )
            else:
            updated_segment = RailSegment(
                id=existing_segment.id,
                start=start_node,
                end=existing_segment.end,
                points=tuple(points[:-1]) + existing_segment.points
            )
            self.segments[existing_segment.id] = updated_segment
            del self.nodes[end_id]
            del self.segments[segment.id]
            segment = updated_segment

        # Update connections
        if start_id in self.nodes:
            self.nodes[start_id].connections.append(segment.id)
        if end_id in self.nodes:
            self.nodes[end_id].connections.append(segment.id)

        return segment

    def find_segment(self, start_id: int, end_id: int, points: Optional[List[Point]] = None) -> Optional[RailSegment]:
        for seg in self.segments.values():
            if (seg.start.id == start_id and seg.end.id == end_id) or \
               (seg.start.id == end_id and seg.end.id == start_id):
                if points is None:
                    return seg
                candidate1 = RailSegment(seg.id, self.nodes[start_id], self.nodes[end_id], tuple(points))
                candidate2 = RailSegment(seg.id, self.nodes[end_id], self.nodes[start_id], tuple(reversed(points)))
                if seg == candidate1 or seg == candidate2:
                    return seg
        return None

    def get_connections(self, node_id: int) -> List[RailSegment]:
        return [self.segments[sid] for sid in self.nodes[node_id].connections]
