import pygame

from graphics.camera import Camera
from models.position import Position
from ui_elements.draw_utils import draw_station
from models.map import RailMap
from ui_elements import get_zoom_box, get_construction_buttons, draw_node, draw_signal

from config.colors import PURPLE, RED, WHITE, GRAY, GREEN, YELLOW
from config.settings import GRID_SIZE
from models.construction import ConstructionState
from .signal import render_signal_preview
from .station import render_station_preview
from .rail import render_rail_preview
from .bulldoze import render_bulldoze_preview
from .platform import render_platform_preview
from models.construction import ConstructionMode


def render_construction_preview(surface: pygame.Surface, camera: Camera, map: RailMap, state: ConstructionState):
    draw_grid(surface, camera)

    # Draw all rails
    for edge in map.get_edges():
        pygame.draw.aaline(surface, WHITE, tuple(camera.world_to_screen(edge[0])), tuple(camera.world_to_screen(edge[1])))
        
    # Draw nodes
    for node in map.get_intersections():
        draw_node(surface, camera, node)
        
    for signal in map.get_signals():
        draw_signal(surface, camera, signal)
        
    for pos, name in map.stations.items():
        draw_station(surface, camera, pos, name)

    for edge in map.get_platforms().keys():
        pygame.draw.aaline(surface, PURPLE, tuple(camera.world_to_screen(edge[0])), tuple(camera.world_to_screen(edge[1])))

    pos = Position(*pygame.mouse.get_pos())
    if state.Mode == ConstructionMode.RAIL:
        render_rail_preview(surface, camera, state, map, pos)
    elif state.Mode == ConstructionMode.SIGNAL:
        render_signal_preview(surface, camera, state, map, pos)
    elif state.Mode == ConstructionMode.STATION:
        render_station_preview(surface, camera, state, map, pos)
    elif state.Mode == ConstructionMode.PLATFORM:
        render_platform_preview(surface, camera, state, map, pos)
    elif state.Mode == ConstructionMode.BULLDOZE:
        render_bulldoze_preview(surface, camera, state, map, pos)
        
    draw_construction_buttons(surface, state)
    draw_zoom_indicator(surface, camera)


    


def draw_grid(surface, camera):
    """Draw grid lines with camera transform"""
    w, h = surface.get_size()
    
    # Calculate world bounds visible on screen
    world_left, world_top = camera.screen_to_world(Position(0, 0))
    world_right, world_bottom = camera.screen_to_world(Position(w, h))

    # Calculate grid line positions
    start_x = int(world_left // GRID_SIZE) * GRID_SIZE
    start_y = int(world_top // GRID_SIZE) * GRID_SIZE
    
    # Draw vertical grid lines
    x = start_x
    while x <= world_right + GRID_SIZE:
        screen_x, _ = camera.world_to_screen(Position(x, 0))
        if 0 <= screen_x <= w:
            pygame.draw.aaline(surface, (40, 40, 40), (screen_x, 0), (screen_x, h))
        x += GRID_SIZE
    
    # Draw horizontal grid lines
    y = start_y
    while y <= world_bottom + GRID_SIZE:
        _, screen_y = camera.world_to_screen(Position(0, y))
        if 0 <= screen_y <= h:
            pygame.draw.aaline(surface, (60, 60, 60), (0, screen_y), (w, screen_y))
        y += GRID_SIZE
        
        
def draw_construction_buttons(surface, state):
    font = pygame.font.SysFont(None, 40)
    for mode, rect in get_construction_buttons(surface):
        if state.Mode is ConstructionMode.BULLDOZE and mode is ConstructionMode.BULLDOZE:
            color = RED
        elif state.Mode is mode:
            color = YELLOW
        else:
            color = GRAY
        pygame.draw.rect(surface, color, rect, border_radius=8)
        text = font.render(mode.name[0], True, WHITE)
        surface.blit(text, text.get_rect(center=rect.center))

def draw_zoom_indicator(surface, camera):
    if camera.scale != 1.0 or camera.x != 0 or camera.y != 0:
        zoom_text = f"{int(camera.scale * 100)}%"
        zoom_font = pygame.font.SysFont(None, 24)
        zoom_surface = zoom_font.render(zoom_text, True, WHITE)
        zoom_box = get_zoom_box(surface)
        pygame.draw.rect(surface, (50, 50, 50), zoom_box, border_radius=4)
        pygame.draw.rect(surface, (150, 150, 150), zoom_box, 2, border_radius=4)
        surface.blit(zoom_surface, zoom_surface.get_rect(center=zoom_box.center))
