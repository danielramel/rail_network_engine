import pygame
from core.config.color import Color
from core.config.config import Config
from modules.setup.construction.models.construction_state import ConstructionState
from modules.setup.construction.models.construction_panel import ConstructionToolPanel
from core.models.event import Event
    
class TrackPanel(ConstructionToolPanel):    
    def __init__(self, screen: pygame.Surface, state: ConstructionState) -> None:
        super().__init__(screen, state)
        
        self.button_size: int = 32
        self._hovered_rect: pygame.Rect | None = None
        
        # Pre-render static text
        self.title_screen = self.title_font.render("Track Construction", True, Color.YELLOW)
        self.speed_label_screen = self.instruction_font.render("Track speed:", True, Color.WHITE)
        self.length_label_screen = self.instruction_font.render("Track length:", True, Color.WHITE)
        self.minus_text = self.instruction_font.render("-", True, Color.WHITE)
        self.plus_text = self.instruction_font.render("+", True, Color.WHITE)
        
        # Calculate and store all layout rects
        self._init_layout()
    
    @property
    def can_decrease_speed(self) -> bool:
        """Check if speed can be decreased."""
        return self._state.track_speed > Config.MIN_TRACK_SPEED
    
    @property
    def can_increase_speed(self) -> bool:
        """Check if speed can be increased."""
        return self._state.track_speed < Config.MAX_TRACK_SPEED
       
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
    
    def _render_button(self, rect: pygame.Rect, text_screen: pygame.Surface, enabled: bool) -> None:
        """Render a button with consistent styling."""
        if enabled:
            is_hovered = self._hovered_rect == rect
            bg_color = Color.DARKGREY if is_hovered else Color.BLACK
            pygame.draw.rect(self._screen, bg_color, rect, border_radius=6)
            pygame.draw.rect(self._screen, Color.WHITE, rect, width=2, border_radius=6)
            self._screen.blit(text_screen, text_screen.get_rect(center=rect.center))
    
    def _render_toggle_button(self, rect: pygame.Rect, text: str, is_selected: bool) -> None:
        """Render a toggle button with selected/unselected states."""
        is_hovered = self._hovered_rect == rect
        if is_selected:
            bg_color = Color.LIGHTGREY if is_hovered else Color.WHITE
            pygame.draw.rect(self._screen, bg_color, rect, border_radius=6)
            text_screen = self.instruction_font.render(text, True, Color.BLACK)
        else:
            bg_color = Color.DARKGREY if is_hovered else Color.BLACK
            pygame.draw.rect(self._screen, bg_color, rect, border_radius=6)
            pygame.draw.rect(self._screen, Color.WHITE, rect, width=2, border_radius=6)
            text_screen = self.instruction_font.render(text, True, Color.WHITE)
        
        self._screen.blit(text_screen, text_screen.get_rect(center=rect.center))
    
    def _adjust_speed(self, delta: int) -> None:
        """Adjust track speed by delta, clamping to valid range."""
        self._state.track_speed += delta
        self._state.track_speed = max(
            Config.MIN_TRACK_SPEED, 
            min(Config.MAX_TRACK_SPEED, self._state.track_speed)
        )
    
    def _update_hover_state(self, screen_pos) -> None:
        """Update which button is currently hovered."""
        self._hovered_rect = None
        if screen_pos is None:
            return
        for rect in [self.speed_minus_rect, self.speed_plus_rect, 
                     self.length_short_rect, self.length_long_rect]:
            if rect.collidepoint(*screen_pos):
                self._hovered_rect = rect
                break
       
    def render(self, screen_pos) -> None:
        """Minimal render method - just blit pre-computed screens."""
        super().render(screen_pos)  # background and border
        
        # Update hover state
        self._update_hover_state(screen_pos)

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
        is_short = self._state.track_length == Config.SHORT_SECTION_LENGTH
        self._render_toggle_button(self.length_short_rect, f"{Config.SHORT_SECTION_LENGTH} m", is_short)
        self._render_toggle_button(self.length_long_rect, f"{Config.LONG_SECTION_LENGTH} m", not is_short)

    def _on_click(self, event: Event) -> bool:
        """Handle +/- clicks and length toggle; return True if the event was consumed."""     
        if not event.is_left_click:
            return self._rect.collidepoint(*event.screen_pos)
        
        # Speed controls
        if self.speed_minus_rect.collidepoint(*event.screen_pos) and self.can_decrease_speed:
            self._adjust_speed(-Config.TRACK_SPEED_INCREMENT)
            return True
        
        if self.speed_plus_rect.collidepoint(*event.screen_pos) and self.can_increase_speed:
            self._adjust_speed(Config.TRACK_SPEED_INCREMENT)
            return True
        
        # Length toggle
        if self.length_short_rect.collidepoint(*event.screen_pos):
            self._state.track_length = Config.SHORT_SECTION_LENGTH
            return True
        
        if self.length_long_rect.collidepoint(*event.screen_pos):
            self._state.track_length = Config.LONG_SECTION_LENGTH
            return True
        
        return self._rect.collidepoint(*event.screen_pos)