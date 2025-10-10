from abc import ABC, abstractmethod
import pygame
from models.geometry.position import Position

class UIView(ABC):
    def __init__(self) -> None:
        self.is_visible: bool = True

    @abstractmethod
    def render(self, surface: pygame.Surface, **ctx) -> None:
        """Render the view. `ctx` may contain read-only model objects (camera, theme...)."""

    @property
    @abstractmethod
    def rect(self) -> pygame.Rect:
        """Return bounding rect for hit-testing and layout."""

    def contains(self, pos: Position) -> bool:
        """Default hit-test using rect; respects is_visible."""
        if not self.is_visible:
            return False
        return self.rect.collidepoint(*pos)


class RectangleUIView(UIView):
    """Simple rectangular view; recomputes rect on update_layout."""

    def __init__(self, width: int, height: int, margin_right: int = 20, margin_top: int = 10):
        super().__init__()
        self._width = width
        self._height = height
        self._margin_right = margin_right
        self._margin_top = margin_top
        self._rect = pygame.Rect(0, 0, width, height)

    @abstractmethod
    def render(self, surface: pygame.Surface, **ctx) -> None:
        """Render the view. `ctx` may contain read-only model objects (camera, theme...)."""

    @property
    def rect(self) -> pygame.Rect:
        return self._rect