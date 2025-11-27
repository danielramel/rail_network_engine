from shared.ui.enums.edge_action import EdgeAction
from core.models.geometry.position import Position
from shared.ui.utils.grid import draw_grid
from shared.ui.utils.tracks import draw_track
from shared.ui.utils.nodes import draw_junction_node
from shared.ui.utils.signal import draw_signal
from shared.ui.utils.station import draw_station
from shared.ui.utils.lines import draw_dotted_line
from core.config.color import Color


from core.config.color import Color
from modules.setup.construction.models.construction_view import ConstructionView

class ConstructionCommonView(ConstructionView):
    def render(self, screen_pos: Position | None) -> None:
        draw_grid(self._screen, self._camera)

        for edge, data in self._railway.graph.all_edges_with_data():
            speed = data["speed"]
            length = data["length"]
            level = data.get("level", 0)
            if edge in self._state.preview.edges:
                edge_action = self._state.preview.edge_action
            elif self._railway.stations.is_edge_platform(edge):
                edge_action = EdgeAction.PLATFORM
            else:
                edge_action = EdgeAction.SPEED
                    
            draw_track(self._screen, edge, self._camera, edge_action, speed=speed, length=length)
                

        for node in self._railway.graph_service.junctions:
            draw_junction_node(self._screen, node, self._camera)

        for signal in self._railway.signals.all():
            if self._state.is_bulldoze_preview_node(signal.node):
                draw_signal(self._screen, signal, self._camera, color=Color.RED)
            else:
                draw_signal(self._screen, signal, self._camera)

        for station in self._railway.stations.all():
            if self._state.is_station_being_moved(station):
                continue
            for middle_point in self._railway.stations.platforms_middle_points(station):
                draw_dotted_line(self._screen, middle_point, station.node, self._camera, color=Color.PURPLE)
            draw_station(self._screen, station, self._camera)