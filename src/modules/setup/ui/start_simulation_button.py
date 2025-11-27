from typing import Callable
from core.models.geometry.position import Position
from shared.ui.models.button import Button
from core.models.event import Event
from core.config.color import Color
import pygame

class StartSimulationButton(Button):
    def __init__(self, screen: pygame.Surface, on_start: Callable):
        self._on_start = on_start
        rect = self._get_rect(screen)
        super().__init__(rect, screen)

    def render(self, screen_pos: Position) -> None:
        bg_color = Color.DARKGREY if self.contains(screen_pos) else Color.BLACK
        pygame.draw.rect(self._screen, bg_color, self._rect, border_radius=8)
        pygame.draw.rect(self._screen, Color.WHITE, self._rect, 2, border_radius=8)
        font = pygame.font.Font(None, 24)
        text = font.render("Start", True, Color.WHITE)
        text_rect = text.get_rect(center=self._rect.center)
        self._screen.blit(text, text_rect)

    def _on_click(self, click: Event) -> None:
        self._on_start()
        
    def _get_rect(self, screen: pygame.Surface) -> pygame.Rect:
        width, height = 150, 40
        x = (screen.get_width() - width) // 2
        y = 10
        return pygame.Rect(x, y, width, height)