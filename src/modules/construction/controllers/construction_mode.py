
from shared.controllers.camera_controller import CameraController
from modules.construction.controllers.construction_tool_strategy import ConstructionToolStrategy
from modules.construction.ui.construction_buttons import ConstructionButtons
from modules.construction.controllers.construction_panel_strategy import ConstructionPanelStrategy
from modules.construction.models.construction_state import ConstructionState
from core.models.railway.railway_system import RailwaySystem
from core.graphics.graphics_context import GraphicsContext
from shared.ui.models.ui_controller import UIController
from shared.ui.models.ui_component import UIComponent


class ConstructionMode(UIController):
    elements: tuple[UIComponent]
    def __init__(self, railway: RailwaySystem, graphics: GraphicsContext):
        self.state = ConstructionState()
        self.elements = (
            ConstructionButtons(graphics.screen, self.state),
            ConstructionPanelStrategy(graphics.screen, self.state),
            CameraController(graphics.camera),
            ConstructionToolStrategy(railway, self.state, graphics)
        )