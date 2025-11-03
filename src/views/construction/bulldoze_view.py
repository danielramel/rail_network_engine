from models.construction_state import EdgeAction
from services.construction.bulldoze_target import BulldozeTargetType, find_bulldoze_target
from views.construction.base_construction_view import BaseConstructionView
from models.geometry import Position
from ui.utils import draw_signal, draw_station, draw_node
from config.colors import RED

class BulldozeView(BaseConstructionView):
    def render(self, world_pos: Position | None):
        self._state.preview.clear()
        
        if world_pos is None:
            return
        
        target = find_bulldoze_target(self._railway, world_pos, self._camera.scale)
        if target.kind == BulldozeTargetType.SIGNAL:
            self._state.preview.nodes = frozenset((target.position,))
        elif target.kind == BulldozeTargetType.STATION:
            draw_station(self._surface, self._railway.stations.get_by_position(target.position), self._camera, color=RED)
        elif target.kind == BulldozeTargetType.NONE:
            draw_node(self._surface, world_pos, self._camera, color=RED)
        elif target.kind == BulldozeTargetType.PLATFORM:
            self._state.preview.edges = target.edges
            self._state.preview.edge_action = EdgeAction.NORMAL
        elif target.kind == BulldozeTargetType.SEGMENT:
            self._state.preview.edges = target.edges
            self._state.preview.nodes = target.nodes
            self._state.preview.edge_action = EdgeAction.BULLDOZE