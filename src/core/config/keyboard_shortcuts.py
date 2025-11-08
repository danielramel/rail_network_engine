import pygame
from core.models.app_state import ViewMode
from modules.construction.models.construction_state import ConstructionTool
from modules.simulation.models.simulation_state import TimeControlMode
        
MODE_SELECTION = {
    pygame.K_s: ViewMode.SETUP,
    pygame.K_c: ViewMode.CONSTRUCTION,
    pygame.K_p: ViewMode.SIMULATION,
}
CONSTRUCTION_MODE_SELECTION = {
    pygame.K_1: ConstructionTool.RAIL,
    pygame.K_2: ConstructionTool.SIGNAL,
    pygame.K_3: ConstructionTool.STATION,
    pygame.K_4: ConstructionTool.PLATFORM,
    pygame.K_5: ConstructionTool.BULLDOZE,
}

TIME_CONTROL_KEYS = {
    pygame.K_1: TimeControlMode.PAUSE,
    pygame.K_2: TimeControlMode.PLAY,
    pygame.K_3: TimeControlMode.FAST_FORWARD,
    pygame.K_4: TimeControlMode.SUPER_FAST_FORWARD,
    pygame.K_SPACE: "toggle_pause",
}