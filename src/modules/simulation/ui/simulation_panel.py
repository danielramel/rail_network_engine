from shared.ui.models.panel import Panel
import pygame
from modules.simulation.models.simulation_state import SimulationState

class SimulationPanel(Panel):
    def __init__(self, simulation_state: SimulationState, surface:pygame.Surface):
        self._state = simulation_state
        super().__init__(surface)
    
    def contains(self, screen_pos):
        if self._state.selected_train is None:
            return False
        
        super().contains(screen_pos)
        
    def render(self, screen_pos):
        if self._state.selected_train is None:
            return False
        
        super().render(screen_pos)
            