import pygame
from config.colors import RED
from graphics.camera import Camera
from domain.rail_map import RailMap
from models.construction import ConstructionState
from ui.utils import color_from_speed, draw_node
from models.geometry import Position
from services.construction.rail_target import find_rail_target

def render_rail_preview(surface: pygame.Surface, world_pos: Position, state: ConstructionState, map: RailMap, camera: Camera):
    target = find_rail_target(map, world_pos, state.construction_anchor)

    if target.kind == 'blocked':
        draw_node(surface, target.snapped, camera, color=RED)
        if state.construction_anchor is not None:
            draw_node(surface, state.construction_anchor.position, camera, color=RED)
        return

    color = color_from_speed(state.track_speed)

    if target.kind in ('node', 'anchor_same'):
        draw_node(surface, target.snapped, camera, color=color)
        return

    if target.kind == 'no_path':
        draw_node(surface, target.snapped, camera, color=RED)
        draw_node(surface, state.construction_anchor.position, camera, color=RED)
        return

    # path
    screen_points = [tuple(camera.world_to_screen(Position(*pt))) for pt in target.found_path]
    pygame.draw.aalines(surface, color, False, screen_points)
    draw_node(surface, target.snapped, camera, color=color)
    draw_node(surface, state.construction_anchor.position, camera, color=color)
