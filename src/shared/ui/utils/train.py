import pygame

from core.graphics.camera import Camera
from core.models.geometry import Position, Edge
from core.config.colors import BLUE, RED, WHITE, YELLOW


def draw_train(surface: pygame.Surface, edges: tuple[Edge], camera: Camera, edge_progress: float = 0.0) -> None:
    if edge_progress < 0.5:
        draw_occupied_edge(surface, edges[0].a, edges[0].b, camera, color=RED, start=edge_progress+0.5, end=1.0)
        draw_occupied_edge(surface, edges[1].a, edges[1].b, camera, color=RED, start=0.0, end=edge_progress)
        draw_occupied_edge(surface, edges[1].a, edges[1].b, camera, color=BLUE, start=edge_progress+0.5, end=1.0)
        for edge in edges[2:-2]:
            draw_occupied_edge(surface, edge.a, edge.b, camera, color=BLUE, start=0.0, end=edge_progress)
            draw_occupied_edge(surface, edge.a, edge.b, camera, color=BLUE, start=edge_progress + 0.5, end=1.0)
        draw_occupied_edge(surface, edges[-2].a, edges[-2].b, camera, color=BLUE, start=0.0, end=edge_progress)
        draw_occupied_edge(surface, edges[-2].a, edges[-2].b, camera, color=YELLOW, start=edge_progress + 0.5, end=1.0)
        draw_occupied_edge(surface, edges[-1].a, edges[-1].b, camera, color=YELLOW, start=0.0, end=edge_progress)
        
    else:
        draw_occupied_edge(surface, edges[1].a, edges[1].b, camera, color=RED, start=edge_progress-0.5, end=edge_progress)
        for edge in edges[2:-1]:
            draw_occupied_edge(surface, edge.a, edge.b, camera, color=BLUE, start=edge_progress - 0.5, end=edge_progress)
        draw_occupied_edge(surface, edges[-1].a, edges[-1].b, camera, color=YELLOW, start=edge_progress-0.5, end=edge_progress)
    

    

def draw_occupied_edge(surface: pygame.Surface, a: Position, b: Position, camera: Camera, color: tuple[int, int, int], start: float, end: float) -> None:
    if start == end: 
        ## fix ui bug
        return
    a = camera.world_to_screen(a)
    b = camera.world_to_screen(b)
    (a_x, a_y), (b_x, b_y) = a, b
    dx = b_x - a_x
    dy = b_y - a_y
    
    dash_start_x = a_x + (dx * start)
    dash_start_y = a_y + (dy * start)
    dash_end_x = a_x + (dx * end)
    dash_end_y = a_y + (dy * end)
    pygame.draw.aaline(surface, color, (int(dash_start_x), int(dash_start_y)), (int(dash_end_x), int(dash_end_y)), max(3, 10*int(camera.scale)))