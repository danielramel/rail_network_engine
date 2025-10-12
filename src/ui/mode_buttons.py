import pygame
from graphics.icon_loader import IconLoader
from models.geometry.position import Position
from models.app_state import AppState, ViewMode
from ui.components.base import BaseUIComponent
from config.colors import BLACK, GREEN, WHITE, YELLOW, RED
from config.paths import MODE_ICON_PATHS
from config.settings import BUTTON_SIZE


class ModeSelectorButtons(BaseUIComponent):
    handled_events = [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL]
    def __init__(self, surface: pygame.Surface, app_state: AppState):
        self.icon_cache = {
            mode: IconLoader().get_icon(MODE_ICON_PATHS[mode.name], BUTTON_SIZE)
            for mode in ViewMode
        }
        self.buttons = self._get_buttons(surface)
        self.state = app_state
        self._surface = surface
        
        
    def handle_event(self, event: pygame.event) -> bool:
        for mode, btn in self.buttons:
            if btn.collidepoint(*event.pos_):
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.state.current_mode = mode
                return True
        return False

    def render(self, screen_pos: Position) -> None:
        for mode, btn_rect in self.buttons:
        # Draw a solid background for the button (not transparent)
            pygame.draw.rect(self._surface, BLACK, btn_rect, border_radius=10)

            icon = self.icon_cache[mode]
            icon_rect = icon.get_rect(center=btn_rect.center)
            self._surface.blit(icon, icon_rect)

            if mode == self.state.current_mode:
                color = GREEN
                pygame.draw.rect(self._surface, color, btn_rect, 2, border_radius=10)
            else:
                pygame.draw.rect(self._surface, WHITE, btn_rect, 2, border_radius=10)

    def contains(self, screen_pos: Position) -> bool:
        return any(btn.collidepoint(*screen_pos) for _, btn in self.buttons)

    def _get_buttons(self, surface: pygame.Surface) -> list[tuple[ViewMode, pygame.Rect]]:
        button_margin = BUTTON_SIZE // 5
        _, h = surface.get_size()
        buttons = []
        for i, mode in enumerate(ViewMode):
            rect = pygame.Rect(
                button_margin,  # x: margin from the left edge
                button_margin + i * (BUTTON_SIZE + button_margin),  # y: stacked from top with margin
                BUTTON_SIZE,
                BUTTON_SIZE
            )
            buttons.append((mode, rect))
        return buttons