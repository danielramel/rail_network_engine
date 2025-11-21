import pygame
from core.config.color import Color
from modules.construction.models.construction_state import ConstructionState
from modules.construction.models.construction_panel import ConstructionToolPanel
    
class SignalPanel(ConstructionToolPanel):
    """Signal placement panel with instructions."""
    
    def __init__(self, screen: pygame.Surface, state: ConstructionState) -> None:
        super().__init__(screen, state)
        
        # Pre-render static text
        self.title_screen = self.title_font.render("Signal Placement", True, Color.YELLOW)
        self.instruction1_screen = self.instruction_font.render(
            "Click on rail to place signal.", True, Color.WHITE
        )
        self.instruction2_screen = self.instruction_font.render(
            "Click again to toggle direction.", True, Color.WHITE
        )
        
        # Calculate and store all layout rects
        self._init_layout()
       
    def _init_layout(self) -> None:
        """Compute and persist all rects for layout."""
        # Title position
        self.title_rect = self.title_screen.get_rect(
            centerx=self._rect.centerx, 
            top=self._rect.top + self.padding
        )
        
        # Instruction positions
        self.instruction1_rect = self.instruction1_screen.get_rect(
            left=self._rect.left + self.padding,
            top=self.title_rect.bottom + 20
        )
        
        self.instruction2_rect = self.instruction2_screen.get_rect(
            left=self._rect.left + self.padding,
            top=self.instruction1_rect.bottom + 5
        )
       
    def render(self, screen_pos) -> None:
        """Render panel with instructions."""
        super().render(screen_pos)  # background and border

        # Title
        self._screen.blit(self.title_screen, self.title_rect)
        
        # Instructions
        self._screen.blit(self.instruction1_screen, self.instruction1_rect)
        self._screen.blit(self.instruction2_screen, self.instruction2_rect)