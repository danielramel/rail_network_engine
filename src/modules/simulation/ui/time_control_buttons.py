import pygame
from core.graphics.icon_loader import IconLoader
from core.models.geometry.position import Position
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from core.config.color import Color
from core.config.paths import ICON_PATHS
from core.config.settings import Settings
from core.config.keyboard_shortcuts import TIME_CONTROL_KEYS
from modules.simulation.models.simulation_state import TimeControlMode, TimeControlState
from core.models.event import Event
from shared.ui.models.shortcut_ui_component import ShortcutUIComponent


class TimeControlButtons(ClickableUIComponent, ShortcutUIComponent):
    handled_events = [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL, pygame.KEYDOWN]
    def __init__(self, time_control: TimeControlState, surface: pygame.Surface):
        self.icon_cache = {
            mode: IconLoader().get_icon(ICON_PATHS[mode.name], Settings.BUTTON_SIZE)
            for mode in TimeControlMode
        }
        self.buttons = self._get_buttons(surface)
        self.time_control_state = time_control
        self._surface = surface
        
        self._shortcuts = {
            (key, False): lambda mode=mode: self.set_time_control_mode(mode)
            for key, mode in TIME_CONTROL_KEYS.items()
        }
            
    def set_time_control_mode(self, mode: TimeControlMode | str):
        if mode == "toggle_pause":
            self.time_control_state.toggle_pause()
        else:
            self.time_control_state.switch_mode(mode)
        
        
    def _on_click(self, event: Event) -> bool:          
        for mode, btn in self.buttons:
            if btn.collidepoint(*event.screen_pos):
                if event.is_left_click:
                    self.time_control_state.mode = mode
                return True
        return False

    def render(self, screen_pos: Position) -> None:
        for mode, btn_rect in self.buttons:
        # Draw a solid background for the button (not transparent)
            pygame.draw.rect(self._surface, Color.BLACK, btn_rect, border_radius=10)

            icon = self.icon_cache[mode]
            icon_rect = icon.get_rect(center=btn_rect.center)
            self._surface.blit(icon, icon_rect)

            if mode == self.time_control_state.mode:
                pygame.draw.rect(self._surface, Color.GREEN, btn_rect, 2, border_radius=10)
            else:
                pygame.draw.rect(self._surface, Color.WHITE, btn_rect, 2, border_radius=10)

    def contains(self, screen_pos: Position) -> bool:
        return any(btn.collidepoint(*screen_pos) for _, btn in self.buttons)


    def _get_buttons(self, surface: pygame.Surface) -> list[tuple[TimeControlMode, pygame.Rect]]:
        button_margin = Settings.BUTTON_SIZE // 5
        w, h = surface.get_size()
        buttons = []
        for i, mode in enumerate(TimeControlMode):
            offset = (Settings.BUTTON_SIZE + button_margin) * i
            rect = pygame.Rect(
                (w - (4*Settings.BUTTON_SIZE+3*button_margin))//2 + offset,
                h - Settings.BUTTON_SIZE - button_margin,
                Settings.BUTTON_SIZE,
                Settings.BUTTON_SIZE
            )
            buttons.append((mode, rect))
        return buttons