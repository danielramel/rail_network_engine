import pygame
from core.config.colors import WHITE, YELLOW
from modules.construction.models.construction_state import ConstructionState
from modules.construction.ui.panels.base_construction_panel import BaseConstructionPanel
    
class StationPanel(BaseConstructionPanel):
    """Station placement panel with instructions."""
    
    def __init__(self, surface: pygame.Surface, state: ConstructionState) -> None:
        super().__init__(surface, state)
        # Pre-render static text
        self.title_surface = self.title_font.render("Station Placement", True, YELLOW)
        self.instruction1_surface = self.instruction_font.render(
            "Click to place station.", True, WHITE
        )
        self.instruction2_surface = self.instruction_font.render(
            "Click on station to move it.", True, WHITE
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
        
        self.instruction2_rect = self.instruction2_surface.get_rect(
            left=self._rect.left + self.padding,
            top=self.instruction1_rect.bottom + 5
        )
       
    def render(self, screen_pos) -> None:
        """Render panel with instructions."""
        super().render(screen_pos)  # background and border

        # Title
        self._surface.blit(self.title_surface, self.title_rect)
        
        # Instructions
        self._surface.blit(self.instruction1_surface, self.instruction1_rect)
        self._surface.blit(self.instruction2_surface, self.instruction2_rect)