from shared.ui.enums.edge_action import EdgeAction
from .bulldoze_target import BulldozeTargetType, find_bulldoze_target
from modules.setup.construction.models.construction_tool_view import ConstructionToolView
from core.models.geometry.position import Position
from shared.ui.utils.nodes import draw_node
from shared.ui.utils.station import draw_station
from core.config.color import Color

class BulldozeView(ConstructionToolView):
    def render(self, world_pos: Position | None):
        self._state.preview.clear()
        
        if world_pos is None:
            return
        
        target = find_bulldoze_target(self._railway, world_pos)
        if target.kind == BulldozeTargetType.SIGNAL:
            self._state.preview.nodes = frozenset((target.node,))
        elif target.kind == BulldozeTargetType.STATION:
            draw_station(self._screen, self._railway.stations.get_by_node(target.node), self._camera, color=Color.RED)
        elif target.kind == BulldozeTargetType.NONE:
            draw_node(self._screen, world_pos, self._camera, color=Color.RED)
        elif target.kind == BulldozeTargetType.PLATFORM:
            self._state.preview.edges = target.edges
            self._state.preview.edge_action = EdgeAction.SPEED
        elif target.kind == BulldozeTargetType.SECTION:
            self._state.preview.edges = target.edges
            self._state.preview.nodes = target.nodes
            self._state.preview.edge_action = EdgeAction.BULLDOZE