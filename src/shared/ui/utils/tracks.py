import pygame
from core.config.color import Color

from core.config.settings import Config
from core.graphics.camera import Camera
from core.models.geometry.edge import Edge
from core.models.geometry.position import Position
from shared.ui.enums.edge_action import EdgeAction
from shared.ui.services.color_from_speed import color_from_speed

        
def draw_track(screen: pygame.Surface, world_edge: Edge, camera: Camera, edge_action: EdgeAction, length: int, speed: int = None) -> None:
    a, b = camera.world_to_screen_edge(world_edge)
    if edge_action is EdgeAction.BULLDOZE or edge_action is EdgeAction.INVALID_TRAIN_PLACEMENT:
        draw_rail(screen, (a, b), camera, color=Color.RED, length=length, level=world_edge.level)
    elif edge_action is EdgeAction.INVALID_PLATFORM:
        draw_platform(screen, (a, b), camera, color=Color.RED)
    elif edge_action is EdgeAction.PLATFORM_SELECTED:
        draw_platform(screen, (a, b), camera, color=Color.LIGHTBLUE)
    elif edge_action is EdgeAction.PLATFORM:
        draw_platform(screen, (a, b), camera, color=Color.PURPLE)
    elif edge_action is EdgeAction.LOCKED_PLATFORM:
        draw_platform(screen, (a, b), camera, color=Color.LIME)
    elif edge_action is EdgeAction.LOCKED_PREVIEW:
        draw_rail(screen, (a, b), camera, color=Color.GREEN, length=length, level=world_edge.level)
    elif edge_action is EdgeAction.LOCKED:
        draw_rail(screen, (a, b), camera, color=Color.LIME, length=length, level=world_edge.level)
    elif edge_action is EdgeAction.NO_SPEED:
        draw_rail(screen, (a, b), camera, color=Color.WHITE, length=length, level=world_edge.level)
    elif edge_action is EdgeAction.SPEED:
        color = color_from_speed(speed)
        draw_rail(screen, (a, b), camera, color=color, length=length, level=world_edge.level)
            
def draw_rail(screen: pygame.Surface, screen_edge: tuple[Position, Position], camera: Camera, color: tuple[int, int, int], length: int, level: int) -> None:
    if level == 1:
        draw_tunnel(screen, screen_edge, color, length)
        return
    if length == Config.SHORT_SECTION_LENGTH:
        a, b = screen_edge
        pygame.draw.aaline(screen, color, tuple(a), tuple(b), max(1, 2*int(camera.scale)))
    elif length == Config.LONG_SECTION_LENGTH:
        draw_long_track(screen, screen_edge, color=color, width=max(1, 2*int(camera.scale)))
    else:
        raise NotImplementedError("Edge length drawing not implemented for length:", length)
    
def draw_long_track(screen: pygame.Surface, screen_edge: Edge, color, width: int):
    """Draw a dotted line on the screen from start_pos to end_pos."""
    (a_x, a_y), (b_x, b_y) = screen_edge
    dx = b_x - a_x
    dy = b_y - a_y

    dash_start_x = a_x + dx * 0.1
    dash_start_y = a_y + dy * 0.1
    dash_end_x = a_x + dx * 0.4
    dash_end_y = a_y + dy * 0.4

    pygame.draw.aaline(screen, color, (dash_start_x, dash_start_y), (dash_end_x, dash_end_y), width)
    
    dash_start_x = a_x + dx * 0.6
    dash_start_y = a_y + dy * 0.6
    dash_end_x = a_x + dx * 0.9
    dash_end_y = a_y + dy * 0.9

    pygame.draw.aaline(screen, color, (dash_start_x, dash_start_y), (dash_end_x, dash_end_y), width)
    
    
        
def draw_platform(screen: pygame.Surface, screen_edge: tuple[Position, Position], camera: Camera, color=Color.PURPLE):
    a, b = screen_edge
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
    
    
    
    
    
def draw_tunnel(screen: pygame.Surface, screen_edge: tuple[Position, Position], color: tuple[int, int, int], length: int) -> None:
    a, b = screen_edge
    if a == b:
        return
    (x1, y1), (x2, y2) = a, b
    dx = x2 - x1
    dy = y2 - y1
    
    distance = a.distance_to(b)
    num_dots = max(1, int(distance // 30)+3)
    dot_spacing = distance / num_dots
    for i in range(num_dots + 1):
        dot_x = x1 + (dx * (i * dot_spacing) / distance)
        dot_y = y1 + (dy * (i * dot_spacing) / distance)
        pygame.draw.circle(screen, color, (int(dot_x), int(dot_y)), 1)