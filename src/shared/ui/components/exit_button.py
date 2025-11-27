from typing import Callable
import pygame
from core.config.paths import ICON_PATHS
from core.graphics.icon_loader import IconLoader
from core.models.geometry.position import Position
from core.config.color import Color
from core.config.settings import Config
from core.models.railway.railway_system import RailwaySystem
from shared.ui.components.save_button import SaveButton
from shared.ui.models.shortcut_ui_component import ShortcutUIComponent
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from shared.ui.models.rectangle_ui_component import RectangleUIComponent
from core.models.event import Event
from core.graphics.graphics_context import GraphicsContext
from tkinter import messagebox


class ExitButton(ShortcutUIComponent, RectangleUIComponent, ClickableUIComponent):
    def __init__(self, railway: RailwaySystem, graphics: GraphicsContext, on_exit: Callable, save_button: 'SaveButton'):
        w, h = graphics.screen.get_size()
        rect = pygame.Rect(10, h - Config.BUTTON_SIZE - 10, Config.BUTTON_SIZE, Config.BUTTON_SIZE)
        super().__init__(rect, graphics.screen)
        self._railway = railway
        self._save_button = save_button
        self._graphics = graphics
        self._icon = IconLoader().get_icon(ICON_PATHS["EXIT"], Config.BUTTON_SIZE)
        self._on_exit = on_exit
        self._shortcuts = {
            (pygame.K_ESCAPE, False): self._handle_exit
        }

    def _on_click(self, event: Event) -> None:
        if event.is_left_click:
            self._handle_exit()

    def _handle_exit(self):
        if not self._railway.is_saved:
            # Show dialog: Save? Don't Save? Cancel?
            result = messagebox.askyesnocancel("Unsaved Changes", 
                "You have unsaved changes. Save before exiting?")
            if result is True:      # Save
                self._save_button.save_game()
                self._on_exit()
            elif result is False:   # Don't Save
                self._on_exit()
            # else: Cancel - do nothing
        else:
            self._on_exit()

    def render(self, screen_pos: Position) -> None:
        bg_color = Color.DARKGREY if self.contains(screen_pos) else Color.BLACK
        pygame.draw.rect(self._screen, bg_color, self._rect, border_radius=10)
        icon_rect = self._icon.get_rect(center=self._rect.center)
        self._screen.blit(self._icon, icon_rect)
        pygame.draw.rect(self._screen, Color.WHITE, self._rect, 2, border_radius=10)