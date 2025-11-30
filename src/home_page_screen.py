import pygame
import os
from core.config.color import Color
from core.config.config import Config
from core.models.geometry.position import Position
from typing import Callable

MAPS_FOLDER = Config.MAPS_FOLDER

class HomePageScreen:
    def __init__(self, screen: pygame.Surface, start_callback: Callable):
        self._screen = screen
        self._start_callback = start_callback
        self._font_title = pygame.font.SysFont("Arial", 72, bold=True)
        self._font_button = pygame.font.SysFont("Arial", 36)
        self._font_map_button = pygame.font.SysFont("Arial", 34)
        
        self._map_files = self._scan_maps_folder()
        
        screen_w, screen_h = screen.get_size()
        button_width = 420
        button_height = 80
        button_spacing = 100
        
        map_button_height = 90
        map_button_h_spacing = max(80, screen_w // 18)
        available_width = int(screen_w * 0.92)
        map_button_width = (available_width - map_button_h_spacing) // 2
        map_button_width = max(420, min(map_button_width, 640))
        map_button_v_spacing = 30
        
        center_x = screen_w // 2
        
        self._map_buttons: list[tuple[pygame.Rect, str, pygame.Surface]] = []
        maps_start_y = 220 
        columns = 2
        rows = 4
        max_buttons = columns * rows
        grid_total_width = columns * map_button_width + (columns - 1) * map_button_h_spacing
        grid_start_x = center_x - grid_total_width // 2

        for i, (filename, filepath) in enumerate(self._map_files[:max_buttons]):
            row = i // columns
            col = i % columns
            x = grid_start_x + col * (map_button_width + map_button_h_spacing)
            y = maps_start_y + row * (map_button_height + map_button_v_spacing)
            button_rect = pygame.Rect(
                x,
                y,
                map_button_width,
                map_button_height
            )
            display_name = os.path.splitext(filename)[0].replace("_", " ").title()
            text_surface = self._font_map_button.render(display_name, True, Color.WHITE)
            self._map_buttons.append((button_rect, filepath, text_surface))
        
        bottom_buttons_y = screen_h - button_height - 200
        
        self._new_button_rect = pygame.Rect(
            center_x - button_width - button_spacing // 2,
            bottom_buttons_y,
            button_width,
            button_height
        )
        
        self._open_button_rect = pygame.Rect(
            center_x + button_spacing // 2,
            bottom_buttons_y,
            button_width,
            button_height
        )
        
        self._title_text = self._font_title.render("Rail Simulator", True, Color.WHITE)
        self._new_text = self._font_button.render("Create New Project", True, Color.WHITE)
        self._open_text = self._font_button.render("Open Project", True, Color.WHITE)
        self._no_maps_text = self._font_map_button.render("No projects found", True, Color.GREY)
        self._your_maps_text = self._font_button.render("Your projects:", True, Color.WHITE)
        
        quit_button_width = 120
        quit_button_height = 50
        quit_margin = 20
        self._quit_button_rect = pygame.Rect(
            quit_margin,
            screen_h - quit_button_height - quit_margin,
            quit_button_width,
            quit_button_height
        )
        self._quit_text = self._font_map_button.render("Quit", True, Color.WHITE)
        
        self._hovered_button: str | None = None
        self._selected_action: str | None = None
        self._selected_filepath: str | None = None
        
        self._alert_message: str | None = None
        self._alert_font = pygame.font.SysFont("Arial", 24)
        self._alert_title_font = pygame.font.SysFont("Arial", 32, bold=True)
        alert_width = 500
        alert_height = 200
        self._alert_rect = pygame.Rect(
            center_x - alert_width // 2,
            screen_h // 2 - alert_height // 2,
            alert_width,
            alert_height
        )
        self._alert_dismiss_text = self._alert_font.render("Click anywhere to dismiss", True, Color.GREY)
    
    def _scan_maps_folder(self) -> list[tuple[str, str]]:
        """Scan the maps folder and return list of (filename, filepath) tuples."""
        map_files = []
        if os.path.exists(MAPS_FOLDER) and os.path.isdir(MAPS_FOLDER):
            for filename in sorted(os.listdir(MAPS_FOLDER)):
                if filename.endswith(".json"):
                    filepath = os.path.join(MAPS_FOLDER, filename)
                    map_files.append((filename, filepath))
        return map_files
    
    def dispatch_event(self, pygame_event: pygame.event) -> str | None:
        if self._alert_message is not None:
            if pygame_event.type == pygame.MOUSEBUTTONUP and pygame_event.button == 1:
                self._alert_message = None
            elif pygame_event.type == pygame.KEYDOWN:
                self._alert_message = None
            return None
        
        if pygame_event.type == pygame.KEYDOWN and pygame_event.key == pygame.K_ESCAPE:
            pygame.quit()
            raise SystemExit()
        if pygame_event.type == pygame.MOUSEMOTION:
            mouse_pos = Position(*pygame.mouse.get_pos())
            if self._new_button_rect.collidepoint(mouse_pos.x, mouse_pos.y):
                self._hovered_button = "new"
            elif self._open_button_rect.collidepoint(mouse_pos.x, mouse_pos.y):
                self._hovered_button = "open"
            elif self._quit_button_rect.collidepoint(mouse_pos.x, mouse_pos.y):
                self._hovered_button = "quit"
            else:
                self._hovered_button = None
                for i, (rect, filepath, _) in enumerate(self._map_buttons):
                    if rect.collidepoint(mouse_pos.x, mouse_pos.y):
                        self._hovered_button = f"map_{i}"
                        break
        
        if pygame_event.type == pygame.MOUSEBUTTONUP and pygame_event.button == 1:
            mouse_pos = Position(*pygame.mouse.get_pos())
            if self._new_button_rect.collidepoint(mouse_pos.x, mouse_pos.y):
                self._start_callback(None)
                
            elif self._open_button_rect.collidepoint(mouse_pos.x, mouse_pos.y):
                filepath = self._open_file_dialog()
                if filepath:
                    self._start_callback(filepath)
            
            elif self._quit_button_rect.collidepoint(mouse_pos.x, mouse_pos.y):
                pygame.quit()
                raise SystemExit()
            
            else:
                for rect, filepath, _ in self._map_buttons:
                    if rect.collidepoint(mouse_pos.x, mouse_pos.y):
                        self._start_callback(filepath)
                        break
                    
    
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
                title="Open Railway..."
            )
            return filepath if filepath else None
        finally:
            root.destroy()
    
    
    def render(self):
        """Render the main menu."""
        self._screen.fill(Color.BLACK)
        
        screen_w, screen_h = self._screen.get_size()
        
        title_rect = self._title_text.get_rect(center=(screen_w // 2, 70))
        self._screen.blit(self._title_text, title_rect)
        
        your_maps_rect = self._your_maps_text.get_rect(center=(screen_w // 2, 160))
        self._screen.blit(self._your_maps_text, your_maps_rect)
        
        if self._map_buttons:
            for i, (rect, filepath, text_surface) in enumerate(self._map_buttons):
                self._draw_button(rect, text_surface, self._hovered_button == f"map_{i}")
        else:
            no_maps_rect = self._no_maps_text.get_rect(center=(screen_w // 2, 500))
            self._screen.blit(self._no_maps_text, no_maps_rect)
        
        self._draw_button(self._new_button_rect, self._new_text, self._hovered_button == "new")
        self._draw_button(self._open_button_rect, self._open_text, self._hovered_button == "open")
        
        self._draw_button(self._quit_button_rect, self._quit_text, self._hovered_button == "quit")
        
        if self._alert_message:
            self._draw_alert()
    
    def _draw_button(self, rect: pygame.Rect, text_surface: pygame.Surface, hovered: bool, bg_color: tuple[int, int, int] | None = None, border_color: tuple[int, int, int] | None = None):
        """Draw a menu button."""
        if bg_color is None:
            fill_color = Color.DARKGREY if hovered else Color.BLACK
        else:
            fill_color = self._adjust_color(bg_color, 1.1) if hovered else bg_color
        pygame.draw.rect(self._screen, fill_color, rect, border_radius=15)
        
        bcolor = border_color if border_color is not None else (Color.WHITE if hovered else Color.GREY)
        pygame.draw.rect(self._screen, bcolor, rect, 3, border_radius=15)
        
        text_rect = text_surface.get_rect(center=rect.center)
        self._screen.blit(text_surface, text_rect)

    @staticmethod
    def _adjust_color(color: tuple[int, int, int], factor: float) -> tuple[int, int, int]:
        r, g, b = color
        r = max(0, min(255, int(r * factor)))
        g = max(0, min(255, int(g * factor)))
        b = max(0, min(255, int(b * factor)))
        return (r, g, b)
    
    def _draw_alert(self):
        """Draw the alert overlay."""
        screen_w, screen_h = self._screen.get_size()
        
        overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self._screen.blit(overlay, (0, 0))
        
        pygame.draw.rect(self._screen, Color.BLACK, self._alert_rect, border_radius=15)
        pygame.draw.rect(self._screen, Color.WHITE, self._alert_rect, 3, border_radius=15)
        
        title_surface = self._alert_title_font.render("Notice", True, Color.WHITE)
        title_rect = title_surface.get_rect(centerx=self._alert_rect.centerx, top=self._alert_rect.top + 20)
        self._screen.blit(title_surface, title_rect)
        
        message_surface = self._alert_font.render(self._alert_message, True, Color.WHITE)
        message_rect = message_surface.get_rect(center=self._alert_rect.center)
        self._screen.blit(message_surface, message_rect)
        
        dismiss_rect = self._alert_dismiss_text.get_rect(centerx=self._alert_rect.centerx, bottom=self._alert_rect.bottom - 15)
        self._screen.blit(self._alert_dismiss_text, dismiss_rect)
        
        
    def tick(self):
        pass
    
    def alert(self, message: str):
        """Display an alert message overlay on the main menu."""
        self._alert_message = message