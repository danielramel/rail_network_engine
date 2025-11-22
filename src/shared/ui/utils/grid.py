
from math import floor
from core.models.geometry.position import Position
import pygame
from core.config.settings import Config
from core.graphics.camera import Camera

def draw_grid(screen: pygame.Surface, camera: Camera):
    """Draw grid lines with camera transform"""
    w, h = screen.get_size()
    
    # Calculate world bounds visible on screen
    world_left, world_top = camera.screen_to_world(Position(0, 0))
    world_right, world_bottom = camera.screen_to_world(Position(w, h))

    # Calculate grid line positions
    start_x = floor(world_left)
    start_y = floor(world_top)
    
    # Draw vertical grid lines
    x = start_x
    while x <= world_right + 1:
        screen_x, _ = camera.world_to_screen(Position(x, 0))
        if 0 <= screen_x <= w:
            pygame.draw.aaline(screen, (40, 40, 40), (screen_x, 0), (screen_x, h))
        x += 1
    
    # Draw horizontal grid lines
    y = start_y
    while y <= world_bottom + 1:
        _, screen_y = camera.world_to_screen(Position(0, y))
        if 0 <= screen_y <= h:
            pygame.draw.aaline(screen, (60, 60, 60), (0, screen_y), (w, screen_y))
        y += 1