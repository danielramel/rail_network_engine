import pygame
from core.graphics.icon_loader import IconLoader
from core.models.geometry.position import Position
from shared.ui.models.clickable_component import ClickComponent
from core.config.colors import BLACK, GREEN, WHITE, YELLOW, RED
from core.config.paths import ICON_PATHS
from core.config.settings import BUTTON_SIZE
from core.config.keyboard_shortcuts import TIME_CONTROL_KEYS
from modules.simulation.models.simulation_state import TimeControlMode, TimeControlState
from core.models.event import Event


class TimeControlButtons(ClickComponent):
    handled_events = [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL, pygame.KEYDOWN]
    def __init__(self, time_control: TimeControlState, surface: pygame.Surface):
        self.icon_cache = {
            mode: IconLoader().get_icon(ICON_PATHS[mode.name], BUTTON_SIZE)
            for mode in TimeControlMode
        }
        self.buttons = self._get_buttons(surface)
        self.time_control_state = time_control
        self._surface = surface
        
        
    def process_event(self, event: Event) -> bool:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.time_control_state.mode == TimeControlMode.PAUSE:
                    self.time_control_state.mode = TimeControlMode.PLAY
                else:
                    self.time_control_state.mode = TimeControlMode.PAUSE
                return True
            elif event.key in TIME_CONTROL_KEYS:
                self.time_control_state.mode = TIME_CONTROL_KEYS[event.key]
                return True
            return False
          
        for mode, btn in self.buttons:
            if btn.collidepoint(*event.screen_pos):
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.time_control_state.mode = mode
                return True
        return False

    def render(self, screen_pos: Position) -> None:
        for mode, btn_rect in self.buttons:
        # Draw a solid background for the button (not transparent)
            pygame.draw.rect(self._surface, BLACK, btn_rect, border_radius=10)

            icon = self.icon_cache[mode]
            icon_rect = icon.get_rect(center=btn_rect.center)
            self._surface.blit(icon, icon_rect)

            if mode == self.time_control_state.mode:
                pygame.draw.rect(self._surface, GREEN, btn_rect, 2, border_radius=10)
            else:
                pygame.draw.rect(self._surface, WHITE, btn_rect, 2, border_radius=10)

    def contains(self, screen_pos: Position) -> bool:
        return any(btn.collidepoint(*screen_pos) for _, btn in self.buttons)


    def _get_buttons(self, surface: pygame.Surface) -> list[tuple[TimeControlMode, pygame.Rect]]:
        button_margin = BUTTON_SIZE // 5
        _, h = surface.get_size()
        buttons = []
        for i, mode in enumerate(TimeControlMode):
            offset = (BUTTON_SIZE + button_margin) * i
            rect = pygame.Rect(
                button_margin + offset,
                h - BUTTON_SIZE - button_margin,
                BUTTON_SIZE,
                BUTTON_SIZE
            )
            buttons.append((mode, rect))
        return buttons