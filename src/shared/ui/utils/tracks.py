import pygame
from core.config.color import Color

from core.graphics.camera import Camera
from core.models.geometry import Position
from core.models.geometry.edge import Edge
from shared.ui.enums.edge_action import EdgeAction
from shared.ui.services.color_from_speed import color_from_speed
from .lines import draw_dotted_line

        
def draw_track(surface: pygame.Surface, edge: Edge, camera: Camera, edge_action: EdgeAction, length: int, speed: int = None) -> None:   
    if edge_action in (EdgeAction.BULLDOZE, EdgeAction.INVALID_PLATFORM):
        draw_rail(surface, edge, camera, color=Color.RED, length=length)
    elif edge_action == EdgeAction.PLATFORM_SELECTED:
        draw_platform(surface, edge, camera, length=length, color=Color.LIGHTBLUE)
    elif edge_action == EdgeAction.PLATFORM:
        draw_platform(surface, edge, camera, length=length, color=Color.PURPLE)
    elif edge_action == EdgeAction.LOCKED_PLATFORM:
        draw_platform(surface, edge, camera, length=length, color=Color.LIME)
    elif edge_action == EdgeAction.LOCKED_PREVIEW:
        draw_rail(surface, edge, camera, color=Color.GREEN, length=length)
    elif edge_action == EdgeAction.LOCKED:
        draw_rail(surface, edge, camera, color=Color.LIME, length=length)
    elif edge_action == EdgeAction.NORMAL:
        draw_rail(surface, edge, camera, color=Color.WHITE, length=length)
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
        
def draw_platform(surface: pygame.Surface, edge: Edge, camera: Camera, length: int, color=Color.PURPLE):
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