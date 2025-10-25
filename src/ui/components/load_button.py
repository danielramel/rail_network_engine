import pygame
from config.paths import GLOBAL_ICON_PATHS
from models.railway_system import RailwaySystem
from graphics.icon_loader import IconLoader
from models.geometry.position import Position
from config.colors import BLACK, WHITE, YELLOW, RED
from config.settings import BUTTON_SIZE
from ui.models.rectangle import RectangleUIComponent


class LoadButton(RectangleUIComponent):
    handled_events = [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL, pygame.KEYDOWN]
    def __init__(self, surface: pygame.Surface, railway: RailwaySystem):
        rect = pygame.Rect(BUTTON_SIZE//5, 800, BUTTON_SIZE, BUTTON_SIZE)
        self.icon = IconLoader().get_icon(GLOBAL_ICON_PATHS["LOAD"], BUTTON_SIZE)
        super().__init__(rect, surface)
        self._railway = railway

    def handle_event(self, event: pygame.event) -> bool:   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l and (event.mod & pygame.KMOD_CTRL):
                # Handle Ctrl+L
                self.load_game()
                return True
            return False
        
        elif self._rect.collidepoint(*event.screen_pos):
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.load_game()
            return True
           
        return self._rect.collidepoint(*event.screen_pos)

    def render(self, screen_pos: Position) -> None:
        pygame.draw.rect(self._surface, BLACK, self._rect, border_radius=10)
        icon_rect = self.icon.get_rect(center=self._rect.center)
        self._surface.blit(self.icon, icon_rect)
        pygame.draw.rect(self._surface, WHITE, self._rect.inflate(-2, -2), 1, border_radius=10)

    def contains(self, screen_pos: Position) -> bool:
        return self._rect.collidepoint(screen_pos.x, screen_pos.y)
    
    def load_game(self):
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
                data = json.loads(f.read())

                self._railway.from_dict(data)

        except Exception as e:
            messagebox.showerror("Load error", str(e))
        finally:
            root.destroy()