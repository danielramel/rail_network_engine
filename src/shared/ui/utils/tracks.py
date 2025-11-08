import pygame
from core.config.colors import GREEN, LIME, PURPLE, LIGHTBLUE, RED, WHITE, BLACK, YELLOW

from core.graphics.camera import Camera
from core.models.geometry import Position
from core.models.geometry.edge import Edge
from shared.ui.enums.edge_action import EdgeAction
from shared.ui.services.color_from_speed import color_from_speed
from .lines import draw_dotted_line

        
def draw_track(surface: pygame.Surface, edge: Edge, camera: Camera, edge_action: EdgeAction, length: int, speed: int = None) -> None:   
    if edge_action in (EdgeAction.BULLDOZE, EdgeAction.INVALID_PLATFORM):
        draw_rail(surface, edge, camera, color=RED, length=length)
    elif edge_action == EdgeAction.PLATFORM_SELECTED:
        draw_platform(surface, edge, camera, length=length, color=LIGHTBLUE)
    elif edge_action == EdgeAction.PLATFORM:
        draw_platform(surface, edge, camera, length=length, color=PURPLE)
    elif edge_action == EdgeAction.LOCKED_PLATFORM:
        draw_rail(surface, edge, camera, color=PURPLE, length=length)
        draw_platform(surface, edge, camera, length=length, color=LIME)
    elif edge_action == EdgeAction.LOCKED_PREVIEW:
        draw_rail(surface, edge, camera, color=GREEN, length=length)
    elif edge_action == EdgeAction.LOCKED:
        draw_rail(surface, edge, camera, color=LIME, length=length)
    elif edge_action == EdgeAction.NORMAL:
        draw_rail(surface, edge, camera, color=WHITE, length=length)
    elif edge_action == EdgeAction.SPEED:
        color = color_from_speed(speed)
        draw_rail(surface, edge, camera, color=color, length=length)

def draw_rail(surface: pygame.Surface, edge: Edge, camera: Camera, color: tuple[int, int, int], length: int) -> None:
    """Draw a track as a dotted line on the surface from edge.a to edge.b."""
    if length == 50:
        pygame.draw.aaline(surface, color, tuple(camera.world_to_screen(edge.a)), tuple(camera.world_to_screen(edge.b)), max(1, 2*int(camera.scale)))
    elif length == 500:
        draw_dotted_line(surface, edge.a, edge.b, camera, color=color, num_dots=5)
    else:
        raise NotImplementedError("Edge length drawing not implemented for length:", length)
        
def draw_platform(surface: pygame.Surface, edge: Edge, camera: Camera, length: int, color=PURPLE):
    a, b = camera.world_to_screen(edge)
    offset = int(2 * camera.scale)  # pixels of separation
    # Calculate direction vector
    (ax, ay), (bx, by) = a, b
    dx, dy = bx - ax, by - ay
    distance = (dx**2 + dy**2) ** 0.5
    if distance != 0:
        # Perpendicular vector (normalized)
        perp_x = -dy / distance
        perp_y = dx / distance
    else:
        perp_x = perp_y = 0

    # Offset both lines in opposite perpendicular directions
    edge1 = Edge(
        Position(ax + perp_x * offset, ay + perp_y * offset),
        Position(bx + perp_x * offset, by + perp_y * offset)
    )
    edge1 = camera.screen_to_world(edge1)
    pygame.draw.aaline(surface, color, tuple(camera.world_to_screen(edge1.a)), tuple(camera.world_to_screen(edge1.b)), max(1, 2*int(camera.scale)))  # Draw platform line
    edge2 = Edge(
        Position(ax - perp_x * offset, ay - perp_y * offset),
        Position(bx - perp_x * offset, by - perp_y * offset)
    )
    edge2 = camera.screen_to_world(edge2)
    pygame.draw.aaline(surface, color, tuple(camera.world_to_screen(edge2.a)), tuple(camera.world_to_screen(edge2.b)), max(1, 2*int(camera.scale)))  # Draw platform line


def draw_occupied_edge(surface: pygame.Surface, a: Position, b: Position, camera: Camera, color: tuple[int, int, int], edge_progress: float = 0.0, is_first: bool = False, is_last: bool = False) -> None:
    a = camera.world_to_screen(a)
    b = camera.world_to_screen(b)
    (a_x, a_y), (b_x, b_y) = a, b
    dx = b_x - a_x
    dy = b_y - a_y
    
    if not is_last:
        dash_start_x = a_x + (dx * max((edge_progress-0.5), 0))
        dash_start_y = a_y + (dy * max((edge_progress-0.5), 0))
        dash_end_x = a_x + (dx * (edge_progress))
        dash_end_y = a_y + (dy * (edge_progress))
        pygame.draw.aaline(surface, color, (int(dash_start_x), int(dash_start_y)), (int(dash_end_x), int(dash_end_y)), max(1, 2*int(camera.scale)))

    if edge_progress < 0.5 and not is_first:
        dash_start_x = a_x + (dx * min((edge_progress+0.5), 1))
        dash_start_y = a_y + (dy * min((edge_progress+0.5), 1))
        dash_end_x = a_x + dx
        dash_end_y = a_y + dy        
        pygame.draw.aaline(surface, color, (int(dash_start_x), int(dash_start_y)), (int(dash_end_x), int(dash_end_y)), max(1, 2*int(camera.scale)))