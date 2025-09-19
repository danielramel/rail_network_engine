import pygame

from graphics.camera import Camera
from utils import snap_to_grid
from views.construction.rail import render_rail_construction
from models.network import RailNetwork
from ui_elements import get_zoom_box, get_construction_buttons, draw_node, draw_signal

from config.colors import WHITE, GRAY, GREEN, YELLOW
from config.settings import GRID_SIZE
from models.construction import ConstructionState
from views.construction.signal import render_signal_construction

def render_construction_view(surface: pygame.Surface, camera: Camera, network: RailNetwork, state: ConstructionState):
    draw_grid(surface, camera)

    pos = pygame.mouse.get_pos()
    if state.Mode == ConstructionState.Mode.RAIL:
        render_rail_construction(surface, camera, state, network, pos)
    elif state.Mode == ConstructionState.Mode.SIGNAL:
        render_signal_construction(surface, camera, state, network, pos)
        
    # Draw all rails
    for edge in network.get_edges():
        screen_points = [camera.world_to_screen(p.x, p.y) for p in edge]
        pygame.draw.lines(surface, WHITE, False, screen_points, max(1, int(5 * camera.scale)))
        
    # Draw nodes
    for node in network.get_intersections():
        draw_node(surface, camera, node)
        
    # Draw signals as triangles
    for signal in network.get_signals():
        draw_signal(surface, camera, signal)


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
            pygame.draw.line(surface, (40, 40, 40), (screen_x, 0), (screen_x, h))
        x += GRID_SIZE
    
    # Draw horizontal grid lines
    y = start_y
    while y <= world_bottom + GRID_SIZE:
        _, screen_y = camera.world_to_screen(0, y)
        if 0 <= screen_y <= h:
            pygame.draw.line(surface, (60, 60, 60), (0, screen_y), (w, screen_y))
        y += GRID_SIZE