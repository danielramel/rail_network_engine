import pygame
from config.colors import BLACK, WHITE, YELLOW
from models.construction_state import ConstructionState
from ui.construction.panels.base_construction_panel import BaseConstructionPanel
    
class RailPanel(BaseConstructionPanel):
    """Rail construction panel with +/- controls for track speed."""
    
    # Speed configuration constants
    MIN_SPEED = 10
    MAX_SPEED = 200
    SPEED_INCREMENT = 10
    
    def __init__(self, surface: pygame.Surface, state: ConstructionState) -> None:
        super().__init__(surface, state)
        
        self.button_size: int = 32
        
        # Pre-render static text
        self.title_surface = self.title_font.render("Rail Construction", True, YELLOW)
        self.label_surface = self.instruction_font.render("Track speed:", True, WHITE)
        self.minus_text = self.instruction_font.render("-", True, WHITE)
        self.plus_text = self.instruction_font.render("+", True, WHITE)
        
        # Calculate and store all layout rects
        self._init_layout()
    
    @property
    def can_decrease_speed(self) -> bool:
        """Check if speed can be decreased."""
        return self._construction_state.track_speed > self.MIN_SPEED
    
    @property
    def can_increase_speed(self) -> bool:
        """Check if speed can be increased."""
        return self._construction_state.track_speed < self.MAX_SPEED
       
    def _init_layout(self) -> None:
        """Compute and persist all rects for layout."""
        # Title position
        self.title_rect = self.title_surface.get_rect(
            centerx=self._rect.centerx, 
            top=self._rect.top + self.padding
        )
        
        # Label position
        self.label_rect = self.label_surface.get_rect(
            left=self._rect.left + self.padding,
            top=self.title_rect.bottom + 20
        )
        
        # Button positions
        button_y = self.label_rect.top - 4
        minus_x = self.label_rect.right + 20
        plus_x = minus_x + self.button_size + 120
        
        self.minus_rect = pygame.Rect(minus_x, button_y, self.button_size, self.button_size)
        self.plus_rect = pygame.Rect(plus_x, button_y, self.button_size, self.button_size)
        
        # Speed value position (center between buttons)
        self.speed_center = (self.minus_rect.right + 60, self.minus_rect.centery)
    
    def _render_button(self, rect: pygame.Rect, text_surface: pygame.Surface, enabled: bool) -> None:
        """Render a button with consistent styling."""
        if enabled:
            pygame.draw.rect(self._surface, BLACK, rect, border_radius=6)
            pygame.draw.rect(self._surface, WHITE, rect, width=2, border_radius=6)
            self._surface.blit(text_surface, text_surface.get_rect(center=rect.center))
    
    def _adjust_speed(self, delta: int) -> None:
        """Adjust track speed by delta, clamping to valid range."""
        self._construction_state.track_speed += delta
        self._construction_state.track_speed = max(
            self.MIN_SPEED, 
            min(self.MAX_SPEED, self._construction_state.track_speed)
        )
       
    def render(self, screen_pos) -> None:
        """Minimal render method - just blit pre-computed surfaces."""
        super().render(screen_pos)  # background and border

        # Title
        self._surface.blit(self.title_surface, self.title_rect)
        
        # Label
        self._surface.blit(self.label_surface, self.label_rect)
        
        # Buttons
        self._render_button(self.minus_rect, self.minus_text, self.can_decrease_speed)
        self._render_button(self.plus_rect, self.plus_text, self.can_increase_speed)
        
        # Speed value (only dynamic part)
        speed_val = f"{self._construction_state.track_speed} km/h"
        speed_surface = self.instruction_font.render(speed_val, True, YELLOW)
        self._surface.blit(speed_surface, speed_surface.get_rect(center=self.speed_center))

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle +/- clicks; return True if the event was consumed."""     
        if event.type != pygame.MOUSEBUTTONUP or event.button != 1:
            return self._rect.collidepoint(*event.screen_pos)
        
        if self.minus_rect.collidepoint(*event.screen_pos) and self.can_decrease_speed:
            self._adjust_speed(-self.SPEED_INCREMENT)
            return True
        
        if self.plus_rect.collidepoint(*event.screen_pos) and self.can_increase_speed:
            self._adjust_speed(self.SPEED_INCREMENT)
            return True
        
        return self._rect.collidepoint(*event.screen_pos)