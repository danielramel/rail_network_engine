from typing import Callable
from core.models.geometry.position import Position
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from shared.ui.models.rectangle_ui_component import RectangleUIComponent
from core.models.event import Event
from core.config.color import Color
import pygame
import tkinter as tk
from tkinter import messagebox

class EndSimulationButton(RectangleUIComponent, ClickableUIComponent):
    def __init__(self, screen: pygame.Surface, on_end: Callable):
        self._on_end = on_end
        rect = self._get_rect(screen)
        super().__init__(rect, screen)

    def render(self, screen_pos: Position) -> None:
        pygame.draw.rect(self._screen, Color.BLACK, self._rect, border_radius=8)
        pygame.draw.rect(self._screen, Color.WHITE, self._rect, 2, border_radius=8)
        font = pygame.font.Font(None, 24)
        text = font.render("End", True, Color.WHITE)
        text_rect = text.get_rect(center=self._rect.center)
        self._screen.blit(text, text_rect)

    def _on_click(self, click: Event) -> None:
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askyesno(
            "End Simulation",
            "Are you sure you want to end the simulation?\n\nAll progress will be lost."
        )
        root.destroy()
        if result:
            self._on_end()
        
    def _get_rect(self, screen: pygame.Surface) -> pygame.Rect:
        width, height = 150, 40
        x = (screen.get_width() - width) // 2 - 400
        y = 10
        return pygame.Rect(x, y, width, height)