import pygame
from config.colors import BLACK, WHITE, YELLOW

class RailPanelContent:
    """Rail construction panel with +/- controls for track speed.
    Stores button rects on the instance so click handling works outside draw().
    """
    def __init__(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        self.padding: int = 15
        self.button_size: int = 32
        self._surface = surface
        self.rect = rect
        
        # Initialize fonts
        self.title_font = pygame.font.SysFont(None, 28)
        self.data_font = pygame.font.SysFont(None, 22)
        
        # Pre-render static text
        self.title_surface = self.title_font.render("Rail Construction", True, YELLOW)
        self.label_surface = self.data_font.render("Track speed:", True, WHITE)
        self.minus_text = self.data_font.render("-", True, WHITE)
        self.plus_text = self.data_font.render("+", True, WHITE)
        
        # Calculate and store all layout rects
        self._init_layout()
       
    def _init_layout(self) -> None:
        """Compute and persist all rects for layout."""
        # Title position
        self.title_rect = self.title_surface.get_rect(
            centerx=self.rect.centerx, 
            top=self.rect.top + self.padding
        )
        
        # Label position
        self.label_rect = self.label_surface.get_rect(
            left=self.rect.left + self.padding, 
            top=self.title_rect.bottom + 20
        )
        
        # Button positions
        button_y = self.label_rect.top - 4
        minus_x = self.label_rect.right + 20
        plus_x = minus_x + self.button_size + 60
        
        self.minus_rect = pygame.Rect(minus_x, button_y, self.button_size, self.button_size)
        self.plus_rect = pygame.Rect(plus_x, button_y, self.button_size, self.button_size)
        
        # Speed value position (center between buttons)
        self.speed_center = (self.minus_rect.right + 40, self.minus_rect.centery)
       
    def draw(self, mode_info: dict) -> None:
        """Minimal draw method - just blit pre-computed surfaces."""
        # Title
        self._surface.blit(self.title_surface, self.title_rect)
        
        # Label
        self._surface.blit(self.label_surface, self.label_rect)
        
        # Minus button
        if mode_info['track_speed'] > 10:
            pygame.draw.rect(self._surface, BLACK, self.minus_rect, border_radius=6)
            pygame.draw.rect(self._surface, WHITE, self.minus_rect, width=2, border_radius=6)
            self._surface.blit(self.minus_text, self.minus_text.get_rect(center=self.minus_rect.center))
        
        # Speed value (only dynamic part)
        speed_val = str(mode_info.get('track_speed', 0))
        speed_surface = self.data_font.render(speed_val, True, YELLOW)
        self._surface.blit(speed_surface, speed_surface.get_rect(center=self.speed_center))
        
        # Plus button
        if mode_info['track_speed'] < 200:
            pygame.draw.rect(self._surface, BLACK, self.plus_rect, border_radius=6)
            pygame.draw.rect(self._surface, WHITE, self.plus_rect, width=2, border_radius=6)
            self._surface.blit(self.plus_text, self.plus_text.get_rect(center=self.plus_rect.center))
    
    def handle_click(self, pos: tuple[int, int], mode_info: dict) -> bool:
        """Handle +/- clicks; return True if the event was consumed."""
        if self.minus_rect.collidepoint(*pos):
            mode_info['track_speed'] -= 10
            mode_info['track_speed'] = max(10, mode_info['track_speed'])
            return True
        if self.plus_rect.collidepoint(*pos):
            mode_info['track_speed'] += 10
            mode_info['track_speed'] = min(200, mode_info['track_speed'])
            return True
        return False