import pygame
from shared.ui.models.panel import Panel
from modules.construction.models.construction_state import ConstructionState

class ConstructionToolPanel(Panel):
    """Base class for construction panels."""
    
    def __init__(self, surface: pygame.Surface, state: ConstructionState) -> None:
        super().__init__(surface)
        
        self._state = state