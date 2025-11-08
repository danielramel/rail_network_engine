from core.graphics.graphics_context import GraphicsContext
from modules.setup.ui.setup_buttons import SetupButtons
from modules.setup.ui.setup_controller import SetupController
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent
from shared.ui.models.ui_component import UIComponent
from shared.ui.models.ui_controller import UIController
from shared.controllers.camera_controller import CameraController
from core.models.railway.railway_system import RailwaySystem
from modules.setup.models.setup_state import SetupState

class SetupMode(FullScreenUIComponent, UIController):
    elements: tuple[UIComponent]
    def __init__(self, railway: RailwaySystem, graphics: GraphicsContext):
        self.state = SetupState()
        self.elements = (
            SetupButtons(graphics.screen, self.state),
            CameraController(graphics.camera),
            SetupController(railway, self.state, graphics),
        )