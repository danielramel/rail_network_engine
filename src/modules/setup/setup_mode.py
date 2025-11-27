from core.graphics.graphics_context import GraphicsContext
from core.models.app_state import AppState
from core.models.railway.railway_system import RailwaySystem
from modules.setup.setup_mode_strategy import SetupModeStrategy
from shared.ui.components.route_button import RouteButton
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent
from shared.ui.models.ui_component import UIComponent
from shared.ui.models.ui_controller import UIController
from shared.ui.components.exit_button import ExitButton
from shared.ui.components.open_button import OpenButton
from shared.ui.components.save_button import SaveButton
from shared.ui.components.mode_selector_buttons import ModeSelectorButtons
from shared.ui.components.zoom_button import ZoomButton

class SetupMode(UIController, FullScreenUIComponent):
    def __init__(self, app_state: AppState, railway: RailwaySystem, graphics: GraphicsContext):
        save_button = SaveButton(graphics.screen, railway, app_state)
        self.elements: list[UIComponent] = [
            RouteButton(graphics.screen, railway),
            ZoomButton(graphics.screen, graphics.camera),
            save_button,
            OpenButton(railway, app_state, graphics),
            ExitButton(railway, graphics, self._on_exit, save_button),
            ModeSelectorButtons(graphics, app_state),
            SetupModeStrategy(app_state, railway, graphics)
        ]
        
    def _on_exit(self):
        pass
        
