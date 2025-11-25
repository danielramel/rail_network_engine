from dataclasses import dataclass, asdict
from core.config.settings import Config
from math import hypot, floor

from typing import TYPE_CHECKING
from core.models.geometry.node import Node
if TYPE_CHECKING:
    from core.models.geometry.edge import Edge


@dataclass(frozen=True, order=True)
class Position:
    x: float
    y: float
            
    def __iter__(self):
        return iter((self.x, self.y))

    def snap_to_grid(self) -> Node:
        """Create a new Point snapped to the grid."""
        return Node(round(self.x), round(self.y))
    
    
    def is_within_station_rect(self, center: 'Node') -> bool:
        """Check if this point is within the station rectangle centered at another point."""
        return (
            abs(center.x - self.x) * 2 < Config.STATION_RECT_WIDTH + 1 and
            abs(center.y - self.y) * 2 < Config.STATION_RECT_HEIGHT + 1
        )
    
    def distance_to(self, other: Node) -> float:
        """Calculate the Euclidean distance to another position."""
        return hypot(self.x - other.x, self.y - other.y)
    
    def get_grid_edges(self, only_surface: bool = True) -> tuple['Edge']:
        from core.models.geometry.edge import Edge
        """Get the edges of the grid cell containing this position."""
        cell_x = floor(self.x)
        cell_y = floor(self.y)

        corners = (
            Node(cell_x, cell_y),
            Node(cell_x  + 1, cell_y),
            Node(cell_x + 1, cell_y + 1),
            Node(cell_x, cell_y + 1),
        )
        edges = (Edge(corners[0], corners[1]),
            Edge(corners[1], corners[2]),
            Edge(corners[2], corners[3]),
            Edge(corners[3], corners[0]),
            Edge(corners[0], corners[2]),
            Edge(corners[1], corners[3]))

        if only_surface:
            return tuple(edges)
        return tuple(edges) + tuple(edge.tunnel_level() for edge in edges) + tuple(Edge(edge.a, edge.b.tunnel_level()) for edge in edges) + tuple(Edge(edge.a.tunnel_level(), edge.b) for edge in edges)
    
    def distance_to_edge(self, edge: 'Edge') -> float:
        a, b = edge.a, edge.b
        ax, ay = a.x, a.y
        bx, by = b.x, b.y
        px, py = self.x, self.y

        abx, aby = bx - ax, by - ay
        apx, apy = px - ax, py - ay
        ab_len_sq = abx * abx + aby * aby

        if ab_len_sq == 0.0:
            return hypot(apx, apy)

        t = (apx * abx + apy * aby) / ab_len_sq
        if t <= 0.0:
            nx, ny = ax, ay
        elif t >= 1.0:
            nx, ny = bx, by
        else:
            nx, ny = ax + t * abx, ay + t * aby

        return hypot(px - nx, py - ny)