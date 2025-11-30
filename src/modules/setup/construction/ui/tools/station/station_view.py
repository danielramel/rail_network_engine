from modules.setup.construction.models.construction_tool_view import ConstructionToolView
from core.models.geometry.position import Position
from core.models.station import Station
from core.config.color import Color
from shared.ui.utils.lines import draw_dotted_line
from shared.ui.utils.station import draw_station
from .station_target import StationTargetType, find_station_target

class StationView(ConstructionToolView):
    def render(self, world_pos: Position | None):
        if world_pos is None:
            return
        moving_station = self._state.moving_station
        target = find_station_target(self._railway, world_pos, moving_station)

        if target.kind is StationTargetType.HOVERED:
            draw_station(self._screen, self._railway.stations.get_by_node(target.node), self._camera, color=Color.LIGHTBLUE)
            return

        if moving_station:
            color = Color.RED if target.kind is StationTargetType.BLOCKED else Color.LIGHTBLUE
            station = Station(moving_station.name, target.node, -1)
            draw_station(self._screen, station, self._camera, color=color)
            for middle_point in self._railway.stations.platforms_middle_points(moving_station):
                draw_dotted_line(self._screen, middle_point, target.node, self._camera, color=color)
                
        else:
            color = Color.RED if target.kind is StationTargetType.BLOCKED else Color.YELLOW
            station = Station("STATION", target.node, -1)
            draw_station(self._screen, station, self._camera, color=color)
