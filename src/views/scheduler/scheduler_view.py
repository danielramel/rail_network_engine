from models.geometry.position import Position
from ui.components.base import BaseUIComponent
from config.colors import WHITE
import pygame

class SchedulerView(BaseUIComponent):
    def __init__(self, map, screen):
        self._surface = screen
        self._map = map
        
    def render(self, screen_pos: Position | None) -> None:
        for i, station in enumerate(self._map.stations):
            print(station.name  + " at " + str(station.position))
            font = pygame.font.SysFont(None, 24)
            text_surface = font.render(station.name, True, WHITE)
            x = 300
            y = 300 + i * 30
            self._surface.blit(text_surface, (x, y))
            
        # Draw a huge rectangle in the middle of the screen
        surface_width, surface_height = self._surface.get_size()
        rect_width, rect_height = surface_width // 2, surface_height // 2
        rect_x = (surface_width - rect_width) // 2
        rect_y = (surface_height - rect_height) // 2
        rect_color = (200, 200, 200)  # Light gray
        pygame.draw.rect(self._surface, rect_color, (rect_x, rect_y, rect_width, rect_height))