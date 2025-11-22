from core.config.settings import Config
from core.models.geometry.position import Position
from modules.setup.models.setup_view import SetupView
from shared.ui.utils.nodes import draw_node
from core.config.color import Color

class TrainPlacementView(SetupView):
    def render(self, world_pos: Position | None) -> None:
        self._state.preview.clear()
        if world_pos is None:
            return
        closest_edge = self._railway.graph_service.get_closest_edge(world_pos, self._camera.scale)
        if closest_edge and self._railway.stations.is_edge_platform(closest_edge) and not self._railway.trains.get_train_on_edge(closest_edge):
            platform = self._railway.stations.get_platform_from_edge(closest_edge)
            if self._state.train_config.total_length > len(platform) *  Config.SHORT_SEGMENT_LENGTH:
                self._state.preview.invalid_platform_edges = platform
            else:
                self._state.preview.train_to_preview = self._railway.trains.create_train(platform, self._state.train_config)
        else:
            draw_node(self._screen, world_pos, self._camera, Color.YELLOW)