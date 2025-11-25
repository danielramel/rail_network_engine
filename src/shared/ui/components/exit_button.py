from typing import Callable
import pygame
from core.config.paths import ICON_PATHS
from core.graphics.icon_loader import IconLoader
from core.models.geometry.position import Position
from core.config.color import Color
from core.config.settings import Config
from shared.ui.models.shortcut_ui_component import ShortcutUIComponent
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from shared.ui.models.rectangle import RectangleUIComponent
from core.models.event import Event
from core.graphics.graphics_context import GraphicsContext


class ExitButton(ShortcutUIComponent, RectangleUIComponent, ClickableUIComponent):
    def __init__(self, graphics: GraphicsContext, on_exit: Callable):
        w, h = graphics.screen.get_size()
        rect = pygame.Rect(10, h - Config.BUTTON_SIZE - 10, Config.BUTTON_SIZE, Config.BUTTON_SIZE)
        super().__init__(rect, graphics.screen)
        self._graphics = graphics
        self._icon = IconLoader().get_icon(ICON_PATHS["EXIT"], Config.BUTTON_SIZE)
        self._on_exit = on_exit
        # define shortcut here after method exists
        self._shortcuts = {
            (pygame.K_ESCAPE, True): self._on_exit
        }

    def _on_click(self, event: Event) -> None:
        if event.is_left_click:
            self._on_exit()

    def render(self, screen_pos: Position) -> None:
        pygame.draw.rect(self._screen, Color.BLACK, self._rect, border_radius=10)
        icon_rect = self._icon.get_rect(center=self._rect.center)
        self._screen.blit(self._icon, icon_rect)
        pygame.draw.rect(self._screen, Color.WHITE, self._rect.inflate(-2, -2), 1, border_radius=10)