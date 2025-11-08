from core.graphics.graphics_context import GraphicsContext
from modules.setup.controllers.setup_controller import SetupController
from shared.ui.models.clickable_component import ClickableComponent
from shared.ui.models.ui_controller import UIController
from shared.controllers.camera_controller import CameraController
from core.models.railway.railway_system import RailwaySystem
from modules.setup.models.setup_state import SetupState

class SetupMode(UIController):
    elements: tuple[ClickableComponent]
    def __init__(self, railway: RailwaySystem, graphics: GraphicsContext):
        self.state = SetupState()
        self.elements = (
            CameraController(graphics.camera),
            SetupController(railway, self.state, graphics),
        )