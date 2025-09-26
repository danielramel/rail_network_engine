import pygame
from config.colors import YELLOW
from graphics.camera import Camera
from models.map import RailMap, find_path
from models.construction import ConstructionState
from ui_elements import draw_node
from models.position import Position


def render_rail_preview(surface : pygame.Surface, camera: Camera, state: ConstructionState, map: RailMap, pos: Position):
    snapped = camera.screen_to_world(pos).snap_to_grid()
    if state.construction_anchor is None:
        draw_node(surface, camera, snapped, color=YELLOW)
        return
    
    if state.construction_anchor.position == snapped:
        draw_node(surface, camera, snapped, color=YELLOW)
        return
    
    found_path = find_path(state.construction_anchor, snapped)
    screen_points = [tuple(camera.world_to_screen(Position(*pt))) for pt in found_path]
    pygame.draw.aalines(surface, YELLOW, False, screen_points)
    draw_node(surface, camera, snapped, color=YELLOW)
    draw_node(surface, camera, state.construction_anchor.position, color=YELLOW)