
from controllers.camera_controller import CameraController
from ui.models.ui_component import UIComponent
from controllers.construction.construction_controller import ConstructionController
from ui.construction.construction_buttons import ConstructionButtons
from controllers.construction.panel_strategy import ConstructionPanelStrategy
from models.construction_state import ConstructionState
from models.railway_system import RailwaySystem
from graphics.graphics_context import GraphicsContext
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