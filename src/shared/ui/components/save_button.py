import pygame
from core.config.paths import ICON_PATHS
from core.models.railway.railway_system import RailwaySystem
from core.graphics.icon_loader import IconLoader
from core.models.geometry.position import Position
from core.config.color import Color
from core.config.settings import BUTTON_SIZE
from shared.ui.models.rectangle import RectangleUIComponent
from shared.ui.models.shortcut_ui_component import ShortcutUIComponent
from core.models.event import Event
from shared.ui.models.clickable_ui_component import ClickableUIComponent


class SaveButton(ShortcutUIComponent, RectangleUIComponent, ClickableUIComponent):
    def __init__(self, surface: pygame.Surface, railway: RailwaySystem):
        self._icon = IconLoader().get_icon(ICON_PATHS["SAVE"], BUTTON_SIZE)
        rect = pygame.Rect(BUTTON_SIZE//5, 700, BUTTON_SIZE, BUTTON_SIZE)
        super().__init__(rect, surface)
        self._railway = railway
        self._shortcuts = {
            (pygame.K_s, True): self.save_game
        }

    def _on_click(self, event: Event) -> bool:        
        if event.is_left_click:
            self.save_game()

    def render(self, screen_pos: Position) -> None:
        pygame.draw.rect(self._surface, Color.BLACK, self._rect, border_radius=10)

        icon_rect = self._icon.get_rect(center=self._rect.center)
        self._surface.blit(self._icon, icon_rect)
        pygame.draw.rect(self._surface, Color.WHITE, self._rect, 2, border_radius=10)
        
    def save_game(self):
        data = self._railway.to_dict()
        
        import tkinter as tk
        from tkinter import filedialog
        import json
        root = tk.Tk()
        root.withdraw()
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Save simulation as..."
            )
            if not filename:
                return None

            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)

        finally:
            root.destroy()