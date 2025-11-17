from core.config.color import Color
from core.models.geometry.position import Position
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from shared.ui.models.rectangle import RectangleUIComponent
import pygame

class Panel(RectangleUIComponent, ClickableUIComponent):
    def __init__(self, surface: pygame.Surface, rect: pygame.Rect = None):
        self._surface = surface
        self._rect = rect if rect is not None else self._get_panel_rect()
                
        self.padding: int = 15
        self.title_font = pygame.font.SysFont(None, 28)
        self.instruction_font = pygame.font.SysFont(None, 22)
        # cannot call super method because _surface needs to be set first
        
    def _get_panel_rect(self) -> pygame.Rect:
        panel_width = 400
        panel_height = 160
        
        screen_width, screen_height = self._surface.get_size()
        panel_x = (screen_width - panel_width) // 2
        panel_y = screen_height - panel_height - 15
        
        return pygame.Rect(panel_x, panel_y, panel_width, panel_height)
    
    def render(self, screen_pos: Position) -> None:
        pygame.draw.rect(self._surface, Color.BLACK, self._rect, border_radius=8)
        pygame.draw.rect(self._surface, Color.WHITE, self._rect, 2, border_radius=8)