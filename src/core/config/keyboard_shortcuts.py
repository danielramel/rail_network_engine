import pygame
        
from core.models.app_state import ViewMode
MODE_SELECTION = {
    pygame.K_s: ViewMode.SETUP,
    pygame.K_c: ViewMode.CONSTRUCTION,
    pygame.K_p: ViewMode.SIMULATION,
}

from modules.construction.models.construction_state import ConstructionTool
CONSTRUCTION_TOOL_SELECTION = {
    pygame.K_1: ConstructionTool.RAIL,
    pygame.K_2: ConstructionTool.SIGNAL,
    pygame.K_3: ConstructionTool.STATION,
    pygame.K_4: ConstructionTool.PLATFORM,
    pygame.K_0: ConstructionTool.BULLDOZE,
}


from modules.simulation.models.simulation_state import TimeControlMode
TIME_CONTROL_KEYS = {
    pygame.K_1: TimeControlMode.PAUSE,
    pygame.K_2: TimeControlMode.PLAY,
    pygame.K_3: TimeControlMode.FAST_FORWARD,
    pygame.K_4: TimeControlMode.SUPER_FAST_FORWARD,
    pygame.K_SPACE: "toggle_pause",
}

from modules.setup.models.setup_state import SetupTool
SETUP_TOOL_SELECTION = {
    pygame.K_1: SetupTool.PLACE_TRAIN,
    pygame.K_2: SetupTool.REMOVE_TRAIN,
}