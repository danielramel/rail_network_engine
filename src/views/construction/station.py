import pygame
from utils import point_within_station_rect, station_rects_overlap, snap_to_grid
from graphics.camera import Camera
from models.map import RailMap
from models.construction import ConstructionState
from ui_elements.draw_utils import draw_station
from config.colors import RED, YELLOW


def render_station_preview(surface : pygame.Surface, camera: Camera, state: ConstructionState, map: RailMap, pos: tuple[int, int]):
    snapped = snap_to_grid(*camera.screen_to_world(*pos))
    
    color = YELLOW
    if any(point_within_station_rect(pos, snapped) for pos in map.graph.nodes):
        color = RED
    elif any(station_rects_overlap(station_pos, snapped) for station_pos in map.stations.keys()):
        color = RED
    else:
        color = YELLOW

    draw_station(surface, camera, snapped, "STATION", color=color)

    
    
    