import pygame
from core.config.colors import GREEN, LIME, PURPLE, LIGHTBLUE, RED, WHITE, BLACK, YELLOW

from core.config.settings import GRID_SIZE, STATION_RECT_SIZE
from core.graphics.camera import Camera
from core.models.geometry import Position, Pose
from core.models.geometry.edge import Edge
from core.models.edge_action import EdgeAction
from shared.ui.utils.draw_line import draw_dotted_line
from shared.ui.services.color_from_speed import color_from_speed

        
def draw_track(surface: pygame.Surface, edge: Edge, camera: Camera, edge_type: EdgeAction, length: int, speed: int = None):   
    if edge_type in (EdgeAction.BULLDOZE, EdgeAction.INVALID_PLATFORM):
        draw_edge(surface, edge, camera, color=RED, length=length)
    elif edge_type == EdgeAction.PLATFORM_SELECTED:
        draw_platform(surface, edge, camera, length=length, color=LIGHTBLUE)
    elif edge_type == EdgeAction.PLATFORM:
        draw_platform(surface, edge, camera, length=length, color=PURPLE)
    elif edge_type == EdgeAction.LOCKED_PLATFORM:
        draw_edge(surface, edge, camera, color=PURPLE, length=length)
        draw_platform(surface, edge, camera, length=length, color=LIME)
    elif edge_type == EdgeAction.LOCKED_PREVIEW:
        draw_edge(surface, edge, camera, color=GREEN, length=length)
    elif edge_type == EdgeAction.LOCKED:
        draw_edge(surface, edge, camera, color=LIME, length=length)
    elif edge_type == EdgeAction.NORMAL:
        draw_edge(surface, edge, camera, color=WHITE, length=length)
    elif edge_type == EdgeAction.SPEED:
        color = color_from_speed(speed)
        draw_edge(surface, edge, camera, color=color, length=length)

def draw_edge(surface: pygame.Surface, edge: Edge, camera: Camera, color: tuple[int, int, int], length: int) -> None:
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
    draw_edge(surface, edge1, camera, color=color, length=length)  # Draw main track line
    edge2 = Edge(
        Position(ax - perp_x * offset, ay - perp_y * offset),
        Position(bx - perp_x * offset, by - perp_y * offset)
    )
    edge2 = camera.screen_to_world(edge2)
    draw_edge(surface, edge2, camera, color=color, length=length)  # Draw platform line