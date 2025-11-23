from shared.ui.enums.edge_action import EdgeAction
from modules.construction.models.construction_view import ConstructionView
from core.models.geometry.position import Position
from core.config.color import Color
from shared.ui.utils.lines import draw_dotted_line
from shared.ui.utils.station import draw_station
from shared.ui.utils.nodes import draw_node
from .portal_target import PortalTargetType, find_portal_target

class PortalView(ConstructionView):
    def render(self, world_pos: Position | None):
        if world_pos is None:
            return

        self._state.preview.clear()

        target = find_portal_target(self._railway, world_pos)
        if target.kind is PortalTargetType.NONE:
            draw_node(self._screen, world_pos, self._camera, Color.PURPLE)
            return

        self._state.preview.edges = target.edges
        if target.kind is PortalTargetType.INVALID:
            self._state.preview.edge_action = EdgeAction.INVALID_PLATFORM
        else:
            self._state.preview.edge_action = EdgeAction.PLATFORM