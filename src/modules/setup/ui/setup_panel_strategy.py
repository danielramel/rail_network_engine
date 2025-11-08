import pygame
from modules.setup.ui.tools.train_placement.train_placement_panel import TrainPlacementPanel
from modules.setup.ui.tools.train_removal.train_removal_panel import TrainRemovalPanel
from shared.ui.models.panel import Panel
from modules.setup.models.setup_state import SetupState, SetupTool

class SetupPanelStrategy(Panel):
    def __init__(self, screen: pygame.Surface, state: SetupState):
        self._state = state
        self._panels: dict[SetupTool, Panel] = {
            SetupTool.PLACE_TRAIN: TrainPlacementPanel(screen),
            SetupTool.REMOVE_TRAIN: TrainRemovalPanel(screen),
        }

    def render(self, screen_pos):
        if self._state.tool is None:
            return
        self._panels[self._state.tool].render(screen_pos)

    def _on_click(self, event):
        if self._state.tool is None:
            return
        return self._panels[self._state.tool].dispatch_event(event)
    
    def contains(self, screen_pos):
        if self._state.tool is None:
            return False
        return self._panels[self._state.tool].contains(screen_pos)