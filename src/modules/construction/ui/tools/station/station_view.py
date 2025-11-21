from modules.construction.models.construction_view import ConstructionView
from core.models.geometry import Position
from core.models.station import Station
from core.config.color import Color
from shared.ui.utils import draw_station, draw_dotted_line
from .station_target import find_station_target

class StationView(ConstructionView):
    def render(self, world_pos: Position | None):
        if world_pos is None:
            return
        moving_station = self._state.moving_station
        target = find_station_target(self._railway, world_pos, moving_station)

        # Hovering over an existing station while not moving
        if not moving_station and target.hovered_station_pos is not None:
            draw_station(self._screen, self._railway.stations.get_by_position(target.hovered_station_pos), self._camera, color=Color.LIGHTBLUE)
            return

        # Moving an existing station
        if moving_station:
            color = Color.RED if target.blocked_by_node or target.overlaps_station else Color.LIGHTBLUE
            station = Station(moving_station.name, target.snapped, -1)
            draw_station(self._screen, station, self._camera, color=color)
            for middle_point in self._railway.stations.platforms_middle_points(moving_station):
                draw_dotted_line(self._screen, middle_point, target.snapped, self._camera, color=color)
                
        # Preview for a new station
        else:
            color = Color.RED if target.blocked_by_node or target.overlaps_station else Color.YELLOW
            station = Station("STATION", target.snapped, -1)
            draw_station(self._screen, station, self._camera, color=color)
