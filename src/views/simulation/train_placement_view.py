from config.colors import YELLOW
from models.geometry import Position
from views.construction.base_view import BaseView

class TrainPlacementView(BaseView):
    def render(self, world_pos: Position | None):
        if world_pos is None:
            return
        

        closest_edge = world_pos.closest_edge(self._railway.graph.edges, self._camera.scale)
        if self._railway.stations.is_edge_platform(closest_edge):
            platform = self._railway.stations.get_platform_from_edge(closest_edge)
            for edge in platform.edges:
                from ui.utils import draw_edge
                draw_edge(self._surface, edge, self._camera, YELLOW, 50)