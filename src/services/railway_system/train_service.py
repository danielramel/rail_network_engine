import networkx as nx

from models.geometry.edge import Edge
from models.signal import Signal
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from models.railway_system import RailwaySystem


class TrainService:
    def __init__(self, railway: 'RailwaySystem'):
        self.railway = railway

    def get_initial_path(self, start_edge: Edge) -> tuple[list[Edge], Optional[Signal]]:
        if self.railway.graph.degree_at(start_edge.b) > 2:
            raise ValueError("Initial path cannot start at a junction.")
        
        visited = {start_edge.a, start_edge.b}
        pos = start_edge.b
        path = []
        while True:
            if self.railway.signals.has_signal_at(pos):
                signal = self.railway.signals.get(pos)
                if not signal.allowed:
                    return path, signal
                
            neighbors = list(self.railway._graph.neighbors(pos))
            if len(neighbors) == 1:
                path.append(Edge(pos, neighbors[0]))
                visited.add(pos)
                return path, None
            
            if neighbors[0] in visited and neighbors[1] in visited:
                return path, None
            
            next_pos = neighbors[0] if neighbors[0] not in visited else neighbors[1]
                
            if self.railway.graph.degree_at(pos) > 2:
                raise ValueError("Initial path cannot pass through a junction.")

            visited.add(next_pos)
            path.append(Edge(pos, next_pos))
            pos = next_pos