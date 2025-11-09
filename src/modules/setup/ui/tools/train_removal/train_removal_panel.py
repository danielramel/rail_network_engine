import pygame
from core.config.color import Color
from shared.ui.models.panel import Panel
    
class TrainRemovalPanel(Panel):
    """Signal placement panel with instructions."""
    
    def __init__(self, surface: pygame.Surface) -> None:
        super().__init__(surface)
        
        # Pre-render static text
        self.title_surface = self.title_font.render("Train Removal", True, Color.YELLOW)
        self.instruction1_surface = self.instruction_font.render(
            "Click on rail to remove train.", True, Color.WHITE
        )
        
        # Calculate and store all layout rects
        self._init_layout()
       
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
       
    def render(self, screen_pos) -> None:
        """Render panel with instructions."""
        super().render(screen_pos)  # background and border

        # Title
        self._surface.blit(self.title_surface, self.title_rect)
        
        # Instructions
        self._surface.blit(self.instruction1_surface, self.instruction1_rect)