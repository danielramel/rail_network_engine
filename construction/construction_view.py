import pygame

from camera import Camera
from construction.modes import render_rail_construction
from rail_network import RailNetwork

from .ui_helpers import get_zoom_box, get_construction_buttons
from colors import *
from construction.models import ConstructionState
from constants import GRID_SIZE

def render_construction_view(surface, camera: Camera, network: RailNetwork, state: ConstructionState):
    draw_grid(surface, camera)

    # Draw all rails
    for edge in network.get_edges():
        screen_points = [camera.world_to_screen(p.x, p.y) for p in edge]
        pygame.draw.lines(surface, WHITE, False, screen_points, max(1, int(5 * camera.scale)))
        
    # Draw preview polyline
    if state.Mode == ConstructionState.Mode.RAIL:
        render_rail_construction(surface, camera, state, network)

    # Draw nodes
    for node in network.get_intersections():
        screen_x, screen_y = camera.world_to_screen(node.x, node.y)
        outer_radius = max(2, int(6 * camera.scale))
        inner_radius = max(1, int(3 * camera.scale))
        pygame.draw.circle(surface, WHITE, (int(screen_x), int(screen_y)), outer_radius)
        pygame.draw.circle(surface, BLACK, (int(screen_x), int(screen_y)), inner_radius)
        
        
    # Draw signals as triangles
    for signal in network.get_signals():
        screen_x, screen_y = camera.world_to_screen(signal.point.x, signal.point.y)
        size = max(18, int(36 * camera.scale))
        
        # Create triangle surface
        triangle_surf = create_triangle_surface(size, BLACK, WHITE)
        
        # Rotate based on direction
        angle = get_rotation_angle(signal.direction)
        rotated_surf = pygame.transform.rotate(triangle_surf, angle)
        
        # Get rect and center it
        rect = rotated_surf.get_rect(center=(screen_x, screen_y))
        surface.blit(rotated_surf, rect)


    # Draw buttons
    font = pygame.font.SysFont(None, 40)
    for mode, rect in get_construction_buttons(surface):
        color = GREEN if state.Mode == mode else GRAY
        pygame.draw.rect(surface, color, rect, border_radius=8)
        text = font.render(mode.value, True, WHITE)
        surface.blit(text, text.get_rect(center=rect.center))

    # Zoom indicator
    if camera.scale != 1.0 or camera.x != 0 or camera.y != 0:
        zoom_text = f"{int(camera.scale * 100)}%"
        zoom_font = pygame.font.SysFont(None, 24)
        zoom_surface = zoom_font.render(zoom_text, True, WHITE)
        zoom_box = get_zoom_box(surface)
        pygame.draw.rect(surface, (50, 50, 50), zoom_box, border_radius=4)
        pygame.draw.rect(surface, (150, 150, 150), zoom_box, 2, border_radius=4)
        surface.blit(zoom_surface, zoom_surface.get_rect(center=zoom_box.center))



def draw_grid(surface, camera):
    """Draw grid lines with camera transform"""
    w, h = surface.get_size()
    
    # Calculate world bounds visible on screen
    world_left, world_top = camera.screen_to_world(0, 0)
    world_right, world_bottom = camera.screen_to_world(w, h)
    
    # Calculate grid line positions
    start_x = int(world_left // GRID_SIZE) * GRID_SIZE
    start_y = int(world_top // GRID_SIZE) * GRID_SIZE
    
    # Draw vertical grid lines
    x = start_x
    while x <= world_right + GRID_SIZE:
        screen_x, _ = camera.world_to_screen(x, 0)
        if 0 <= screen_x <= w:
            pygame.draw.line(surface, (60, 60, 60), (screen_x, 0), (screen_x, h))
        x += GRID_SIZE
    
    # Draw horizontal grid lines
    y = start_y
    while y <= world_bottom + GRID_SIZE:
        _, screen_y = camera.world_to_screen(0, y)
        if 0 <= screen_y <= h:
            pygame.draw.line(surface, (60, 60, 60), (0, screen_y), (w, screen_y))
        y += GRID_SIZE
        
        
def get_rotation_angle(direction_vector):
    """Convert direction vector to rotation angle in degrees"""
    dx, dy = direction_vector
    angle_map = {
        (0, 1): 0,     # Up
        (1, 1): 45,    # Up-Right
        (1, 0): 90,     # Right
        (1, -1): 135,    # Down-Right
        (0, -1): 180,    # Down
        (-1, -1): 225,   # Down-Left
        (-1, 0): 270,   # Left
        (-1, 1): 315   # Up-Left
    }
    return angle_map.get((dx, dy), 0)

def create_triangle_surface(size, color, outline_color):
    """Create a surface with a pointy upward-facing triangle"""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    h = size // 2
    w = h
    points = [
        (h, 0),           # Top point
        (h - w, size - 1), # Bottom left
        (h + w, size - 1)  # Bottom right
    ]
    pygame.draw.polygon(surf, color, points)
    pygame.draw.polygon(surf, outline_color, points, 2)
    return surf