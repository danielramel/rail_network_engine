import pygame
from modules.construction.models.construction_state import ConstructionState
from core.config.colors import WHITE, YELLOW
from modules.construction.models.construction_panel import ConstructionToolPanel
    
class BulldozePanel(ConstructionToolPanel):
    """Bulldoze panel with instructions."""
    
    def __init__(self, surface: pygame.Surface, state: ConstructionState) -> None:
        super().__init__(surface, state)
        
        # Pre-render static text
        self.title_surface = self.title_font.render("Bulldoze", True, YELLOW)
        self.instruction_surface = self.instruction_font.render(
            "Click on element to remove it.", True, WHITE
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
        
        # Instruction position
        self.instruction_rect = self.instruction_surface.get_rect(
            left=self._rect.left + self.padding,
            top=self.title_rect.bottom + 20
        )
       
    def render(self, screen_pos) -> None:
        """Render panel with instructions."""
        super().render(screen_pos)  # background and border

        # Title
        self._surface.blit(self.title_surface, self.title_rect)
        
        # Instruction
        self._surface.blit(self.instruction_surface, self.instruction_rect)