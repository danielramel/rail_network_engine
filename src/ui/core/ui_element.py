from abc import ABC, abstractmethod
from models.geometry.position import Position
from typing import Any
import pygame

class UIElement(ABC):
    """Minimal UI contract: every element must be drawable."""    
    def handle_event(self, pos: Position, *args: Any) -> bool:
        """Default: not clickable."""
        return False
    
    @abstractmethod
    def render(self, *args: Any) -> None:
        """Draw this UI element."""
    
    
class RectangleUIElement(UIElement):
    handled_events = [pygame.MOUSEBUTTONDOWN]
    """A rectangular UI element defined by a pygame.Rect."""
    def __init__(self, rect: pygame.Rect, surface: pygame.Surface):
        self._rect = rect
        self._surface = surface
        self.is_visible = True

    def handle_event(self, pos: Position, *args: Any) -> bool:
        """Default: not clickable."""
        return False
    
    def contains(self, pos: Position) -> bool:
        if not self.is_visible:
            return False
        return self._rect.collidepoint(*pos)