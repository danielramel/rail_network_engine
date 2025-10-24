import pygame
from models.construction import ConstructionState
from ui.models.panel import Panel

class BaseConstructionPanel(Panel):
    """Base class for construction panels."""
    
    def __init__(self, surface: pygame.Surface, state: ConstructionState) -> None:
        super().__init__(surface)
        
        self._construction_state = state
        
        self.padding: int = 15
        self.title_font = pygame.font.SysFont(None, 28)
        self.instruction_font = pygame.font.SysFont(None, 22)