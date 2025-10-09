import pygame
from graphics.camera import Camera
from models.construction import ConstructionState
from models.geometry import Position
from domain.rail_map import RailMap
from models.station import Station
from ui.utils import draw_dotted_line, draw_station
from config.colors import LIGHTBLUE, RED, YELLOW
from services.construction.station_target import find_station_target

def render_station_preview(surface: pygame.Surface, world_pos: Position, state: ConstructionState, map: RailMap, camera: Camera):
    moving_station = state.moving_station
    target = find_station_target(map, world_pos, moving_station)

    if not moving_station and target.hovered_station_pos is not None:
        draw_station(surface, map.get_station_at(target.hovered_station_pos), camera, color=LIGHTBLUE)
        return

        
    if moving_station:
        color = RED if target.blocked_by_node or target.overlaps_station else LIGHTBLUE
        station = Station(moving_station.name, target.snapped)
        draw_station(surface, station, camera, color=color)
        for middle_point in map.get_platforms_middle_points(moving_station):
            draw_dotted_line(surface, middle_point, target.snapped, camera, color=color)
            
    else:
        color = RED if target.blocked_by_node or target.overlaps_station else YELLOW
        station = Station("STATION", target.snapped)
        draw_station(surface, station, camera, color=color)