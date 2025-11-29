from typing import Callable
from core.models.geometry.position import Position
from shared.ui.models.button import Button
from core.models.event import Event
from core.config.color import Color
import pygame
import tkinter as tk
from tkinter import messagebox

class EndSimulationButton(Button):
    def __init__(self, screen: pygame.Surface, on_end: Callable):
        self._on_end = on_end
        rect = self._get_rect(screen)
        super().__init__(rect, screen)

    def render(self, screen_pos: Position) -> None:
        hovered = self.contains(screen_pos)
        bg_color = Color.DARKGREY if hovered else Color.BLACK
        border_color = Color.LIGHTGREY if hovered else Color.WHITE
        pygame.draw.rect(self._screen, bg_color, self._rect, border_radius=8)
        pygame.draw.rect(self._screen, border_color, self._rect, 2, border_radius=8)
        font = pygame.font.Font(None, 24)
        text = font.render("End", True, Color.WHITE)
        text_rect = text.get_rect(center=self._rect.center)
        self._screen.blit(text, text_rect)

    def _on_click(self, click: Event) -> None:
        if click.is_right_click:
            return
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
        width, height = 80, 40
        x = 10
        y = screen.get_height() - height - 10
        return pygame.Rect(x, y, width, height)