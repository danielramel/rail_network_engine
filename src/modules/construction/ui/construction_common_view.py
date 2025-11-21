from shared.ui.enums.edge_action import EdgeAction
from core.models.geometry.position import Position
from shared.ui.utils import draw_grid, draw_track, draw_node, draw_signal, draw_station, draw_dotted_line
from core.config.color import Color
from modules.construction.models.construction_view import ConstructionView

class ConstructionCommonView(ConstructionView):
    def render(self, world_pos: Position | None) -> None:
        draw_grid(self._screen, self._camera)

        for edge, data in self._railway.graph.all_edges_with_data():
            speed = data.get('speed')
            length = data.get('length')
            if edge in self._state.preview.edges:
                draw_track(self._screen, edge, self._camera, self._state.preview.edge_action, speed=speed, length=length)
            elif self._railway.stations.is_edge_platform(edge):
                draw_track(self._screen, edge, self._camera, EdgeAction.PLATFORM, length=length)
            else:
                draw_track(self._screen, edge, self._camera, EdgeAction.SPEED, speed=speed, length=length)

        for node in self._railway.graph_service.junctions:
            draw_node(self._screen, node, self._camera, junction=True)

        for signal in self._railway.signals.all():
            if self._state.is_bulldoze_preview_node(signal.position):
                draw_signal(self._screen, signal, self._camera, color=Color.RED)
            else:
                draw_signal(self._screen, signal, self._camera)

        for station in self._railway.stations.all():
            if self._state.is_station_being_moved(station):
                continue
            for middle_point in self._railway.stations.platforms_middle_points(station):
                draw_dotted_line(self._screen, middle_point, station.position, self._camera, color=Color.PURPLE)
            draw_station(self._screen, station, self._camera)