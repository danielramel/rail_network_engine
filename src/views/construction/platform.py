import pygame
from config.colors import PURPLE, RED
from graphics.camera import Camera
from models.map import RailMap
from models.construction import ConstructionState, CursorTarget
from ui_elements.draw_utils import draw_dashed_line, draw_node, draw_station
from services.platform import get_platform_context
from models.position import Position


def render_platform_preview(surface: pygame.Surface, camera: Camera, state: ConstructionState, map: RailMap, pos: Position):
    world_pos = camera.screen_to_world(pos)
    context = get_platform_context(map, world_pos, camera.scale)
    if context.type == CursorTarget.EDGE:
        _, edges = map.get_segments_at(context.data, endOnSignal=True)
        color = RED if len(edges) < 5 else PURPLE
        for edge in edges:
            screen_points = [tuple(camera.world_to_screen(Position(*p))) for p in edge]
            pygame.draw.aaline(surface, color, *screen_points)
    elif context.type == CursorTarget.EMPTY:
        draw_node(surface, camera, context.data, color=PURPLE)

    if context.nearest_station is not None and context.type != CursorTarget.NODE:
        draw_station(surface, camera, context.nearest_station, map.stations[context.nearest_station], color=PURPLE)
        start = camera.world_to_screen(context.nearest_station)
        if context.type == CursorTarget.EDGE:
            end = camera.world_to_screen(Position.midpoint(*context.data))
        else:
            end = camera.world_to_screen(context.data)
        draw_dashed_line(surface, start, end, PURPLE)