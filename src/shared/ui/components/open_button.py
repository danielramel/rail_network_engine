import pygame
from core.config.paths import ICON_PATHS
from core.models.app_state import AppState
from core.models.railway.railway_system import RailwaySystem
from core.graphics.icon_loader import IconLoader
from core.models.geometry.position import Position
from core.config.color import Color
from core.config.settings import Config
from shared.ui.models.shortcut_ui_component import ShortcutUIComponent
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from shared.ui.models.rectangle import RectangleUIComponent
from core.models.event import Event


class OpenButton(ShortcutUIComponent, RectangleUIComponent, ClickableUIComponent):
    def __init__(self, screen: pygame.Surface, railway: RailwaySystem, app_state: AppState):
        rect = pygame.Rect(200+Config.BUTTON_SIZE + Config.BUTTON_SIZE//5, Config.BUTTON_SIZE//5, Config.BUTTON_SIZE, Config.BUTTON_SIZE)
        self._icon = IconLoader().get_icon(ICON_PATHS["LOAD"], Config.BUTTON_SIZE)
        super().__init__(rect, screen)
        self._railway = railway
        self._app_state = app_state
        # define shortcut here after method exists
        self._shortcuts = {
            (pygame.K_o, True): self.load_game_ui
        }

    def _on_click(self, event: Event) -> None:
        if event.is_left_click:
            self.load_game_ui()

    def render(self, screen_pos: Position) -> None:
        pygame.draw.rect(self._screen, Color.BLACK, self._rect, border_radius=10)
        icon_rect = self._icon.get_rect(center=self._rect.center)
        self._screen.blit(self._icon, icon_rect)
        pygame.draw.rect(self._screen, Color.WHITE, self._rect.inflate(-2, -2), 1, border_radius=10)

    def load_game_ui(self):
        import tkinter as tk
        from tkinter import filedialog, messagebox
        import json

        root = tk.Tk()
        root.withdraw()
        try:
            filename = filedialog.askopenfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Load simulation from..."
            )
            if not filename:
                return None

            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._railway.from_dict(data)

        except Exception as e:
            messagebox.showerror("Load error", str(e))
        finally:
            root.destroy()
            self._app_state.filename = filename
