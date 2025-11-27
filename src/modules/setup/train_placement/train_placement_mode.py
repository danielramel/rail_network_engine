from core.graphics.graphics_context import GraphicsContext
from modules.setup.train_placement.ui.train_placement_buttons import TrainPlacementButtons
from modules.setup.train_placement.ui.train_placement_panel_strategy import TrainPlacementPanelStrategy
from modules.setup.train_placement.ui.train_placement_tool_strategy import TrainPlacementToolStrategy
from shared.ui.components.time_display import TimeDisplay
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent
from shared.ui.models.ui_component import UIComponent
from shared.ui.models.ui_controller import UIController
from shared.controllers.camera_controller import CameraController
from core.models.railway.railway_system import RailwaySystem
from modules.setup.train_placement.models.train_placement_state import TrainPlacementState

class TrainPlacementMode(FullScreenUIComponent, UIController):
    elements: tuple[UIComponent]
    def __init__(self, railway: RailwaySystem, graphics: GraphicsContext):        
        self.state = TrainPlacementState(railway.time)
        self.elements = (
            TrainPlacementButtons(graphics.screen, self.state),
            TrainPlacementPanelStrategy(graphics.screen, self.state),
            CameraController(graphics.camera),
            TrainPlacementToolStrategy(railway, self.state, graphics),
        )