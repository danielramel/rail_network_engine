import pygame
from graphics.camera import Camera
from models.geometry import Position
from models.map.rail_map import RailMap
from models.map.station_repository import Station
from ui.utils import draw_station
from config.colors import LIGHTBLUE, RED, YELLOW
from services.construction.station_target import find_station_target

def render_station_preview(surface: pygame.Surface, world_pos: Position, mode_info: dict, map: RailMap, camera: Camera):
    moving_station = mode_info.get('moving_station')
    target = find_station_target(map, world_pos, moving_station)

    if not moving_station and target.hovered_station_pos is not None:
        draw_station(surface, map.get_station_at(target.hovered_station_pos), camera, color=LIGHTBLUE)
        return

    if target.blocked_by_node or target.overlaps_station:
        color = RED
    else:
        color = LIGHTBLUE if moving_station else YELLOW

    station = Station(moving_station.name if moving_station else "STATION", target.snapped)
    draw_station(surface, station, camera, color=color)