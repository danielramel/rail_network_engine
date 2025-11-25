import pygame
from core.config.paths import ICON_PATHS
from core.models.railway.railway_system import RailwaySystem
from core.graphics.icon_loader import IconLoader
from core.models.geometry.position import Position
from core.config.color import Color
from core.config.settings import Config
from shared.ui.models.rectangle import RectangleUIComponent
from shared.ui.models.shortcut_ui_component import ShortcutUIComponent
from core.models.event import Event
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from core.models.app_state import AppState
import json


class SaveButton(ShortcutUIComponent, RectangleUIComponent, ClickableUIComponent):
    _save_timestamp: int = -5000
    def __init__(self, screen: pygame.Surface, railway: RailwaySystem, app_state: AppState) -> None:
        self._icon = IconLoader().get_icon(ICON_PATHS["SAVE"], Config.BUTTON_SIZE)
        self._saved_icon = IconLoader().get_icon(ICON_PATHS["SAVED"], Config.BUTTON_SIZE)
        rect = pygame.Rect(200, Config.BUTTON_SIZE//5, Config.BUTTON_SIZE, Config.BUTTON_SIZE)
        super().__init__(rect, screen)
        self._railway = railway
        self._app_state = app_state
        self._shortcuts = {
            (pygame.K_s, True): self.save_game
        }
        
    def _on_click(self, event: Event) -> bool:        
        if event.is_left_click:
            self.save_game_dialog()

    def render(self, screen_pos: Position) -> None:
        pygame.draw.rect(self._screen, Color.BLACK, self._rect, border_radius=10)
        current_time = pygame.time.get_ticks()
        if current_time - self._save_timestamp < 3000:  # 3 seconds
            icon = self._saved_icon
        else:
            icon = self._icon
        
        icon_rect = icon.get_rect(center=self._rect.center)
        self._screen.blit(icon, icon_rect)
        pygame.draw.rect(self._screen, Color.WHITE, self._rect, 2, border_radius=10)
        
    def save_game(self):
        if self._app_state.filepath is not None:
            data = self._railway.to_dict()
            with open(self._app_state.filepath, 'w') as f:
                json.dump(data, f, indent=4)
            self._save_timestamp = pygame.time.get_ticks()
        else:
            self.save_game_dialog()
        
    def save_game_dialog(self):
        data = self._railway.to_dict()
        
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save simulation as..."
        )
        if not filepath:
            return None
            
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
                
            self._app_state.filepath = filepath
            self._save_timestamp = pygame.time.get_ticks()

        finally:
            root.destroy()