import pygame

from ui.core.ui_component import BaseUIComponent

    
class RectangleUIComponent(BaseUIComponent):
    handled_events = [pygame.MOUSEBUTTONDOWN]
    """A rectangular UI element defined by a pygame.Rect."""
    def __init__(self, rect: pygame.Rect, surface: pygame.Surface):
        self._rect = rect
        self._surface = surface