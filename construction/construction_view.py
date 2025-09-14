# construction/view.py
import pygame

from .ui_helpers import get_zoom_box, get_construction_buttons
from colors import *
from core_funcs import find_path
from construction.state import ConstructionState
from .geometry_utils import snap_to_grid, snap_to_axis
from constants import GRID_SIZE

def render_construction_view(surface, camera, network, state: ConstructionState):
    # Draw grid (assume draw_grid defined elsewhere)
    draw_grid(surface, camera)

    # Draw all rails
    for segment in network.segments:
        screen_points = [camera.world_to_screen(p.x, p.y) for p in segment.points]
        if len(screen_points) >= 2:
            pygame.draw.lines(surface, WHITE, False, screen_points, max(1, int(5 * camera.scale)))

    # Draw nodes
    for node in network.nodes.values():
        screen_x, screen_y = camera.world_to_screen(node.pos.x, node.pos.y)
        outer_radius = max(2, int(6 * camera.scale))
        inner_radius = max(1, int(3 * camera.scale))
        pygame.draw.circle(surface, WHITE, (int(screen_x), int(screen_y)), outer_radius)
        pygame.draw.circle(surface, BLACK, (int(screen_x), int(screen_y)), inner_radius)

    # Draw preview polyline
    if state.selected_mode.name == "RAIL" and state.rail_construction_points:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        world_x, world_y = camera.screen_to_world(mouse_x, mouse_y)
        snapped = snap_to_grid(world_x, world_y)
        preview_points = state.rail_construction_points[:]
        if preview_points:
            snapped_to_axis = snap_to_axis(preview_points[-1], snapped)
            found_path = find_path(preview_points[-1], snapped_to_axis)
            preview_points.extend(found_path[1:])
        screen_points = [camera.world_to_screen(pt.x, pt.y) for pt in preview_points]
        if len(screen_points) >= 2:
            pygame.draw.lines(surface, GRAY, False, screen_points, max(1, int(3 * camera.scale)))

    # Draw buttons
    font = pygame.font.SysFont(None, 40)
    for mode, rect in get_construction_buttons(surface):
        color = GREEN if state.selected_mode == mode else GRAY
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