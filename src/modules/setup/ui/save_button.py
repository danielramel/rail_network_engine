from typing import Callable
import pygame
from core.config.paths import ICON_PATHS
from core.models.railway.railway_system import RailwaySystem
from core.graphics.icon_loader import IconLoader
from core.models.geometry.position import Position
from core.config.color import Color
from core.config.settings import Config
from shared.ui.models.shortcut_ui_component import ShortcutUIComponent
from core.models.event import Event
from shared.ui.models.button import Button


class SaveButton(ShortcutUIComponent, Button):
    _save_timestamp: int = -5000
    def __init__(self, screen: pygame.Surface, railway: RailwaySystem, on_save: Callable) -> None:
        w, h = screen.get_size()
        rect = pygame.Rect(10, h - 2*(Config.BUTTON_SIZE + 10), Config.BUTTON_SIZE, Config.BUTTON_SIZE)
        super().__init__(rect, screen)
        self._icon = IconLoader().get_icon(ICON_PATHS["SAVE"], Config.BUTTON_SIZE)
        self._saved_icon = IconLoader().get_icon(ICON_PATHS["SAVED"], Config.BUTTON_SIZE)
        self._unsaved_icon = IconLoader().get_icon(ICON_PATHS["UNSAVED"], Config.BUTTON_SIZE)
        self._on_save = on_save
        self._railway = railway
        self._shortcuts = {
            (pygame.K_s, True): self._on_shortcut
        }
        
    def _on_click(self, event: Event) -> bool:        
        if event.is_left_click:
            saved =self._on_save(dialog=True)
            if saved:
                self._save_timestamp = pygame.time.get_ticks()
                
    def _on_shortcut(self) -> bool:
        saved = self._on_save(dialog=False)
        if saved:
            self._save_timestamp = pygame.time.get_ticks()
            

    def render(self, screen_pos: Position) -> None:
        bg_color = Color.DARKGREY if self.contains(screen_pos) else Color.BLACK
        pygame.draw.rect(self._screen, bg_color, self._rect, border_radius=10)
        current_time = pygame.time.get_ticks()
        
        # Show saved icon briefly after save, then show state-based icon
        if current_time - self._save_timestamp < 3000:  # 3 seconds after save
            icon = self._saved_icon
        elif self._railway.is_saved:
            icon = self._icon
        else:
            icon = self._unsaved_icon
        
        icon_rect = icon.get_rect(center=self._rect.center)
        self._screen.blit(icon, icon_rect)
        pygame.draw.rect(self._screen, Color.WHITE, self._rect, 2, border_radius=10)