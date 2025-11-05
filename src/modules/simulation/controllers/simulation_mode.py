from models.railway_system import RailwaySystem
from graphics.graphics_context import GraphicsContext
from models.simulation_state import SimulationState
from ui.models.ui_component import UIComponent
from ui.models.ui_controller import UIController
from ui.simulation.time_control_buttons import TimeControlButtons
from ui.train_placement_button import TrainPlacementButton
from ui.simulation.time_display import TimeDisplay
from controllers.camera_controller import CameraController
from modules.simulation.controllers.simulation_controller import SimulationController

class SimulationMode(UIController):
    elements: tuple[UIComponent]
    def __init__(self, railway: RailwaySystem, graphics: GraphicsContext):
        self.state = SimulationState()
        self.elements = (
            TimeControlButtons(self.state.time, graphics.screen),
            TrainPlacementButton(railway, graphics.screen),
            TimeDisplay(self.state.time, graphics.screen),
            CameraController(graphics.camera),
            SimulationController(railway, self.state, graphics),
        )