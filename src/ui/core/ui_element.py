from abc import ABC, abstractmethod
from models.geometry.position import Position
from typing import Any
import pygame

class UIElement(ABC):
    """Minimal UI contract: every element must be drawable."""

    @abstractmethod
    def contains(self, pos: Position) -> bool:
        """Check if the given position is within this UI element."""
        
    def handle_click(self, pos: Position, *args: Any) -> bool:
        """Default: not clickable."""
        return False
    
    @abstractmethod
    def draw(self, *args: Any) -> None:
        """Draw this UI element."""
    
    
class RectangleUIElement(UIElement):
    """A rectangular UI element defined by a pygame.Rect."""
    def __init__(self, rect: pygame.Rect, surface: pygame.Surface):
        self._rect = rect
        self._surface = surface
        self.is_visible = True

    def handle_click(self, pos: Position, *args: Any) -> bool:
        """Default: not clickable."""
        return False
    
    def contains(self, pos: Position) -> bool:
        if not self.is_visible:
            return False
        return self._rect.collidepoint(*pos)