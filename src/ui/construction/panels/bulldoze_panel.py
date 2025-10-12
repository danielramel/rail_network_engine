import pygame
from config.colors import WHITE, YELLOW
from models.construction import ConstructionState
from ui.components.panel import Panel
    
class BulldozePanel(Panel):
    """Bulldoze panel with instructions."""
    
    def __init__(self, surface: pygame.Surface, state: ConstructionState) -> None:
        super().__init__(surface)
        
        self._construction_state = state
        
        self.padding: int = 15
        
        # Initialize fonts
        self.title_font = pygame.font.SysFont(None, 28)
        self.instruction_font = pygame.font.SysFont(None, 22)
        
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

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Return True if event is within panel bounds."""
        pos = event.screen_pos
        return self._rect.collidepoint(*pos)