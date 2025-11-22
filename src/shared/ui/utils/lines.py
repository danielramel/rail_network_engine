import pygame
from core.models.geometry.node import Node
from core.models.geometry.position import Position
from core.graphics.camera import Camera


def draw_dotted_line(screen: pygame.Surface, world_a: Position | Node, world_b: Position | Node, camera: Camera, color, num_dots: int = None):
    """Draw a dotted line on the screen from start_pos to end_pos."""
    a = camera.world_to_screen(world_a)
    b = camera.world_to_screen(world_b)
    if a == b:
        return
    (x1, y1), (x2, y2) = a, b
    dx = x2 - x1
    dy = y2 - y1
    
    distance = a.distance_to(b)
    if num_dots is None:
        num_dots = max(1, int(distance // 10))  # default: one dot every 10 pixels
    dot_spacing = distance / num_dots
    for i in range(num_dots):
        dot_x = x1 + (dx * (i * dot_spacing) / distance)
        dot_y = y1 + (dy * (i * dot_spacing) / distance)
        pygame.draw.circle(screen, color, (int(dot_x), int(dot_y)), 1)

def draw_dashed_line(screen: pygame.Surface, world_a: Position, world_b: Position, camera: Camera, color, num_dashes: int = 10):
    a = camera.world_to_screen(world_a)
    b = camera.world_to_screen(world_b)
    (a_x, a_y), (b_x, b_y) = a, b
    dx = b_x - a_x
    dy = b_y - a_y

    distance = a.distance_to(b)
    dash_length = distance // (num_dashes * 2)
    
    for i in range(num_dashes):
        dash_start_x = a_x + (dx * ((i * 2 + 0.5) * dash_length) / distance)
        dash_start_y = a_y + (dy * ((i * 2 + 0.5) * dash_length) / distance)
        dash_end_x = a_x + (dx * ((i * 2 + 1.5) * dash_length) / distance)
        dash_end_y = a_y + (dy * ((i * 2 + 1.5) * dash_length) / distance)
        pygame.draw.aaline(screen, color, (int(dash_start_x), int(dash_start_y)), (int(dash_end_x), int(dash_end_y)), max(1, 2//int(camera.scale)))