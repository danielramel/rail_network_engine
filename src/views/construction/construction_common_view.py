from models.construction_state import EdgeAction
from models.geometry.position import Position
from views.construction.base_construction_view import BaseConstructionView
from ui.utils import draw_grid, draw_edge, draw_node, draw_signal, draw_station, draw_dotted_line
from config.colors import RED, PURPLE

class ConstructionCommonView(BaseConstructionView):
    def render(self, screen_pos: Position | None) -> None:
        draw_grid(self._surface, self._camera)

        for edge, speed in self._railway.graph.all_edges_with_attr('speed'):
            if edge in self._state.preview.edges:
                draw_edge(self._surface, edge, self._camera, self._state.preview.edge_action, speed=speed)
            elif self._railway.stations.is_edge_platform(edge):
                draw_edge(self._surface, edge, self._camera, EdgeAction.PLATFORM)
            else:
                draw_edge(self._surface, edge, self._camera, EdgeAction.SPEED, speed=speed)

        for node in self._railway.graph_service.junctions:
            draw_node(self._surface, node, self._camera)

        for signal in self._railway.signals.all():
            if self._state.is_bulldoze_preview_node(signal.position):
                draw_signal(self._surface, signal, self._camera, color=RED)
            else:
                draw_signal(self._surface, signal, self._camera)

        for station in self._railway.stations.all():
            if self._state.is_station_being_moved(station):
                continue
            for middle_point in self._railway.stations.platforms_middle_points(station):
                draw_dotted_line(self._surface, middle_point, station.position, self._camera, color=PURPLE)
            draw_station(self._surface, station, self._camera)