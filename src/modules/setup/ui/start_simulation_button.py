from typing import Callable
from core.models.geometry.position import Position
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from shared.ui.models.rectangle_ui_component import RectangleUIComponent
from core.models.event import Event
from core.config.color import Color
import pygame

class StartSimulationButton(RectangleUIComponent, ClickableUIComponent):
    def __init__(self, screen: pygame.Surface, on_start: Callable):
        self._on_start = on_start
        rect = self._get_rect(screen)
        super().__init__(rect, screen)

    def render(self, world_pos: Position) -> None:
        pygame.draw.rect(self._screen, Color.BLACK, self._rect, border_radius=8)
        pygame.draw.rect(self._screen, Color.WHITE, self._rect, 2, border_radius=8)
        font = pygame.font.Font(None, 36)
        text = font.render("Start Simulation", True, Color.WHITE)
        text_rect = text.get_rect(center=self._rect.center)
        self._screen.blit(text, text_rect)

    def _on_click(self, click: Event) -> None:
        self._on_start()
        
    def _get_rect(self, screen: pygame.Surface) -> pygame.Rect:
        width, height = 200, 60
        x = (screen.get_width() - width) // 2
        y = 10
        return pygame.Rect(x, y, width, height)