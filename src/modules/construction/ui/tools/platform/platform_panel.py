import pygame
from core.config.color import Color
from core.config.settings import Settings
from modules.construction.models.construction_state import ConstructionState
from modules.construction.models.construction_panel import ConstructionToolPanel
from core.models.event import Event

    
class PlatformPanel(ConstructionToolPanel):
    """Platform placement panel with instructions."""
    
    # Platform length configuration constants
    MIN_LENGTH = 2
    MAX_LENGTH = 10
    LENGTH_INCREMENT = 1
    
    def __init__(self, surface: pygame.Surface, state: ConstructionState) -> None:
        super().__init__(surface, state)
        
        self.button_size: int = 32
        
        # Pre-render static text
        self.title_surface = self.title_font.render("Platform Placement", True, Color.YELLOW)
        self.instruction1_surface = self.instruction_font.render(
            "Click on rail to place platform, then", True, Color.WHITE
        )
        self.instruction2_surface = self.instruction_font.render(
            "connect it to already existing station.", True, Color.WHITE
        )
        self.length_label_surface = self.instruction_font.render("Platform length:", True, Color.WHITE)
        self.minus_text = self.instruction_font.render("-", True, Color.WHITE)
        self.plus_text = self.instruction_font.render("+", True, Color.WHITE)
        
        # Calculate and store all layout rects
        self._init_layout()
    
    @property
    def can_decrease_length(self) -> bool:
        """Check if length can be decreased."""
        return self._state.platform_edge_count > self.MIN_LENGTH
    
    @property
    def can_increase_length(self) -> bool:
        """Check if length can be increased."""
        return self._state.platform_edge_count < self.MAX_LENGTH
       
    def _init_layout(self) -> None:
        """Compute and persist all rects for layout."""
        # Title position
        self.title_rect = self.title_surface.get_rect(
            centerx=self._rect.centerx, 
            top=self._rect.top + self.padding
        )
        
        # Instruction positions
        self.instruction1_rect = self.instruction1_surface.get_rect(
            left=self._rect.left + self.padding,
            top=self.title_rect.bottom + 20
        )
        
        self.instruction2_rect = self.instruction2_surface.get_rect(
            left=self._rect.left + self.padding,
            top=self.instruction1_rect.bottom + 5
        )
        
        # Length label position
        self.length_label_rect = self.length_label_surface.get_rect(
            left=self._rect.left + self.padding,
            top=self.instruction2_rect.bottom + 20
        )
        
        # Length button positions
        length_button_y = self.length_label_rect.top - 4
        length_minus_x = self.length_label_rect.right + 20
        length_plus_x = length_minus_x + self.button_size + 80
        
        self.length_minus_rect = pygame.Rect(length_minus_x, length_button_y, self.button_size, self.button_size)
        self.length_plus_rect = pygame.Rect(length_plus_x, length_button_y, self.button_size, self.button_size)
        
        # Length value position (center between buttons)
        self.length_center = (self.length_minus_rect.right + 40, self.length_minus_rect.centery)
    
    def _render_button(self, rect: pygame.Rect, text_surface: pygame.Surface, enabled: bool) -> None:
        """Render a button with consistent styling."""
        if enabled:
            pygame.draw.rect(self._surface, Color.BLACK, rect, border_radius=6)
            pygame.draw.rect(self._surface, Color.WHITE, rect, width=2, border_radius=6)
            self._surface.blit(text_surface, text_surface.get_rect(center=rect.center))
    
    def _adjust_length(self, delta: int) -> None:
        """Adjust platform length by delta, clamping to valid range."""
        self._state.platform_edge_count += delta
        self._state.platform_edge_count = max(
            self.MIN_LENGTH, 
            min(self.MAX_LENGTH, self._state.platform_edge_count)
        )
       
    def render(self, screen_pos) -> None:
        """Render panel with instructions."""
        super().render(screen_pos)  # background and border

        # Title
        self._surface.blit(self.title_surface, self.title_rect)
        
        # Instructions
        self._surface.blit(self.instruction1_surface, self.instruction1_rect)
        self._surface.blit(self.instruction2_surface, self.instruction2_rect)
        
        # Length label
        self._surface.blit(self.length_label_surface, self.length_label_rect)
        
        # Length buttons
        self._render_button(self.length_minus_rect, self.minus_text, self.can_decrease_length)
        self._render_button(self.length_plus_rect, self.plus_text, self.can_increase_length)
        
        # Length value
        length_val = f"{self._state.platform_edge_count * Settings.SHORT_SEGMENT_LENGTH} m"
        length_surface = self.instruction_font.render(length_val, True, Color.YELLOW)
        self._surface.blit(length_surface, length_surface.get_rect(center=self.length_center))
    
    def _on_click(self, event: Event) -> bool:
        """Handle +/- clicks; return True if the event was consumed."""     
        if not event.is_left_click:
            return self._rect.collidepoint(*event.screen_pos)
        
        # Length controls
        if self.length_minus_rect.collidepoint(*event.screen_pos) and self.can_decrease_length:
            self._adjust_length(-self.LENGTH_INCREMENT)
            return True
        
        if self.length_plus_rect.collidepoint(*event.screen_pos) and self.can_increase_length:
            self._adjust_length(self.LENGTH_INCREMENT)
            return True
        
        return self._rect.collidepoint(*event.screen_pos)