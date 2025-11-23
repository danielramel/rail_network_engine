import pygame
from core.config.color import Color
from modules.construction.models.construction_state import ConstructionState
from modules.construction.models.construction_panel import ConstructionToolPanel
from core.models.event import Event
    
class RailPanel(ConstructionToolPanel):
    """Rail construction panel with +/- controls for track speed and toggle for track length."""
    
    # Speed configuration constants
    MIN_SPEED = 10
    MAX_SPEED = 200
    SPEED_INCREMENT = 10
    
    # Length configuration constants
    SHORT_LENGTH = 50
    LONG_LENGTH = 500
    
    def __init__(self, screen: pygame.Surface, state: ConstructionState) -> None:
        super().__init__(screen, state, height=200)
        
        self.button_size: int = 32
        
        # Pre-render static text
        self.title_screen = self.title_font.render("Rail Construction", True, Color.YELLOW)
        self.speed_label_screen = self.instruction_font.render("Track speed:", True, Color.WHITE)
        self.length_label_screen = self.instruction_font.render("Track length:", True, Color.WHITE)
        self.tunnel_label_screen = self.instruction_font.render("Tunnel:", True, Color.WHITE)
        self.minus_text = self.instruction_font.render("-", True, Color.WHITE)
        self.plus_text = self.instruction_font.render("+", True, Color.WHITE)
        
        # Calculate and store all layout rects
        self._init_layout()
    
    @property
    def can_decrease_speed(self) -> bool:
        """Check if speed can be decreased."""
        return self._state.track_speed > self.MIN_SPEED
    
    @property
    def can_increase_speed(self) -> bool:
        """Check if speed can be increased."""
        return self._state.track_speed < self.MAX_SPEED
       
    def _init_layout(self) -> None:
        """Compute and persist all rects for layout."""
        # Title position
        self.title_rect = self.title_screen.get_rect(
            centerx=self._rect.centerx, 
            top=self._rect.top + self.padding
        )
        
        # Speed label position
        self.speed_label_rect = self.speed_label_screen.get_rect(
            left=self._rect.left + self.padding,
            top=self.title_rect.bottom + 20
        )
        
        # Speed button positions
        speed_button_y = self.speed_label_rect.top - 4
        speed_minus_x = self.speed_label_rect.right + 20
        speed_plus_x = speed_minus_x + self.button_size + 120
        
        self.speed_minus_rect = pygame.Rect(speed_minus_x, speed_button_y, self.button_size, self.button_size)
        self.speed_plus_rect = pygame.Rect(speed_plus_x, speed_button_y, self.button_size, self.button_size)
        
        # Speed value position (center between buttons)
        self.speed_center = (self.speed_minus_rect.right + 60, self.speed_minus_rect.centery)
        
        # Length label position
        self.length_label_rect = self.length_label_screen.get_rect(
            left=self._rect.left + self.padding,
            top=self.speed_label_rect.bottom + 30
        )
        
        # Length toggle buttons (50m and 500m)
        toggle_button_y = self.length_label_rect.top - 4
        toggle_start_x = self.length_label_rect.right + 20
        toggle_width = 80
        toggle_spacing = 10
        
        self.length_short_rect = pygame.Rect(toggle_start_x, toggle_button_y, toggle_width, self.button_size)
        self.length_long_rect = pygame.Rect(
            toggle_start_x + toggle_width + toggle_spacing, 
            toggle_button_y, 
            toggle_width, 
            self.button_size
        )
        
        # Tunnel label position
        self.tunnel_label_rect = self.tunnel_label_screen.get_rect(
            left=self._rect.left + self.padding,
            top=self.length_label_rect.bottom + 30
        )
        
        # Tunnel toggle buttons (No tunnel and Tunnel)
        tunnel_button_y = self.tunnel_label_rect.top - 4
        tunnel_start_x = self.tunnel_label_rect.right + 20
        tunnel_width = 80
        tunnel_spacing = 10
        
        self.tunnel_no_rect = pygame.Rect(tunnel_start_x, tunnel_button_y, tunnel_width, self.button_size)
        self.tunnel_yes_rect = pygame.Rect(
            tunnel_start_x + tunnel_width + tunnel_spacing, 
            tunnel_button_y, 
            tunnel_width, 
            self.button_size
        )
    
    def _render_button(self, rect: pygame.Rect, text_screen: pygame.Surface, enabled: bool) -> None:
        """Render a button with consistent styling."""
        if enabled:
            pygame.draw.rect(self._screen, Color.BLACK, rect, border_radius=6)
            pygame.draw.rect(self._screen, Color.WHITE, rect, width=2, border_radius=6)
            self._screen.blit(text_screen, text_screen.get_rect(center=rect.center))
    
    def _render_toggle_button(self, rect: pygame.Rect, text: str, is_selected: bool) -> None:
        """Render a toggle button with selected/unselected states."""
        if is_selected:
            pygame.draw.rect(self._screen, Color.WHITE, rect, border_radius=6)
            text_screen = self.instruction_font.render(text, True, Color.BLACK)
        else:
            pygame.draw.rect(self._screen, Color.BLACK, rect, border_radius=6)
            pygame.draw.rect(self._screen, Color.WHITE, rect, width=2, border_radius=6)
            text_screen = self.instruction_font.render(text, True, Color.WHITE)
        
        self._screen.blit(text_screen, text_screen.get_rect(center=rect.center))
    
    def _adjust_speed(self, delta: int) -> None:
        """Adjust track speed by delta, clamping to valid range."""
        self._state.track_speed += delta
        self._state.track_speed = max(
            self.MIN_SPEED, 
            min(self.MAX_SPEED, self._state.track_speed)
        )
       
    def render(self, screen_pos) -> None:
        """Minimal render method - just blit pre-computed screens."""
        super().render(screen_pos)  # background and border

        # Title
        self._screen.blit(self.title_screen, self.title_rect)
        
        # Speed label
        self._screen.blit(self.speed_label_screen, self.speed_label_rect)
        
        # Speed buttons
        self._render_button(self.speed_minus_rect, self.minus_text, self.can_decrease_speed)
        self._render_button(self.speed_plus_rect, self.plus_text, self.can_increase_speed)
        
        # Speed value
        speed_val = f"{self._state.track_speed} km/h"
        speed_screen = self.instruction_font.render(speed_val, True, Color.YELLOW)
        self._screen.blit(speed_screen, speed_screen.get_rect(center=self.speed_center))
        
        # Length label
        self._screen.blit(self.length_label_screen, self.length_label_rect)
        
        # Length toggle buttons
        is_short = self._state.track_length == self.SHORT_LENGTH
        self._render_toggle_button(self.length_short_rect, "50 m", is_short)
        self._render_toggle_button(self.length_long_rect, "500 m", not is_short)
        
        # Tunnel label
        self._screen.blit(self.tunnel_label_screen, self.tunnel_label_rect)
        
        # Tunnel toggle buttons
        self._render_toggle_button(self.tunnel_no_rect, "No tunnel", not self._state.is_tunnel)
        self._render_toggle_button(self.tunnel_yes_rect, "Tunnel", self._state.is_tunnel)

    def _on_click(self, event: Event) -> bool:
        """Handle +/- clicks and length toggle; return True if the event was consumed."""     
        if not event.is_left_click:
            return self._rect.collidepoint(*event.screen_pos)
        
        # Speed controls
        if self.speed_minus_rect.collidepoint(*event.screen_pos) and self.can_decrease_speed:
            self._adjust_speed(-self.SPEED_INCREMENT)
            return True
        
        if self.speed_plus_rect.collidepoint(*event.screen_pos) and self.can_increase_speed:
            self._adjust_speed(self.SPEED_INCREMENT)
            return True
        
        # Length toggle
        if self.length_short_rect.collidepoint(*event.screen_pos):
            self._state.track_length = self.SHORT_LENGTH
            return True
        
        if self.length_long_rect.collidepoint(*event.screen_pos):
            self._state.track_length = self.LONG_LENGTH
            return True
        
        # Tunnel toggle
        if self.tunnel_no_rect.collidepoint(*event.screen_pos):
            self._state.is_tunnel = False
            return True
        
        if self.tunnel_yes_rect.collidepoint(*event.screen_pos):
            self._state.is_tunnel = True
            return True
        
        return self._rect.collidepoint(*event.screen_pos)