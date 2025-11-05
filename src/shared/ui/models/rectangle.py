import pygame

from models.geometry.position import Position
from ui.models.ui_component import UIComponent

    
class RectangleUIComponent(UIComponent):
    handled_events = [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEWHEEL]
    """A rectangular UI element defined by a pygame.Rect."""
    def __init__(self, rect: pygame.Rect, surface: pygame.Surface):
        self._rect = rect
        self._surface = surface
        
    def contains(self, screen_pos: Position) -> bool:
        return self._rect.collidepoint(*screen_pos)
    
    def process_event(self, event):
        return self._rect.collidepoint(*event.screen_pos)