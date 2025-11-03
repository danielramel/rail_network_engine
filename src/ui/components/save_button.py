import pygame
from config.paths import GLOBAL_ICON_PATHS
from models.railway_system import RailwaySystem
from graphics.icon_loader import IconLoader
from models.geometry.position import Position
from config.colors import BLACK, WHITE, YELLOW, RED
from config.settings import BUTTON_SIZE
from ui.models.rectangle import RectangleUIComponent


class SaveButton(RectangleUIComponent):
    handled_events = [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL, pygame.KEYDOWN]
    def __init__(self, surface: pygame.Surface, railway: RailwaySystem):
        self.icon = IconLoader().get_icon(GLOBAL_ICON_PATHS["SAVE"], BUTTON_SIZE)
        rect = pygame.Rect(BUTTON_SIZE//5, 700, BUTTON_SIZE, BUTTON_SIZE)
        super().__init__(rect, surface)
        self._railway = railway

    def process_event(self, event: pygame.event) -> bool:   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                # Handle Ctrl+S
                self.save_game()
                return True
            return False
        
        elif self._rect.collidepoint(*event.screen_pos):
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.save_game()
            return True
           
        return self._rect.collidepoint(*event.screen_pos)

    def render(self, screen_pos: Position) -> None:
        pygame.draw.rect(self._surface, BLACK, self._rect, border_radius=10)

        icon_rect = self.icon.get_rect(center=self._rect.center)
        self._surface.blit(self.icon, icon_rect)
        pygame.draw.rect(self._surface, WHITE, self._rect, 2, border_radius=10)
        



    def contains(self, screen_pos: Position) -> bool:
        return self._rect.collidepoint(screen_pos.x, screen_pos.y)
    
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