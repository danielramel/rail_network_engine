import pygame
from ui_elements.draw_utils import draw_signal
from utils import snap_to_grid
from config.colors import RED
from graphics.camera import Camera
from models.network import RailNetwork
from models.construction import ConstructionState


def render_signal_construction(surface : pygame.Surface, camera: Camera, state: ConstructionState, network: RailNetwork, pos: tuple[int, int]):
    snapped = snap_to_grid(*camera.screen_to_world(*pos))
    
    if snapped in network.graph:
        if network.graph.degree[snapped] > 2:
            return
        if 'signal' in network.graph.nodes[snapped]:
            return
        
    return
    
