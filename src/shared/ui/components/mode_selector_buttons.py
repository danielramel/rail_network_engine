import pygame
from core.graphics.graphics_context import GraphicsContext
from core.graphics.icon_loader import IconLoader
from core.models.geometry.position import Position
from core.models.app_state import AppState, ViewMode
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from shared.ui.models.shortcut_ui_component import ShortcutUIComponent
from core.config.color import Color
from core.config.paths import ICON_PATHS
from core.config.settings import Config
from core.models.event import Event
from core.config.keyboard_shortcuts import MODE_SELECTION


class ModeSelectorButtons(ShortcutUIComponent, ClickableUIComponent):
    def __init__(self, graphics: GraphicsContext, app_state: AppState):
        self.icon_cache = {
            mode: IconLoader().get_icon(ICON_PATHS[mode.name], Config.BUTTON_SIZE)
            for mode in ViewMode
        }
        self._buttons = self._get_buttons(graphics.screen)
        self._state = app_state
        self._screen = graphics.screen
        self._alert_component = graphics.alert_component
        
        self._shortcuts = {
            (key, False): lambda mode=mode: self._state.switch_mode(mode)
            for key, mode in MODE_SELECTION.items()
        }
        
        
    def _on_click(self, event: Event) -> bool:
        if not event.is_left_click:
            return False
        for mode, btn in self._buttons:
            if btn.collidepoint(*event.screen_pos):
                self._state.switch_mode(mode)
                return True
        return False        

    def render(self, screen_pos: Position) -> None:
        for mode, btn_rect in self._buttons:
        # Draw a solid background for the button (not transparent)
            pygame.draw.rect(self._screen, Color.BLACK, btn_rect, border_radius=10)

            icon = self.icon_cache[mode]
            icon_rect = icon.get_rect(center=btn_rect.center)
            self._screen.blit(icon, icon_rect)

            if mode == self._state.mode:
                pygame.draw.rect(self._screen, Color.GREEN, btn_rect.inflate(10, 10), 5, border_radius=10)
            else:
                pygame.draw.rect(self._screen, Color.WHITE, btn_rect.inflate(-2, -2), 1, border_radius=10)
                

    def contains(self, screen_pos: Position) -> bool:
        return any(btn.collidepoint(*screen_pos) for _, btn in self._buttons)

    def _get_buttons(self, screen: pygame.Surface) -> list[tuple[ViewMode, pygame.Rect]]:
        button_margin = Config.BUTTON_SIZE // 5
        _, h = screen.get_size()
        buttons = []
        for i, mode in enumerate(ViewMode):
            rect = pygame.Rect(
                button_margin,  # x: margin from the left edge
                button_margin + i * (Config.BUTTON_SIZE + button_margin),  # y: stacked from top with margin
                Config.BUTTON_SIZE,
                Config.BUTTON_SIZE
            )
            buttons.append((mode, rect))
        return buttons