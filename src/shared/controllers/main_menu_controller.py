import pygame
from core.config.color import Color
from core.models.geometry.position import Position
from typing import Callable

class MainMenuController:
    """Main menu screen with options to create new railway or load existing one."""
    
    def __init__(self, screen: pygame.Surface, start_callback: Callable):
        self._screen = screen
        self._start_callback = start_callback
        self._font_title = pygame.font.SysFont("Arial", 72, bold=True)
        self._font_button = pygame.font.SysFont("Arial", 36)
        
        # Calculate button positions
        screen_w, screen_h = screen.get_size()
        button_width = 400
        button_height = 80
        button_spacing = 40
        
        center_x = screen_w // 2
        center_y = screen_h // 2
        
        self._new_button_rect = pygame.Rect(
            center_x - button_width // 2,
            center_y - button_height - button_spacing // 2,
            button_width,
            button_height
        )
        
        self._load_button_rect = pygame.Rect(
            center_x - button_width // 2,
            center_y + button_spacing // 2,
            button_width,
            button_height
        )
        
        self._title_text = self._font_title.render("Rail Simulator", True, Color.WHITE)
        self._new_text = self._font_button.render("Create New Railway", True, Color.WHITE)
        self._load_text = self._font_button.render("Load Existing Railway", True, Color.WHITE)
        
        self._hovered_button: str | None = None
        self._selected_action: str | None = None
        self._selected_filepath: str | None = None
    
    def dispatch_event(self, pygame_event: pygame.event) -> str | None:
        if pygame_event.type == pygame.MOUSEMOTION:
            mouse_pos = Position(*pygame.mouse.get_pos())
            if self._new_button_rect.collidepoint(mouse_pos.x, mouse_pos.y):
                self._hovered_button = "new"
            elif self._load_button_rect.collidepoint(mouse_pos.x, mouse_pos.y):
                self._hovered_button = "load"
            else:
                self._hovered_button = None
        
        if pygame_event.type == pygame.MOUSEBUTTONUP and pygame_event.button == 1:
            mouse_pos = Position(*pygame.mouse.get_pos())
            if self._new_button_rect.collidepoint(mouse_pos.x, mouse_pos.y):
                self._start_callback(None)
                
            elif self._load_button_rect.collidepoint(mouse_pos.x, mouse_pos.y):
                filepath = self._open_file_dialog()
                if filepath:
                    self._start_callback(filepath)
                    
    
    def _open_file_dialog(self) -> str | None:
        """Open file dialog to select a railway file."""
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()
        try:
            filepath = filedialog.askopenfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Load Railway..."
            )
            return filepath if filepath else None
        finally:
            root.destroy()
    
    
    def render(self):
        """Render the main menu."""
        self._screen.fill(Color.BLACK)
        
        screen_w, screen_h = self._screen.get_size()
        
        # Draw title
        title_rect = self._title_text.get_rect(center=(screen_w // 2, screen_h // 4))
        self._screen.blit(self._title_text, title_rect)
        
        # Draw buttons
        self._draw_button(self._new_button_rect, self._new_text, self._hovered_button == "new")
        self._draw_button(self._load_button_rect, self._load_text, self._hovered_button == "load")
    
    def _draw_button(self, rect: pygame.Rect, text_surface: pygame.Surface, hovered: bool):
        """Draw a menu button."""
        # Button background
        if hovered:
            pygame.draw.rect(self._screen, Color.DARKGREY, rect, border_radius=15)
        else:
            pygame.draw.rect(self._screen, Color.BLACK, rect, border_radius=15)
        
        # Button border
        border_color = Color.WHITE if hovered else Color.GREY
        pygame.draw.rect(self._screen, border_color, rect, 3, border_radius=15)
        
        # Button text
        text_rect = text_surface.get_rect(center=rect.center)
        self._screen.blit(text_surface, text_rect)
        
        
    def tick(self):
        pass