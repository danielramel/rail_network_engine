import pygame
from core.config.color import Color

from core.config.settings import Settings
from core.graphics.camera import Camera
from core.models.geometry import Position
from core.models.geometry.edge import Edge
from shared.ui.enums.edge_action import EdgeAction
from shared.ui.services.color_from_speed import color_from_speed

        
def draw_track(surface: pygame.Surface, world_edge: Edge, camera: Camera, edge_action: EdgeAction, length: int, speed: int = None) -> None:
    screen_edge = camera.world_to_screen(world_edge)
    if edge_action in (EdgeAction.BULLDOZE, EdgeAction.INVALID_PLATFORM):
        draw_rail(surface, screen_edge, camera, color=Color.RED, length=length)
    elif edge_action == EdgeAction.PLATFORM_SELECTED:
        draw_platform(surface, screen_edge, camera, color=Color.LIGHTBLUE)
    elif edge_action == EdgeAction.PLATFORM:
        draw_platform(surface, screen_edge, camera, color=Color.PURPLE)
    elif edge_action == EdgeAction.LOCKED_PLATFORM:
        draw_platform(surface, screen_edge, camera, color=Color.LIME)
    elif edge_action == EdgeAction.LOCKED_PREVIEW:
        draw_rail(surface, screen_edge, camera, color=Color.GREEN, length=length)
    elif edge_action == EdgeAction.LOCKED:
        draw_rail(surface, screen_edge, camera, color=Color.LIME, length=length)
    elif edge_action == EdgeAction.NORMAL:
        draw_rail(surface, screen_edge, camera, color=Color.WHITE, length=length)
    elif edge_action == EdgeAction.SPEED:
        color = color_from_speed(speed)
        draw_rail(surface, screen_edge, camera, color=color, length=length)

def draw_rail(surface: pygame.Surface, edge: Edge, camera: Camera, color: tuple[int, int, int], length: int) -> None:
    """Draw a track as a dotted line on the surface from edge.a to edge.b."""
    if length == Settings.SHORT_SEGMENT_LENGTH:
        pygame.draw.aaline(surface, color, tuple(edge.a), tuple(edge.b), max(1, 2*int(camera.scale)))
    elif length == Settings.LONG_SEGMENT_LENGTH:
        draw_long_track(surface, edge, color=color, width=2*camera.scale)
    else:
        raise NotImplementedError("Edge length drawing not implemented for length:", length)
    
def draw_long_track(surface: pygame.Surface, screen_edge: Edge, color, width: float):
    """Draw a dotted line on the surface from start_pos to end_pos."""
    a, b = screen_edge
    if a == b:
        return
    (x1, y1), (x2, y2) = a, b
    dx = x2 - x1
    dy = y2 - y1
    
    distance = a.distance_to(b)
    num_dots = 6 # will be +1 dots
    dot_spacing = distance / num_dots
    for i in range(0, num_dots + 1):
        dot_x = x1 + (dx * (i * dot_spacing) / distance)
        dot_y = y1 + (dy * (i * dot_spacing) / distance)
        pygame.draw.circle(surface, color, (int(dot_x), int(dot_y)), max(1, width))
        
def draw_platform(surface: pygame.Surface, edge: Edge, camera: Camera, color=Color.PURPLE):
    a, b = edge
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
    pygame.draw.aaline(surface, color, tuple(edge1.a), tuple(edge1.b), max(1, 2*int(camera.scale)))  # Draw platform line
    edge2 = Edge(
        Position(ax - perp_x * offset, ay - perp_y * offset),
        Position(bx - perp_x * offset, by - perp_y * offset)
    )
    pygame.draw.aaline(surface, color, tuple(edge2.a), tuple(edge2.b), max(1, 2*int(camera.scale)))  # Draw platform line