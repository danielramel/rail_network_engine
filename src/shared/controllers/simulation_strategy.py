from core.models.app_state import AppState, AppPhase
from core.models.railway.railway_system import RailwaySystem
from core.graphics.graphics_context import GraphicsContext
from core.models.geometry.position import Position
from modules.setup.setup_mode import SetupMode
from modules.simulation.simulation_mode import SimulationMode
from shared.ui.models.ui_controller import UIController
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent
from typing import Optional

class SimulationStrategy(FullScreenUIComponent):
    def __init__(self, app_state: AppState, railway: RailwaySystem, graphics: GraphicsContext):
        self._state = app_state
        app_state.subscribe(self.switch_to)
        
        self._modes: dict[AppPhase, lambda: UIController] = {
            AppPhase.SETUP: lambda: SetupMode(app_state, railway, graphics),
            AppPhase.SIMULATION: lambda: SimulationMode(railway, graphics, lambda: app_state.switch_phase(AppPhase.SETUP)),
            }
        
        self._current_mode: UIController = self._modes[app_state.phase]()
        
    
    def switch_to(self, phase: AppPhase):
        self._current_mode = self._modes[phase]()
        
    def handle_event(self, event) -> bool:        
        self._current_mode.dispatch_event(event)
        
    def render(self, screen_pos: Optional[Position]):
        self._current_mode.render(screen_pos)
        
    def tick(self):
        self._current_mode.tick()