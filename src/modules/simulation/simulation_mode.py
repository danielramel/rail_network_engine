from core.graphics.graphics_context import GraphicsContext
from shared.ui.models.clickable_component import ClickableComponent
from shared.ui.models.ui_controller import UIController
from modules.simulation.ui.time_control_buttons import TimeControlButtons
from modules.simulation.ui.time_display import TimeDisplay
from shared.controllers.camera_controller import CameraController
from modules.simulation.controllers.simulation_controller import SimulationController
from core.models.railway.railway_system import RailwaySystem
from modules.simulation.models.simulation_state import SimulationState

class SimulationMode(UIController):
    elements: tuple[ClickableComponent]
    def __init__(self, railway: RailwaySystem, graphics: GraphicsContext):
        self.state = SimulationState()
        self.elements = (
            TimeControlButtons(self.state.time, graphics.screen),
            TimeDisplay(self.state.time, graphics.screen),
            CameraController(graphics.camera),
            SimulationController(railway, self.state, graphics),
        )