import pygame
from core.models.app_state import ViewMode
from modules.construction.construction_state import ConstructionMode
from modules.simulation.simulation_state import TimeControlMode
        
MODE_SELECTION = {
    pygame.K_s: ViewMode.SIMULATION,
    pygame.K_c: ViewMode.CONSTRUCTION,
}

CONSTRUCTION_MODE_SELECTION = {
    pygame.K_1: ConstructionMode.RAIL,
    pygame.K_2: ConstructionMode.SIGNAL,
    pygame.K_3: ConstructionMode.STATION,
    pygame.K_4: ConstructionMode.PLATFORM,
    pygame.K_5: ConstructionMode.BULLDOZE,
}

TIME_CONTROL_KEYS = {
    pygame.K_SPACE: "handled_separately",
    pygame.K_1: TimeControlMode.PAUSE,
    pygame.K_2: TimeControlMode.PLAY,
    pygame.K_3: TimeControlMode.FAST_FORWARD,
    pygame.K_4: TimeControlMode.SUPER_FAST_FORWARD,
}