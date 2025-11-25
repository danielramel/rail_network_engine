from modules.construction.construction_mode import ConstructionMode 
from modules.setup.setup_mode import SetupMode
from modules.simulation.simulation_mode import SimulationMode
from core.models.app_state import AppState, ViewMode
from core.models.railway.railway_system import RailwaySystem
from core.graphics.graphics_context import GraphicsContext
from core.models.geometry.position import Position

from shared.ui.models.ui_controller import UIController
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent


class ModeStrategy(FullScreenUIComponent):
    def __init__(self, app_state: AppState, railway: RailwaySystem, graphics: GraphicsContext):
        self._state = app_state
        app_state.subscribe(self.switch_to)
        self._current_mode: UIController = None
        
        self._modes: dict[ViewMode, lambda: UIController] = {
            ViewMode.CONSTRUCTION: lambda: ConstructionMode(railway, graphics),
            ViewMode.SETUP: lambda: SetupMode(railway, graphics),
            ViewMode.SIMULATION: lambda: SimulationMode(railway, graphics)
        }
        
        self.switch_to(app_state.mode)
    
    def switch_to(self, new_mode: ViewMode):
        self._current_mode = self._modes[new_mode]()
        
    def handle_event(self, event) -> bool:
        if self._current_mode is None:
            return False
        
        self._current_mode.dispatch_event(event)
        
    def render(self, screen_pos: Position | None):
        if self._current_mode is None:
            return
        
        self._current_mode.render(screen_pos)
        
    def tick(self):
        self._current_mode.tick()