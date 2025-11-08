from core.models.geometry import Position
from modules.setup.models.setup_view import SetupView

class TrainPlacementView(SetupView):
    def render(self, world_pos: Position | None) -> None:
        if world_pos is None:
            return
        self._state.preview.clear()
        closest_edge = world_pos.closest_edge(self._railway.graph.edges, self._camera.scale)
        if closest_edge and self._railway.stations.is_edge_platform(closest_edge):
            self._state.preview.edge = closest_edge
            train = self._railway.trains.get_train_on_edge(closest_edge)
            if train is not None:
                locomotive_edge = train.occupied_edges()[0]
                self._state.preview.reversed = locomotive_edge.a < locomotive_edge.b