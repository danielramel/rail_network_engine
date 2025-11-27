import pygame
from modules.setup.train_placement.ui.tools.train_adder.train_adder_panel import TrainAdderPanel
from modules.setup.train_placement.ui.tools.train_removal.train_removal_panel import TrainRemovalPanel
from shared.ui.models.panel import Panel
from modules.setup.train_placement.models.train_placement_state import TrainPlacementState, TrainPlacementTool

class TrainPlacementPanelStrategy(Panel):
    def __init__(self, screen: pygame.Surface, state: TrainPlacementState):
        self._state = state
        self._panels: dict[TrainPlacementTool, Panel] = {
            TrainPlacementTool.PLACE_TRAIN: TrainAdderPanel(screen, state),
            TrainPlacementTool.REMOVE_TRAIN: TrainRemovalPanel(screen),
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