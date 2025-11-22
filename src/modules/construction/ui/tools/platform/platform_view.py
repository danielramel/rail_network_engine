from shared.ui.enums.edge_action import EdgeAction
from modules.construction.models.construction_view import ConstructionView
from core.models.geometry import Position
from core.config.color import Color
from shared.ui.utils import draw_node, draw_station, draw_dotted_line
from .platform_target import PlatformTargetType, find_platform_target

class PlatformView(ConstructionView):
    def render(self, world_pos: Position | None):
        if world_pos is None:
            return
        
        # handle the “select_station” preview mode first
        if self._state.platform_waiting_for_station:
            middle_point = self._railway.stations.get_middle_of_platform(self._state.preview.edges)
            for station in self._railway.stations.all():
                if world_pos.is_within_station_rect(station.position):
                    draw_station(self._screen, station, self._camera, color=Color.LIGHTBLUE)
                    draw_dotted_line(self._screen, station.position, middle_point, self._camera, color=Color.LIGHTBLUE)
                    break
            else:
                draw_dotted_line(self._screen, world_pos, middle_point, self._camera, color=Color.LIGHTBLUE)
            return

        self._state.preview.clear()

        target = find_platform_target(self._railway, world_pos, self._camera.scale, self._state.platform_edge_count)
        if target.kind is PlatformTargetType.NONE:
            draw_node(self._screen, world_pos, self._camera, color=Color.PURPLE)
            return

        self._state.preview.edges = target.edges
        if target.kind is PlatformTargetType.INVALID:
            self._state.preview.edge_action = EdgeAction.INVALID_PLATFORM
        else:
            self._state.preview.edge_action = EdgeAction.PLATFORM