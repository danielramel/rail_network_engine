from core.config.config import Config
from core.models.geometry.position import Position
from modules.setup.train_placement.models.train_placement_view import TrainPlacementView
from shared.ui.utils.nodes import draw_node
from core.config.color import Color

class TrainAdderView(TrainPlacementView):
    def render(self, world_pos: Position | None) -> None:
        self._state.preview.clear()
        if world_pos is None:
            return
        closest_edge = self._railway.graph_service.get_closest_edge(world_pos)
        if closest_edge is None:
            draw_node(self._screen, world_pos, self._camera, Color.YELLOW)
            return 
        
        is_valid, edges = self._railway.graph_service.calculate_train_preview(closest_edge, self._state.train_config.total_length)
        if not is_valid:
            self._state.preview.invalid_train_placement_edges = edges
        else:
            self._state.preview.train_to_preview = self._railway.trains.create_train(edges, self._state.train_config)