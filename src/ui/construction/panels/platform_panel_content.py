import pygame
from config.colors import WHITE, YELLOW

class PlatformPanelContent:
    """Platform control panel with no additional options.
    """
    def __init__(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        self.padding: int = 15
        self._surface = surface
        self._rect = rect
        
        # Initialize fonts
        self.title_font = pygame.font.SysFont(None, 28)
        self.data_font = pygame.font.SysFont(None, 22)
        
        # Pre-render static text
        self.title_surface = self.title_font.render("Platform Control", True, YELLOW)
        self.label_surface = self.data_font.render("Click to place platform.", True, WHITE)

        # Calculate and store all layout rects
        self._init_layout()
       
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
        
    def draw(self, mode_info: dict) -> None:
        """Minimal draw method - just blit pre-computed surfaces."""
        # Title
        self._surface.blit(self.title_surface, self.title_rect)
        
        # Label
        self._surface.blit(self.label_surface, self.label_rect)