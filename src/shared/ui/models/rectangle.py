import pygame

from core.models.geometry.position import Position
from shared.ui.models.ui_component import UIComponent
    
class RectangleUIComponent(UIComponent):
    """A rectangular UI element defined by a pygame.Rect."""
    def __init__(self, rect: pygame.Rect, screen: pygame.Surface):
        self._rect = rect
        self._screen = screen
        
    def contains(self, screen_pos: Position) -> bool:
        return self._rect.collidepoint(*screen_pos)