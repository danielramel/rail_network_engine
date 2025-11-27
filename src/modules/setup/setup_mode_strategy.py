from modules.setup.construction.construction_mode import ConstructionMode 
from modules.setup.setup_state import SetupState, SetupView
from modules.setup.train_placement.train_placement_mode import TrainPlacementMode
from core.models.railway.railway_system import RailwaySystem
from core.graphics.graphics_context import GraphicsContext
from core.models.geometry.position import Position

from shared.ui.models.ui_controller import UIController
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent


class SetupModeStrategy(FullScreenUIComponent):
    def __init__(self, setup_state: SetupState, railway: RailwaySystem, graphics: GraphicsContext):
        self._state = setup_state
        setup_state.subscribe(self.switch_to)
        self._current_mode: UIController = None
        
        self._modes: dict[SetupView, lambda: UIController] = {
            SetupView.CONSTRUCTION: lambda: ConstructionMode(railway, graphics),
            SetupView.TRAIN_PLACEMENT: lambda: TrainPlacementMode(railway, graphics),
            }
        
        self._current_mode = self._modes[setup_state.current_view]()
        
    
    def switch_to(self, new_mode: SetupView):
        self._current_mode = self._modes[new_mode]()
        
    def handle_event(self, event) -> bool:
        self._current_mode.dispatch_event(event)
        
    def render(self, screen_pos: Position | None):
        self._current_mode.render(screen_pos)
        
    def tick(self):
        self._current_mode.tick()