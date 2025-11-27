from shared.controllers.camera_controller import CameraController
from shared.ui.components.zoom_button import ZoomButton
from shared.ui.models.ui_component import UIComponent
from shared.ui.models.ui_controller import UIController
from core.models.railway.railway_system import RailwaySystem
from core.graphics.graphics_context import GraphicsContext
from modules.setup.construction.ui.construction_tool_strategy import ConstructionToolStrategy
from modules.setup.construction.ui.construction_buttons import ConstructionButtons
from modules.setup.construction.ui.construction_panel_strategy import ConstructionPanelStrategy
from modules.setup.construction.models.construction_state import ConstructionState
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent


class ConstructionMode(UIController, FullScreenUIComponent):
    elements: tuple[UIComponent]
    def __init__(self, railway: RailwaySystem, graphics: GraphicsContext):
        self.state = ConstructionState()
        self.elements = (
            ConstructionButtons(graphics.screen, self.state),
            ConstructionPanelStrategy(graphics.screen, self.state),
            ZoomButton(graphics.screen, graphics.camera),
            CameraController(graphics.camera),
            ConstructionToolStrategy(railway, self.state, graphics)
        )