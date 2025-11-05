import pygame
from views.base_view import BaseView
from models.geometry import Position
from models.station import Station
from config.colors import LIGHTBLUE, RED, YELLOW
from ui.utils import draw_station, draw_dotted_line
from services.construction.station_target import find_station_target

class StationView(BaseView):
    def render(self, world_pos: Position | None):
        if world_pos is None:
            return
        moving_station = self._state.moving_station
        target = find_station_target(self._railway, world_pos, moving_station)

        # Hovering over an existing station while not moving
        if not moving_station and target.hovered_station_pos is not None:
            draw_station(self._surface, self._railway.stations.get_by_position(target.hovered_station_pos), self._camera, color=LIGHTBLUE)
            return

        # Moving an existing station
        if moving_station:
            color = RED if target.blocked_by_node or target.overlaps_station else LIGHTBLUE
            station = Station(moving_station.name, target.snapped, -1)
            draw_station(self._surface, station, self._camera, color=color)
            for middle_point in self._railway.stations.platforms_middle_points(moving_station):
                draw_dotted_line(self._surface, middle_point, target.snapped, self._camera, color=color)
                
        # Preview for a new station
        else:
            color = RED if target.blocked_by_node or target.overlaps_station else YELLOW
            station = Station("STATION", target.snapped, -1)
            draw_station(self._surface, station, self._camera, color=color)
