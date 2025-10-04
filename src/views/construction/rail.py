import pygame
from config.colors import YELLOW, RED
from graphics.camera import Camera
from models.map import RailMap
from ui.utils import color_from_speed, draw_node
from models.geometry import Position, Pose


def render_rail_preview(surface: pygame.Surface, world_pos: Position, state_info: dict, map: RailMap, camera: Camera):
    snapped = world_pos.snap_to_grid()
    construction_anchor: Pose = state_info['construction_anchor']
    
    if map.is_blocked(snapped):
        draw_node(surface, snapped, camera, color=RED)
        if construction_anchor is not None:
            draw_node(surface, construction_anchor.position, camera, color=RED)
        return

    color = color_from_speed(state_info['track_speed'])
    if not construction_anchor:
        draw_node(surface, snapped, camera, color=color)
        return

    if construction_anchor.position == snapped:
        draw_node(surface, snapped, camera, color=color)
        return

    found_path = map.find_path(construction_anchor, snapped)
    if not found_path:
        draw_node(surface, snapped, camera, color=RED)
        draw_node(surface, construction_anchor.position, camera, color=RED)
        return
    
    
    screen_points = [tuple(camera.world_to_screen(Position(*pt))) for pt in found_path]
    pygame.draw.aalines(surface, color, False, screen_points)
    draw_node(surface, snapped, camera, color=color)
    draw_node(surface, construction_anchor.position, camera, color=color)