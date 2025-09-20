import pygame
from utils import rects_overlap, snap_to_grid
from graphics.camera import Camera
from models.map import RailMap
from models.construction import ConstructionState
from ui_elements.draw_utils import draw_station
from config.colors import RED, YELLOW


def render_station_construction(surface : pygame.Surface, camera: Camera, state: ConstructionState, map: RailMap, pos: tuple[int, int]):
    snapped = snap_to_grid(*camera.screen_to_world(*pos))

    for station_pos in map.stations.keys():
        if rects_overlap(station_pos, snapped):
            draw_station(surface, camera, snapped, "STATION", color=RED)
            return
        
    draw_station(surface, camera, snapped, "STATION", color=YELLOW)

    
    
    