import pygame

from core.graphics.camera import Camera
from core.models.geometry import Position, Edge
from core.config.color import Color


def draw_train(surface: pygame.Surface, edges: tuple[Edge], camera: Camera, edge_progress: float = 0.0, border_color: tuple[int, int, int] = None) -> None:
    if edge_progress < 0.5:
        draw_occupied_edge(surface, edges[0].a, edges[0].b, camera, color=Color.RED, start=edge_progress+0.5, end=1.0, border_color=border_color)
        draw_occupied_edge(surface, edges[1].a, edges[1].b, camera, color=Color.RED, start=0.0, end=edge_progress, border_color=border_color)
        draw_occupied_edge(surface, edges[1].a, edges[1].b, camera, color=Color.LIGHTBLUE, start=edge_progress+0.5, end=1.0, border_color=border_color)
        for edge in edges[2:-2]:
            draw_occupied_edge(surface, edge.a, edge.b, camera, color=Color.LIGHTBLUE, start=0.0, end=edge_progress, border_color=border_color)
            draw_occupied_edge(surface, edge.a, edge.b, camera, color=Color.LIGHTBLUE, start=edge_progress + 0.5, end=1.0, border_color=border_color)
        draw_occupied_edge(surface, edges[-2].a, edges[-2].b, camera, color=Color.LIGHTBLUE, start=0.0, end=edge_progress, border_color=border_color)
        draw_occupied_edge(surface, edges[-2].a, edges[-2].b, camera, color=Color.WHITE, start=edge_progress + 0.5, end=1.0, border_color=border_color)
        draw_occupied_edge(surface, edges[-1].a, edges[-1].b, camera, color=Color.WHITE, start=0.0, end=edge_progress, border_color=border_color)
        
    else:
        draw_occupied_edge(surface, edges[1].a, edges[1].b, camera, color=Color.RED, start=edge_progress-0.5, end=edge_progress, border_color=border_color)
        for edge in edges[2:-1]:
            draw_occupied_edge(surface, edge.a, edge.b, camera, color=Color.LIGHTBLUE, start=edge_progress - 0.5, end=edge_progress, border_color=border_color)
        draw_occupied_edge(surface, edges[-1].a, edges[-1].b, camera, color=Color.WHITE, start=edge_progress-0.5, end=edge_progress, border_color=border_color)
    


import math

def draw_occupied_edge(
    surface: pygame.Surface,
    a: Position,
    b: Position,
    camera: Camera,
    color: tuple[int, int, int],
    start: float,
    end: float,
    border_color: tuple[int, int, int] | None = None,
) -> None:
    if start == end:
        return

    a = camera.world_to_screen(a)
    b = camera.world_to_screen(b)
    (a_x, a_y), (b_x, b_y) = a, b
    dx = b_x - a_x
    dy = b_y - a_y

    dash_start_x = a_x + dx * start
    dash_start_y = a_y + dy * start
    dash_end_x = a_x + dx * end
    dash_end_y = a_y + dy * end

    width = max(3, int(10 * int(camera.scale)))

    rect_length = ((dash_end_x - dash_start_x) ** 2 + (dash_end_y - dash_start_y) ** 2) ** 0.5
    angle = math.atan2(dash_end_y - dash_start_y, dash_end_x - dash_start_x)

    rect_surface = pygame.Surface((rect_length, width), pygame.SRCALPHA)
    pygame.draw.rect(rect_surface, color, (0, 0, rect_length, width))
    if border_color is not None:
        pygame.draw.rect(rect_surface, border_color, (0, 0, rect_length, width), 2)

    rotated = pygame.transform.rotate(rect_surface, -math.degrees(angle))
    surface.blit(rotated, (dash_start_x - rotated.get_width() / 2, dash_start_y - rotated.get_height() / 2))