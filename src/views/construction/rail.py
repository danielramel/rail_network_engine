import pygame
from config.colors import RED, YELLOW
from graphics.camera import Camera
from models.map import RailMap, find_path
from models.map.pathfinding import can_be_part_of_path
from ui_elements import draw_node
from models.position import Position, PositionWithDirection


def render_rail_preview(surface : pygame.Surface, world_pos: Position, anchor: PositionWithDirection, map: RailMap, camera: Camera):
    snapped = world_pos.snap_to_grid()
    if not can_be_part_of_path(snapped, map):
        draw_node(surface, camera, snapped, color=RED)
        if anchor is not None:
            draw_node(surface, camera, anchor.position, color=RED)
        return

    if anchor is None:
        draw_node(surface, camera, snapped, color=YELLOW)
        return

    if anchor.position == snapped:
        draw_node(surface, camera, snapped, color=YELLOW)
        return

    found_path = find_path(anchor, snapped, map)
    if not found_path:
        draw_node(surface, camera, snapped, color=RED)
        draw_node(surface, camera, anchor.position, color=RED)
        return
    
    
    screen_points = [tuple(camera.world_to_screen(Position(*pt))) for pt in found_path]
    pygame.draw.aalines(surface, YELLOW, False, screen_points)
    draw_node(surface, camera, snapped, color=YELLOW)
    draw_node(surface, camera, anchor.position, color=YELLOW)