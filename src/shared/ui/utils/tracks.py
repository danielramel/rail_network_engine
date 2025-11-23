import pygame
from core.config.color import Color

from core.config.settings import Config
from core.graphics.camera import Camera
from core.models.geometry.edge import Edge
from core.models.geometry.position import Position
from shared.ui.enums.edge_action import EdgeAction
from shared.ui.services.color_from_speed import color_from_speed

        
def draw_track(screen: pygame.Surface, world_edge: Edge, camera: Camera, edge_action: EdgeAction, length: int, speed: int = None) -> None:
    screen_edge = camera.world_to_screen(world_edge)
    if edge_action is EdgeAction.BULLDOZE:
        draw_rail(screen, screen_edge, camera, color=Color.RED, length=length)
    elif edge_action is EdgeAction.INVALID_PLATFORM:
        draw_platform(screen, screen_edge, camera, color=Color.RED)
    elif edge_action is EdgeAction.PLATFORM_SELECTED:
        draw_platform(screen, screen_edge, camera, color=Color.LIGHTBLUE)
    elif edge_action is EdgeAction.PLATFORM:
        draw_platform(screen, screen_edge, camera, color=Color.PURPLE)
    elif edge_action is EdgeAction.LOCKED_PLATFORM:
        draw_platform(screen, screen_edge, camera, color=Color.LIME)
    elif edge_action is EdgeAction.LOCKED_PREVIEW:
        draw_rail(screen, screen_edge, camera, color=Color.GREEN, length=length)
    elif edge_action is EdgeAction.LOCKED:
        draw_rail(screen, screen_edge, camera, color=Color.LIME, length=length)
    elif edge_action is EdgeAction.NORMAL:
        draw_rail(screen, screen_edge, camera, color=Color.WHITE, length=length)
    elif edge_action is EdgeAction.SPEED:
        color = color_from_speed(speed)
        draw_rail(screen, screen_edge, camera, color=color, length=length)
    elif edge_action is EdgeAction.TUNNEL_SPEED:
        color = color_from_speed(speed)
        draw_tunnel(screen, screen_edge, camera, color=color, length=length)

def draw_rail(screen: pygame.Surface, edge: Edge, camera: Camera, color: tuple[int, int, int], length: int) -> None:
    """Draw a track as a dotted line on the screen from edge.a to edge.b."""
    if length == Config.SHORT_SEGMENT_LENGTH:
        pygame.draw.aaline(screen, color, tuple(edge.a), tuple(edge.b), max(1, 2*int(camera.scale)))
    elif length == Config.LONG_SEGMENT_LENGTH:
        draw_long_track(screen, edge, color=color, width=2*camera.scale)
    else:
        raise NotImplementedError("Edge length drawing not implemented for length:", length)
    
def draw_long_track(screen: pygame.Surface, screen_edge: Edge, color, width: float):
    """Draw a dotted line on the screen from start_pos to end_pos."""
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
        pygame.draw.circle(screen, color, (int(dot_x), int(dot_y)), max(1, width))
        
def draw_platform(screen: pygame.Surface, edge: Edge, camera: Camera, color=Color.PURPLE):
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
    a = Position(ax + perp_x * offset, ay + perp_y * offset)
    b = Position(bx + perp_x * offset, by + perp_y * offset)
    pygame.draw.aaline(screen, color, tuple(a), tuple(b), max(1, 1*int(camera.scale)))  # Draw platform line
    a = Position(ax - perp_x * offset, ay - perp_y * offset)
    b = Position(bx - perp_x * offset, by - perp_y * offset)
    pygame.draw.aaline(screen, color, tuple(a), tuple(b), max(1, 1*int(camera.scale)))  # Draw platform line
    
    
    
    
    
def draw_tunnel(screen: pygame.Surface, screen_edge: Edge, camera: Camera, color: Color, length: int) -> None:
    a, b = screen_edge
    if a == b:
        return
    (x1, y1), (x2, y2) = a, b
    dx = x2 - x1
    dy = y2 - y1
    
    distance = a.distance_to(b)
    num_dots = max(1, int(distance // 10))
    dot_spacing = distance / num_dots
    for i in range(num_dots + 1):
        dot_x = x1 + (dx * (i * dot_spacing) / distance)
        dot_y = y1 + (dy * (i * dot_spacing) / distance)
        pygame.draw.circle(screen, color, (int(dot_x), int(dot_y)), 1)