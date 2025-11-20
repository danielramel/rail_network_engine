from core.graphics.graphics_context import GraphicsContext
from modules.setup.ui.setup_buttons import SetupButtons
from modules.setup.ui.setup_panel_strategy import SetupPanelStrategy
from modules.setup.ui.setup_tool_strategy import SetupToolStrategy
from shared.ui.components.time_display import TimeDisplay
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent
from shared.ui.models.ui_component import UIComponent
from shared.ui.models.ui_controller import UIController
from shared.controllers.camera_controller import CameraController
from core.models.railway.railway_system import RailwaySystem
from modules.setup.models.setup_state import SetupState
from core.models.time import Time

class SetupMode(FullScreenUIComponent, UIController):
    elements: tuple[UIComponent]
    def __init__(self, railway: RailwaySystem, graphics: GraphicsContext, time: Time):
        railway.signals.add_signals_to_dead_ends()
        
        self.state = SetupState(time)
        self.elements = (
            TimeDisplay(self.state.time, graphics, modifiable=True),
            SetupButtons(graphics.screen, self.state),
            SetupPanelStrategy(graphics.screen, self.state),
            CameraController(graphics.camera),
            SetupToolStrategy(railway, self.state, graphics),
        )