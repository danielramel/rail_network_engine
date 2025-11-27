import pygame
        
from core.models.app_state import ViewMode
MODE_SELECTION = {
    pygame.K_s: ViewMode.TRAIN_PLACEMENT,
    pygame.K_c: ViewMode.CONSTRUCTION,
    pygame.K_p: ViewMode.SIMULATION,
}

from modules.construction.models.construction_state import ConstructionTool
CONSTRUCTION_TOOL_SELECTION = {
    pygame.K_1: ConstructionTool.RAIL,
    pygame.K_2: ConstructionTool.TUNNEL,
    pygame.K_3: ConstructionTool.SIGNAL,
    pygame.K_4: ConstructionTool.STATION,
    pygame.K_5: ConstructionTool.PLATFORM,
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

from modules.train_placement.models.train_placement_state import TrainPlacementTool
TRAIN_PLACEMENT_TOOL_SELECTION = {
    pygame.K_1: TrainPlacementTool.PLACE_TRAIN,
    pygame.K_2: TrainPlacementTool.REMOVE_TRAIN,
}