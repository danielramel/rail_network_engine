from core.graphics.graphics_context import GraphicsContext
from modules.simulation.ui.panel.train_panel_manager import TrainPanelManager
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from shared.ui.models.ui_controller import UIController
from modules.simulation.ui.time_control_buttons import TimeControlButtons
from shared.ui.components.time_display import TimeDisplay
from shared.controllers.camera_controller import CameraController
from modules.simulation.ui.simulation_controller import SimulationController
from core.models.railway.railway_system import RailwaySystem
from modules.simulation.models.simulation_state import SimulationState
from core.models.time import Time

class SimulationMode(UIController, FullScreenUIComponent):
    elements: tuple[ClickableUIComponent]
    def __init__(self, railway: RailwaySystem, graphics: GraphicsContext, time: Time):
        railway.signals.add_signals_to_dead_ends()
        
                
        self._state = SimulationState(time)
        
        self.elements = (
            TimeControlButtons(self._state.time_control, graphics.screen),
            TimeDisplay(self._state.time, graphics),
            TrainPanelManager(railway, self._state, graphics.screen, railway.schedules),
            CameraController(graphics.camera),
            SimulationController(railway, self._state, graphics),
        )