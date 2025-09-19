import pygame
from utils import snap_to_grid
from graphics.camera import Camera
from models.map import RailMap
from models.construction import ConstructionState
from ui_elements.draw_utils import draw_station
from config.colors import YELLOW



def render_station_construction(surface : pygame.Surface, camera: Camera, state: ConstructionState, network: RailMap, pos: tuple[int, int]):
    snapped = snap_to_grid(*camera.screen_to_world(*pos))
    
    draw_station(surface, camera, snapped, color=YELLOW)

    
    
    