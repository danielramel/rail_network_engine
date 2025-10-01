import pygame
from config.colors import RED, YELLOW
from graphics.camera import Camera
from models.map import RailMap
from ui_elements import draw_node
from models.geometry import Position, Pose


def render_rail_preview(surface : pygame.Surface, world_pos: Position, anchor: Pose, map: RailMap, camera: Camera):
    snapped = world_pos.snap_to_grid()
    if map.is_blocked(snapped):
        draw_node(surface, snapped, camera, color=RED)
        if anchor is not None:
            draw_node(surface, anchor.position, camera, color=RED)
        return

    if anchor is None:
        draw_node(surface, snapped, camera, color=YELLOW)
        return

    if anchor.position == snapped:
        draw_node(surface, snapped, camera, color=YELLOW)
        return

    found_path = map.find_path(anchor, snapped)
    if not found_path:
        draw_node(surface, snapped, camera, color=RED)
        draw_node(surface, anchor.position, camera, color=RED)
        return
    
    
    screen_points = [tuple(camera.world_to_screen(Position(*pt))) for pt in found_path]
    pygame.draw.aalines(surface, YELLOW, False, screen_points)
    draw_node(surface, snapped, camera, color=YELLOW)
    draw_node(surface, anchor.position, camera, color=YELLOW)