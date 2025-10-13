from models.geometry.position import Position
from ui.components.base import BaseUIComponent
import pygame
from domain.rail_map import RailMap
from models.train import TrainRepository
from config.colors import BLUE

class TimetableView(BaseUIComponent):
    def __init__(self, map: RailMap, train_repository: TrainRepository, screen: pygame.Surface):
        self._surface = screen
        self._map = map
        self._train_repository = train_repository
        
        # Fonts - all bigger
        self.title_font = pygame.font.SysFont('Arial', 36, bold=True)
        self.header_font = pygame.font.SysFont('Arial', 24, bold=True)
        self.text_font = pygame.font.SysFont('Arial', 20)
        
        # Colors
        self.bg_color = (0, 0, 0)
        self.header_color = (255, 255, 255)
        self.text_color = (200, 200, 200)
        self.line_color = (80, 80, 80)
        self.button_color = (50, 50, 50)
        self.button_hover_color = (70, 70, 70)
        self.button_text_color = (255, 255, 255)
        self.s70_color = (100, 150, 255)
        self.s71_color = (255, 150, 100)
        self.z72_color = (150, 255, 150)
        
        # Table dimensions
        self.table_width = 800
        
        # Add train button
        self.add_button_rect = None
        self.is_hovering_button = False
       
    def render(self, screen_pos: Position | None):
        # Clear background
        self._surface.fill(self.bg_color)
        
        # Calculate center offset for horizontal centering
        screen_width = self._surface.get_width()
        center_offset = (screen_width - self.table_width) // 2
        
        # Title
        title = self.title_font.render("Train Timetable", True, self.header_color)
        title_rect = title.get_rect()
        title_rect.centerx = screen_width // 2
        title_rect.y = 20
        self._surface.blit(title, title_rect)
        
        # Column headers
        y_offset = 80
        headers = ["Type", "Route", "Start", "Frequency"]
        x_positions = [center_offset + 20, center_offset + 150, 
                      center_offset + 550, center_offset + 680]
        
        for i, header in enumerate(headers):
            header_text = self.header_font.render(header, True, self.header_color)
            self._surface.blit(header_text, (x_positions[i], y_offset))
        
        # Draw separator line
        pygame.draw.line(self._surface, self.line_color, 
                        (center_offset + 20, y_offset + 35), 
                        (center_offset + self.table_width, y_offset + 35), 2)
        
        # Render timetable entries
        y_offset += 50
        row_height = 60
        
        for train in self._train_repository.all():
            # Train type with color coding
            type_color = BLUE
            
            # Type badge
            pygame.draw.rect(self._surface, type_color, 
                           (x_positions[0], y_offset, 80, 40), border_radius=5)
            type_text = self.text_font.render(train.code, True, (0, 0, 0))
            self._surface.blit(type_text, (x_positions[0] + 15, y_offset + 10))
            
            # Stations (route)
            stations_str = " → ".join(station for station in train.stations)
            stations_text = self.text_font.render(stations_str, True, self.text_color)
            self._surface.blit(stations_text, (x_positions[1], y_offset + 10))
            
            # Start time
            start_text = self.text_font.render(train.start_time, True, self.text_color)
            self._surface.blit(start_text, (x_positions[2], y_offset + 10))
            
            # Frequency
            freq_text = self.text_font.render(train.frequency, True, self.text_color)
            self._surface.blit(freq_text, (x_positions[3], y_offset + 10))
            
            y_offset += row_height
            
            # Draw separator line
            pygame.draw.line(self._surface, self.line_color, 
                           (center_offset + 20, y_offset - 10), 
                           (center_offset + self.table_width, y_offset - 10), 1)
        
        # Add train button
        button_width = 180
        button_height = 50
        button_x = (screen_width - button_width) // 2
        button_y = y_offset + 30
        
        self.add_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
        button_color = self.button_hover_color if self.is_hovering_button else self.button_color
        pygame.draw.rect(self._surface, button_color, self.add_button_rect, border_radius=5)
        pygame.draw.rect(self._surface, self.line_color, self.add_button_rect, 2, border_radius=5)
        
        button_text = self.text_font.render("+ Add Train", True, self.button_text_color)
        button_text_rect = button_text.get_rect(center=self.add_button_rect.center)
        self._surface.blit(button_text, button_text_rect)