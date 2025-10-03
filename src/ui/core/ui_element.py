from abc import ABC, abstractmethod
import pygame
from models.geometry.position import Position
from typing import Any

class UIElement(ABC):
    """Minimal UI contract: every element must be drawable."""

    @abstractmethod
    def contains(self, pos: Position) -> bool:
        """Check if the given position is within this UI element."""
        pass

    def handle_click(self, pos: Position, *args: Any) -> bool:
        """Default: not clickable."""
        return False
    
    @abstractmethod
    def draw(self, *args: Any) -> None:
        """Draw this UI element."""
        pass