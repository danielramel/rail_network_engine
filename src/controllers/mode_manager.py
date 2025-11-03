from controllers.construction.construction_mode import ConstructionMode 
from controllers.simulation.simulation_mode import SimulationMode
from models.app_state import AppState, ViewMode
from models.railway_system import RailwaySystem
from graphics.graphics_context import GraphicsContext
from models.geometry import Position

from ui.models.ui_component import UIComponent
from ui.models.ui_handler import UILayer


class ModeController(UIComponent):
    def __init__(self, app_state: AppState, railway: RailwaySystem, graphics: GraphicsContext):
        self._state = app_state
        app_state.subscribe(self.switch_to)
        self._current_mode: UILayer = None
        
        self._modes: dict[ViewMode, lambda: UILayer] = {
            ViewMode.CONSTRUCTION: lambda: ConstructionMode(railway, graphics),
            ViewMode.SIMULATION: lambda: SimulationMode(railway, graphics)
        }
        
        self.switch_to(app_state.mode)
    
    def switch_to(self, new_mode: ViewMode):
        self._current_mode = self._modes[new_mode]()
        
        
    def _handle_filtered_event(self, event) -> bool:            
        if self._current_mode is None:
            return False
        
        self._current_mode.handle_event(event)
        
    def render(self, screen_pos: Position | None):
        if self._current_mode is None:
            return
        
        self._current_mode.render(screen_pos)