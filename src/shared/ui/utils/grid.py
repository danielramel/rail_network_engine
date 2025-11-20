
from core.models.geometry.position import Position
import pygame
from core.config.settings import Settings
from core.graphics.camera import Camera

def draw_grid(surface: pygame.Surface, camera: Camera):
    """Draw grid lines with camera transform"""
    w, h = surface.get_size()
    
    # Calculate world bounds visible on screen
    world_left, world_top = camera.screen_to_world(Position(0, 0))
    world_right, world_bottom = camera.screen_to_world(Position(w, h))

    # Calculate grid line positions
    start_x = int(world_left // Settings.GRID_SIZE) * Settings.GRID_SIZE
    start_y = int(world_top // Settings.GRID_SIZE) * Settings.GRID_SIZE
    
    # Draw vertical grid lines
    x = start_x
    while x <= world_right + Settings.GRID_SIZE:
        screen_x, _ = camera.world_to_screen(Position(x, 0))
        if 0 <= screen_x <= w:
            pygame.draw.aaline(surface, (40, 40, 40), (screen_x, 0), (screen_x, h))
        x += Settings.GRID_SIZE
    
    # Draw horizontal grid lines
    y = start_y
    while y <= world_bottom + Settings.GRID_SIZE:
        _, screen_y = camera.world_to_screen(Position(0, y))
        if 0 <= screen_y <= h:
            pygame.draw.aaline(surface, (60, 60, 60), (0, screen_y), (w, screen_y))
        y += Settings.GRID_SIZE