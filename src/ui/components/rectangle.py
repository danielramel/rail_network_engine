import pygame

from models.geometry.position import Position
from ui.components.base import BaseUIComponent

    
class RectangleUIComponent(BaseUIComponent):
    handled_events = [pygame.MOUSEBUTTONDOWN]
    """A rectangular UI element defined by a pygame.Rect."""
    def __init__(self, rect: pygame.Rect, surface: pygame.Surface):
        self._rect = rect
        self._surface = surface
        
    def contains(self, screen_pos: Position) -> bool:
        return self._rect.collidepoint(*screen_pos)
    
    def handle_event(self, event):
        return self._rect.collidepoint(*event.pos_)