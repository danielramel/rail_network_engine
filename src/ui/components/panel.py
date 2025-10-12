from config.colors import BLACK, WHITE
from models.geometry.position import Position
from ui.components.rectangle import RectangleUIComponent
import pygame

class Panel(RectangleUIComponent):
    handled_events = [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL]
    def __init__(self, surface: pygame.Surface):
        self._surface = surface
        self._rect = self._get_panel_rect()
        
        # cannot call super method because _surface needs to be set first
        
        
    def _get_panel_rect(self) -> pygame.Rect:
        """Calculate and return the rectangle for the panel."""
        # Panel dimensions
        panel_width = 400
        panel_height = 120
        
        # Position in middle bottom
        screen_width, screen_height = self._surface.get_size()
        panel_x = (screen_width - panel_width) // 2
        panel_y = screen_height - panel_height - 15
        
        return pygame.Rect(panel_x, panel_y, panel_width, panel_height)
    
    def render(self, screen_pos: Position) -> None:
        """Draw a construction information panel in the middle bottom of the screen"""
        pygame.draw.rect(self._surface, BLACK, self._rect, border_radius=8)
        pygame.draw.rect(self._surface, WHITE, self._rect, 2, border_radius=8)