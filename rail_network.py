class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class RailNode:
    def __init__(self, node_id, pos: Point):
        self.id = node_id
        self.pos = pos        # (x, y) coordinate
        self.connections = [] # List of RailSegments

class RailSegment:
    def __init__(self, start_node, end_node, points: list[Point]):
        self.start = start_node
        self.end = end_node
        self.points = points
        self.length = self.calculate_length()
    
    def calculate_length(self):
        length = 0
        for i in range(1, len(self.points)):
            x1, y1 = self.points[i-1].x, self.points[i-1].y
            x2, y2 = self.points[i].x, self.points[i].y
            length += ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        return length

class RailNetwork:
    def __init__(self):
        self.nodes = {}
        self.segments = []

    def add_node(self, node_id, pos):
        node = RailNode(node_id, pos)
        self.nodes[node_id] = node
        return node

    def add_segment(self, start_id, end_id, points):
        start_node = self.nodes[start_id]
        end_node = self.nodes[end_id]
        segment = RailSegment(start_node, end_node, points)
        self.segments.append(segment)
        start_node.connections.append(segment)
        end_node.connections.append(segment)
        return segment

