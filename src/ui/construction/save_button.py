import pygame
from models.simulation import Simulation
from graphics.icon_loader import IconLoader
from models.geometry.position import Position
from config.colors import BLACK, WHITE, YELLOW, RED
from config.settings import BUTTON_SIZE
from ui.components.rectangle import RectangleUIComponent


class SaveButton(RectangleUIComponent):
    handled_events = [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL, pygame.KEYDOWN]
    def __init__(self, surface: pygame.Surface, simulation: Simulation):
        rect = pygame.Rect(BUTTON_SIZE//5, 700, BUTTON_SIZE, BUTTON_SIZE)
        super().__init__(rect, surface)
        self._simulation = simulation

    def handle_event(self, event: pygame.event) -> bool:   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                # Handle Ctrl+S
                self.save_game()
                return True
            return False
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self._rect.collidepoint(*event.pos_):
            self.save_game()
            return True
           
        return self._rect.collidepoint(*event.pos_)

    def render(self, screen_pos: Position) -> None:
        pygame.draw.rect(self._surface, WHITE, self._rect, border_radius=10)

        font_size = max(12, self._rect.height - 10)
        font = pygame.font.Font(None, font_size)
        text_surf = font.render("S", True, YELLOW)
        text_rect = text_surf.get_rect(center=self._rect.center)
        self._surface.blit(text_surf, text_rect)


        pygame.draw.rect(self._surface, WHITE, self._rect.inflate(-2, -2), 1, border_radius=10)

    def contains(self, screen_pos: Position) -> bool:
        return self._rect.collidepoint(screen_pos.x, screen_pos.y)
    
    def save_game(self):
        data = self._simulation.to_dict()
        
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