
from shared.controllers.camera_controller import CameraController
from shared.ui.components import UIComponent
from modules.construction.controllers.construction_controller import ConstructionController
from modules.construction.ui.construction_buttons import ConstructionButtons
from modules.construction.controllers.construction_panel_strategy import ConstructionPanelStrategy
from modules.construction.construction_state import ConstructionState
from core.models.railway import RailwaySystem
from core.graphics import GraphicsContext
from ui.models.ui_controller import UIController

class ConstructionMode(UIController):
    elements: tuple[UIComponent]
    def __init__(self, railway: RailwaySystem, graphics: GraphicsContext):
        self.state = ConstructionState()
        self.elements = (
            ConstructionButtons(graphics.screen, self.state),
            ConstructionPanelStrategy(graphics.screen, self.state),
            CameraController(graphics.camera),
            ConstructionController(railway, self.state, graphics)
        )