import pygame
import os
from core.config.color import Color
from core.config.settings import Config
from core.models.geometry.position import Position
from typing import Callable

MAPS_FOLDER = Config.MAPS_FOLDER

class MainMenuController:
    def __init__(self, screen: pygame.Surface, start_callback: Callable):
        self._screen = screen
        self._start_callback = start_callback
        self._font_title = pygame.font.SysFont("Arial", 72, bold=True)
        self._font_button = pygame.font.SysFont("Arial", 36)
        self._font_map_button = pygame.font.SysFont("Arial", 28)
        
        # Scan maps folder for available map files
        self._map_files = self._scan_maps_folder()
        
        # Calculate button positions
        screen_w, screen_h = screen.get_size()
        button_width = 300
        button_height = 60
        button_spacing = 100
        
        map_button_width = 300
        map_button_height = 50
        map_button_spacing = 20
        
        center_x = screen_w // 2
        
        # Create map file buttons at the top (below title)
        self._map_buttons: list[tuple[pygame.Rect, str, pygame.Surface]] = []
        maps_start_y = 250  # Start maps closer to the top
        
        for i, (filename, filepath) in enumerate(self._map_files):
            button_rect = pygame.Rect(
                center_x - map_button_width // 2,
                maps_start_y + i * (map_button_height + map_button_spacing),
                map_button_width,
                map_button_height
            )
            # Create display name from filename (remove .json extension)
            display_name = os.path.splitext(filename)[0].replace("_", " ").title()
            text_surface = self._font_map_button.render(display_name, True, Color.WHITE)
            self._map_buttons.append((button_rect, filepath, text_surface))
        
        # Position New and Load buttons at the bottom, side by side
        bottom_buttons_y = screen_h - button_height - 200
        
        self._new_button_rect = pygame.Rect(
            center_x - button_width - button_spacing // 2,
            bottom_buttons_y,
            button_width,
            button_height
        )
        
        self._load_button_rect = pygame.Rect(
            center_x + button_spacing // 2,
            bottom_buttons_y,
            button_width,
            button_height
        )
        
        self._title_text = self._font_title.render("Rail Simulator", True, Color.WHITE)
        self._new_text = self._font_button.render("Create New Railway", True, Color.WHITE)
        self._load_text = self._font_button.render("Load Railway", True, Color.WHITE)
        self._no_maps_text = self._font_map_button.render("No maps found", True, Color.GREY)
        self._your_maps_text = self._font_button.render("Your Maps:", True, Color.WHITE)
        
        # Quit button in bottom left corner
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
        if pygame_event.type == pygame.KEYDOWN and pygame_event.key == pygame.K_ESCAPE:
            pygame.quit()
            raise SystemExit()
        if pygame_event.type == pygame.MOUSEMOTION:
            mouse_pos = Position(*pygame.mouse.get_pos())
            if self._new_button_rect.collidepoint(mouse_pos.x, mouse_pos.y):
                self._hovered_button = "new"
            elif self._load_button_rect.collidepoint(mouse_pos.x, mouse_pos.y):
                self._hovered_button = "load"
            elif self._quit_button_rect.collidepoint(mouse_pos.x, mouse_pos.y):
                self._hovered_button = "quit"
            else:
                # Check map buttons
                self._hovered_button = None
                for i, (rect, filepath, _) in enumerate(self._map_buttons):
                    if rect.collidepoint(mouse_pos.x, mouse_pos.y):
                        self._hovered_button = f"map_{i}"
                        break
        
        if pygame_event.type == pygame.MOUSEBUTTONUP and pygame_event.button == 1:
            mouse_pos = Position(*pygame.mouse.get_pos())
            if self._new_button_rect.collidepoint(mouse_pos.x, mouse_pos.y):
                self._start_callback(None)
                
            elif self._load_button_rect.collidepoint(mouse_pos.x, mouse_pos.y):
                filepath = self._open_file_dialog()
                if filepath:
                    self._start_callback(filepath)
            
            elif self._quit_button_rect.collidepoint(mouse_pos.x, mouse_pos.y):
                pygame.quit()
                raise SystemExit()
            
            else:
                # Check map buttons
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
                title="Load Railway..."
            )
            return filepath if filepath else None
        finally:
            root.destroy()
    
    
    def render(self):
        """Render the main menu."""
        self._screen.fill(Color.BLACK)
        
        screen_w, screen_h = self._screen.get_size()
        
        # Draw title at the top
        title_rect = self._title_text.get_rect(center=(screen_w // 2, 70))
        self._screen.blit(self._title_text, title_rect)
        
        # Draw "Your Maps:" label above the map buttons
        your_maps_rect = self._your_maps_text.get_rect(center=(screen_w // 2, 160))
        self._screen.blit(self._your_maps_text, your_maps_rect)
        
        # Draw map file buttons first (at the top) or "No maps found" message
        if self._map_buttons:
            for i, (rect, filepath, text_surface) in enumerate(self._map_buttons):
                self._draw_button(rect, text_surface, self._hovered_button == f"map_{i}")
                if i == 4:
                    break  # Limit to first 5 map buttons for display
        else:
            no_maps_rect = self._no_maps_text.get_rect(center=(screen_w // 2, 500))
            self._screen.blit(self._no_maps_text, no_maps_rect)
        
        # Draw New and Load buttons at the bottom
        self._draw_button(self._new_button_rect, self._new_text, self._hovered_button == "new")
        self._draw_button(self._load_button_rect, self._load_text, self._hovered_button == "load")
        
        # Draw quit button
        self._draw_button(self._quit_button_rect, self._quit_text, self._hovered_button == "quit")
    
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