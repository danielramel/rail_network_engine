from models.construction import EdgeType
from services.construction.bulldoze_target import BulldozeTargetType, find_bulldoze_target
from views.construction.base_construction_view import BaseConstructionView
from models.geometry import Position
from ui.utils import draw_signal, draw_station, draw_node
from config.colors import RED

class BulldozeView(BaseConstructionView):
    def render(self, world_pos: Position | None):
        self._construction_state.preview_edges = set()
        self._construction_state.preview_nodes = set()
        self._construction_state.preview_edges_type = None
        
        if world_pos is None:
            return
        
        target = find_bulldoze_target(self._map, world_pos, self._camera.scale)
        if target.kind == BulldozeTargetType.SIGNAL:
            draw_signal(self._surface, self._map.get_signal_at(target.pos), self._camera, color=RED)
        elif target.kind == BulldozeTargetType.STATION:
            draw_station(self._surface, self._map.get_station_at(target.pos), self._camera, color=RED)
        elif target.kind == BulldozeTargetType.NONE:
            draw_node(self._surface, world_pos, self._camera, color=RED)
        elif target.kind == BulldozeTargetType.PLATFORM:
            self._construction_state.preview_edges = target.edges
            self._construction_state.preview_edges_type = EdgeType.NORMAL
        elif target.kind == BulldozeTargetType.SEGMENT:
            self._construction_state.preview_edges = target.edges
            self._construction_state.preview_nodes = target.nodes
            self._construction_state.preview_edges_type = EdgeType.BULLDOZE