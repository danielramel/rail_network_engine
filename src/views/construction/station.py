import pygame
from graphics.camera import Camera
from models.geometry import Position
from models.map import RailMap
from models.construction import ConstructionState
from models.map.station_repository import Station
from ui.utils import draw_station
from config.colors import BLUE, RED, YELLOW


def render_station_preview(surface : pygame.Surface, world_pos: Position, moving_station: Station | None, map: RailMap, camera: Camera):    
    snapped = world_pos.snap_to_grid()
    if not moving_station:
        for station_pos in map.station_positions:
            if world_pos.is_within_station_rect(station_pos):
                draw_station(surface, map.get_station_at(station_pos), camera, color=BLUE)
                return
            
    if any(snapped.is_within_station_rect(node_pos) for node_pos in map.nodes):
        color = RED        
    elif any(snapped.station_rect_overlaps(station_pos) for station_pos in map.station_positions):
        color = RED
    else:
        color = BLUE if moving_station else YELLOW
    
    station = Station(moving_station.name if moving_station else "STATION" , snapped)
    draw_station(surface, station, camera, color=color)