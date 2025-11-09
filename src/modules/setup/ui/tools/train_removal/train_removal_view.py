from core.models.geometry import Position
from modules.setup.models.setup_state import SetupAction
from modules.setup.models.setup_view import SetupView
from shared.ui.utils.nodes import draw_node
from core.config.color import Color

class TrainRemovalView(SetupView):
    def render(self, world_pos: Position | None) -> None:
        if world_pos is None:
            return
        self._state.preview.clear()
        closest_edge = world_pos.closest_edge(self._railway.graph.edges, self._camera.scale)
        if closest_edge and self._railway.stations.is_edge_platform(closest_edge):
            self._state.preview.edge = closest_edge
            self._state.preview.action = SetupAction.REMOVE
        else:
            draw_node(self._surface, world_pos, self._camera, color=Color.RED)