from core.config.color import Color
from core.models.geometry.position import Position
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from shared.ui.models.rectangle import RectangleUIComponent
import pygame

class Panel(RectangleUIComponent, ClickableUIComponent):
    def __init__(self, screen: pygame.Surface, x: int = None, y: int = None, height: int = 160, width: int = 400) -> None:
        self._screen = screen
        self._rect = self._get_panel_rect(x, y, height, width)
                
        self.padding: int = 15
        self.title_font = pygame.font.SysFont(None, 28)
        self.instruction_font = pygame.font.SysFont(None, 22)
        # cannot call super method because _screen needs to be set first
        
    def _get_panel_rect(self, x:int, y:int, height: int, width: int) -> pygame.Rect:
        screen_w, screen_h = self._screen.get_size()
        if x is None:
            x = (screen_w - width) // 2
        elif x < 0:
            x = screen_w + x
            
        if y is None:
            y = screen_h - height - 15
            
        elif y < 0:
            y = screen_h - y
                    
        return pygame.Rect(x, y, width, height)
    
    def render(self, screen_pos: Position) -> None:
        pygame.draw.rect(self._screen, Color.BLACK, self._rect, border_radius=8)
        pygame.draw.rect(self._screen, Color.WHITE, self._rect, 2, border_radius=8)