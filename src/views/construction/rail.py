import pygame
from utils import snap_to_grid
from config.colors import YELLOW
from graphics.camera import Camera
from models.map import RailMap, find_path
from models.construction import ConstructionState
from ui_elements import draw_node


def render_rail_construction(surface : pygame.Surface, camera: Camera, state: ConstructionState, network: RailMap, pos: tuple[int, int]):
    snapped = snap_to_grid(*camera.screen_to_world(*pos))
    if state.construction_anchor is None:
        draw_node(surface, camera, snapped, color=YELLOW)
        return
    
    if state.construction_anchor.point == snapped:
        draw_node(surface, camera, snapped, color=YELLOW)
        return
    
    found_path = find_path(state.construction_anchor, snapped)
    screen_points = [camera.world_to_screen(pt.x, pt.y) for pt in found_path]
    pygame.draw.lines(surface, YELLOW, False, screen_points, max(1, int(3 * camera.scale)))
    draw_node(surface, camera, snapped, color=YELLOW)
    draw_node(surface, camera, state.construction_anchor.point, color=YELLOW)