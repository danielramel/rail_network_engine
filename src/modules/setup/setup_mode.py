from core.graphics.graphics_context import GraphicsContext
from modules.setup.controllers.setup_controller import SetupController
from shared.ui.models.ui_component import UIComponent
from shared.ui.models.ui_controller import UIController
from shared.controllers.camera_controller import CameraController
from core.models.railway.railway_system import RailwaySystem
from modules.simulation.models.simulation_state import SimulationState

class SetupMode(UIController):
    elements: tuple[UIComponent]
    def __init__(self, railway: RailwaySystem, graphics: GraphicsContext):
        self.state = SimulationState()
        self.elements = (
            CameraController(graphics.camera),
            SetupController(railway, graphics),
        )