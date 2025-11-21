from core.models.geometry import Position
from modules.setup.models.setup_state import SetupAction
from modules.setup.models.setup_view import SetupView
from shared.ui.utils.nodes import draw_node
from core.config.color import Color

class TrainPlacementView(SetupView):
    def render(self, world_pos: Position | None) -> None:
        if world_pos is None:
            return
        self._state.preview.clear()
        closest_edge = self._railway.graph_service.get_closest_edge_on_grid(world_pos, self._camera.scale)
        if closest_edge and self._railway.stations.is_edge_platform(closest_edge) and not self._railway.trains.get_train_on_edge(closest_edge):
            self._state.preview.edge = closest_edge
            self._state.preview.action = SetupAction.ADD
            
        else:
            draw_node(self._screen, world_pos, self._camera, color=Color.YELLOW)