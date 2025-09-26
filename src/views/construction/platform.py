import pygame
from config.colors import PURPLE, RED
from graphics.camera import Camera
from models.map import RailMap
from models.construction import ConstructionState, CursorTarget
from ui_elements.draw_utils import draw_node, draw_station
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

    if context.nearest_station is not None:
        draw_station(surface, camera, context.nearest_station, map.stations[context.nearest_station], color=PURPLE)
        start = camera.world_to_screen(context.nearest_station)
        if context.type == CursorTarget.EDGE:
            end = Position.midpoint(*context.data)
        else:
            end = camera.world_to_screen(context.data)
        dash_length = 10
        gap_length = 5
        dx, dy = end.x - start.x, end.y - start.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance == 0:
            return
        dashes = int(distance // (dash_length + gap_length))
        for i in range(dashes + 1):
            t1 = (i * (dash_length + gap_length)) / distance
            t2 = min((i * (dash_length + gap_length) + dash_length) / distance, 1)
            x1 = start.x + dx * t1
            y1 = start.y + dy * t1
            x2 = start.x + dx * t2
            y2 = start.y + dy * t2
            pygame.draw.line(surface, PURPLE, (x1, y1), (x2, y2), 2)