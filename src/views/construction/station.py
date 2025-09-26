import pygame
from graphics.camera import Camera
from models.position import Position
from models.map import RailMap
from models.construction import ConstructionState
from ui_elements.draw_utils import draw_station
from config.colors import RED, YELLOW


def render_station_preview(surface : pygame.Surface, camera: Camera, state: ConstructionState, map: RailMap, pos: Position):
    snapped = camera.screen_to_world(pos).snap_to_grid()

    color = YELLOW
    if any(snapped.within_station_rect(pos) for pos in map.graph.nodes):
        color = RED
    elif any(snapped.station_rect_overlaps(station_pos) for station_pos in map.stations.keys()):
        color = RED
    else:
        color = YELLOW

    draw_station(surface, camera, snapped, "STATION", color=color)

    
    
    