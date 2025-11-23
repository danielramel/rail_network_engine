from shared.ui.enums.edge_action import EdgeAction
from modules.construction.models.construction_view import ConstructionView
from core.models.geometry.position import Position
from core.config.color import Color
from shared.ui.utils.lines import draw_dotted_line
from shared.ui.utils.station import draw_station
from shared.ui.utils.nodes import draw_node
from .platform_target import PlatformTargetType, find_platform_target

class PlatformView(ConstructionView):
    def render(self, world_pos: Position | None):
        if world_pos is None:
            return

        target = find_platform_target(self._railway, world_pos, self._state.platform_edge_count, self._state.platform_waiting_for_station)
        if target.kind is PlatformTargetType.WAITING_FOR_STATION:
            middle_point = self._railway.stations.get_middle_of_platform(self._state.preview.edges)
            draw_dotted_line(self._screen, world_pos, middle_point, self._camera, color=Color.LIGHTBLUE)
            return
        
        if target.kind is PlatformTargetType.STATION_FOUND:
            draw_station(self._screen, target.station, self._camera, color=Color.LIGHTBLUE)
            middle_point = self._railway.stations.get_middle_of_platform(self._state.preview.edges)
            draw_dotted_line(self._screen, target.station.node, middle_point, self._camera, color=Color.LIGHTBLUE)
            return
        
        self._state.preview.clear()
        if target.kind is PlatformTargetType.NONE:
            draw_node(self._screen, world_pos, self._camera, Color.PURPLE)
            return

        self._state.preview.edges = target.edges
        if target.kind is PlatformTargetType.INVALID:
            self._state.preview.edge_action = EdgeAction.INVALID_PLATFORM
        else:
            self._state.preview.edge_action = EdgeAction.PLATFORM