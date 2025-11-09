import pygame
from core.config.paths import ICON_PATHS
from core.models.railway.railway_system import RailwaySystem
from core.graphics.icon_loader import IconLoader
from core.models.geometry.position import Position
from core.config.colors import BLACK, WHITE
from core.config.settings import BUTTON_SIZE
from shared.ui.models.shortcut_ui_component import ShortcutUIComponent
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from shared.ui.models.rectangle import RectangleUIComponent
from core.models.event import Event


class LoadButton(ShortcutUIComponent, RectangleUIComponent, ClickableUIComponent):
    def __init__(self, surface: pygame.Surface, railway: RailwaySystem):
        rect = pygame.Rect(BUTTON_SIZE // 5, 800, BUTTON_SIZE, BUTTON_SIZE)
        self._icon = IconLoader().get_icon(ICON_PATHS["LOAD"], BUTTON_SIZE)
        super().__init__(rect, surface)
        self._railway = railway

        # define shortcut here after method exists
        self._shortcuts = {
            (pygame.K_l, True): self.load_game_ui
        }

    def _on_click(self, event: Event) -> None:
        if event.is_left_click:
            self.load_game_ui()

    def render(self, screen_pos: Position) -> None:
        pygame.draw.rect(self._surface, BLACK, self._rect, border_radius=10)
        icon_rect = self._icon.get_rect(center=self._rect.center)
        self._surface.blit(self._icon, icon_rect)
        pygame.draw.rect(self._surface, WHITE, self._rect.inflate(-2, -2), 1, border_radius=10)

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
