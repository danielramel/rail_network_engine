from models.construction import ConstructionMode
from ui.core.ui_element import RectangleUIElement
import pygame
from config.colors import BLACK, WHITE, YELLOW

class Panel(RectangleUIElement):
    def __init__(self, surface: pygame.Surface, state: dict):
        self._surface = surface
        self._state = state
        self.rect = self._get_panel_rect()

    def draw(self) -> None:
        if self._state.mode is not ConstructionMode.RAIL:
            return
        """Draw a construction information panel in the middle bottom of the screen"""
        padding = 15
        pygame.draw.rect(self._surface, BLACK, self.rect, border_radius=8)
        pygame.draw.rect(self._surface, WHITE, self.rect, 2, border_radius=8)

        # Font setup
        title_font = pygame.font.SysFont(None, 28)
        data_font = pygame.font.SysFont(None, 22)
        
        # Draw title
        title_surface = title_font.render("Rail Construction", True, YELLOW)
        title_rect = title_surface.get_rect(centerx=self.rect.centerx, top=self.rect.top + padding)
        self._surface.blit(title_surface, title_rect)
        
        # Draw track speed adjustment controls
        label_surface = data_font.render("Track speed:", True, WHITE)
        label_rect = label_surface.get_rect(left=self.rect.left + padding, top=title_rect.bottom + 20)
        self._surface.blit(label_surface, label_rect)

        # Button dimensions
        button_size = 32
        button_y = label_rect.top - 4
        minus_x = label_rect.right + 20
        plus_x = minus_x + button_size + 60

        # Draw minus button with border
        minus_rect = pygame.Rect(minus_x, button_y, button_size, button_size)
        pygame.draw.rect(self._surface, BLACK, minus_rect, border_radius=6)
        pygame.draw.rect(self._surface, WHITE, minus_rect, width=2, border_radius=6)
        minus_text = data_font.render("-", True, WHITE)
        minus_text_rect = minus_text.get_rect(center=minus_rect.center)
        self._surface.blit(minus_text, minus_text_rect)

        # Draw speed value
        speed_surface = data_font.render(str(self._state.mode_info['track_speed']), True, YELLOW)
        speed_rect = speed_surface.get_rect(center=(minus_rect.right + 40, minus_rect.centery))
        self._surface.blit(speed_surface, speed_rect)

        # Draw plus button with border
        plus_rect = pygame.Rect(plus_x, button_y, button_size, button_size)
        pygame.draw.rect(self._surface, BLACK, plus_rect, border_radius=6)
        pygame.draw.rect(self._surface, WHITE, plus_rect, width=2, border_radius=6)
        plus_text = data_font.render("+", True, WHITE)
        plus_text_rect = plus_text.get_rect(center=plus_rect.center)
        self._surface.blit(plus_text, plus_text_rect)

    
    def _get_panel_rect(self) -> pygame.Rect:
        # Panel dimensions
        panel_width = 400
        panel_height = 120
        
        # Position in middle bottom
        screen_width, screen_height = self._surface.get_size()
        panel_x = (screen_width - panel_width) // 2
        panel_y = screen_height - panel_height - 15
        
        return pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        
        

    