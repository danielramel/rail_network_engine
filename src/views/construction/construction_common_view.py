from models.construction_state import EdgeAction
from models.geometry.edge import Edge
from models.geometry.position import Position
from views.construction.base_view import BaseView
from ui.utils import draw_grid, draw_track, draw_node, draw_signal, draw_station, draw_dotted_line
from config.colors import RED, PURPLE

class ConstructionCommonView(BaseView):
    def render(self, screen_pos: Position | None) -> None:
        draw_grid(self._surface, self._camera)

        for edge, data in self._railway.graph.all_edges_with_data():
            speed = data.get('speed')
            length = data.get('length')
            if edge in self._state.preview.edges:
                draw_track(self._surface, edge, self._camera, self._state.preview.edge_action, speed=speed, length=length)
            elif self._railway.stations.is_edge_platform(edge):
                draw_track(self._surface, edge, self._camera, EdgeAction.PLATFORM, length=length)
            else:
                draw_track(self._surface, edge, self._camera, EdgeAction.SPEED, speed=speed, length=length)

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