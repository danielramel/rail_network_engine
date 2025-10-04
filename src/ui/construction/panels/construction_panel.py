from models.construction import ConstructionMode
from ui.core.ui_element import RectangleUIElement
import pygame
from config.colors import BLACK, WHITE
from .rail_panel_content import RailPanelContent

class ConstructionPanel(RectangleUIElement):        
    def __init__(self, surface: pygame.Surface, state: dict):
        self._surface = surface
        self._state = state
        self._rect = self._get_panel_rect()
        self._panels = {
            ConstructionMode.RAIL: RailPanelContent(self._surface, self._rect),
        }

    def draw(self) -> None:
        if not self.is_visible:
            return
        """Draw a construction information panel in the middle bottom of the screen"""
        pygame.draw.rect(self._surface, BLACK, self._rect, border_radius=8)
        pygame.draw.rect(self._surface, WHITE, self._rect, 2, border_radius=8)

        # Draw the content using the context drawer
        content_drawer = self._panels.get(self._state.mode)
        if content_drawer:
            content_drawer.draw(self._state.mode_info)
            
    def handle_click(self, pos) -> bool:
        if self._state.mode not in self._panels:
            return False
        return self._panels.get(self._state.mode).handle_click(pos, self._state.mode_info)

    @property
    def is_visible(self) -> bool:
        return self._state.mode in self._panels
    
    
    def _get_panel_rect(self) -> pygame.Rect:
        # Panel dimensions
        panel_width = 400
        panel_height = 120
        
        # Position in middle bottom
        screen_width, screen_height = self._surface.get_size()
        panel_x = (screen_width - panel_width) // 2
        panel_y = screen_height - panel_height - 15
        
        return pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        
        

    