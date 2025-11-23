import pygame
from shared.ui.models.panel import Panel
from modules.construction.models.construction_state import ConstructionState

class ConstructionToolPanel(Panel):
    """Base class for construction panels."""
    
    def __init__(self, screen: pygame.Surface, state: ConstructionState, **kwargs) -> None:
        super().__init__(screen, **kwargs)
        
        self._state = state