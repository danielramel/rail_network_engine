from core.models.geometry.position import Position
from modules.setup.train_placement.models.train_placement_tool_view import TrainPlacementToolView
from shared.ui.utils.nodes import draw_node
from core.config.color import Color

class TrainRemovalView(TrainPlacementToolView):
    def render(self, world_pos: Position | None) -> None:
        self._state.preview.clear()
        if world_pos is None:
            return
        closest_edge = self._railway.graph_service.get_closest_edge(world_pos)
        if closest_edge is not None:
            id = self._railway.trains.get_train_on_edge(closest_edge)
            if id is not None:
                self._state.preview.train_id_to_remove = id
                return

        draw_node(self._screen, world_pos, self._camera, color=Color.RED)