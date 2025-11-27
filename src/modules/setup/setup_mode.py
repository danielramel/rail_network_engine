from core.graphics.graphics_context import GraphicsContext
from core.models.app_state import AppPhase, AppState
from core.models.railway.railway_system import RailwaySystem
from modules.setup.setup_mode_strategy import SetupModeStrategy
from modules.setup.setup_state import SetupState
from modules.setup.ui.start_simulation_button import StartSimulationButton
from shared.ui.components.route_button import RouteButton
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent
from shared.ui.models.ui_component import UIComponent
from shared.ui.models.ui_controller import UIController
from modules.setup.ui.exit_button import ExitButton
from modules.setup.ui.open_button import OpenButton
from modules.setup.ui.save_button import SaveButton
from modules.setup.setup_mode_selector_buttons import SetupModeSelectorButtons
    

class SetupMode(UIController, FullScreenUIComponent):
    def __init__(self, app_state: AppState, railway: RailwaySystem, graphics: GraphicsContext):
        setup_state = SetupState(app_state)
        
        save_button = SaveButton(graphics.screen, railway, app_state)
        self.elements: list[UIComponent] = [
            RouteButton(graphics.screen, railway),
            save_button,
            OpenButton(railway, app_state, graphics),
            ExitButton(railway, graphics, app_state.exit, lambda: save_button.save_game()),
            StartSimulationButton(graphics.screen, lambda: app_state.switch_phase(AppPhase.SIMULATION)),
            SetupModeSelectorButtons(graphics, setup_state),
            SetupModeStrategy(setup_state, railway, graphics)
        ]
        
        railway.trains.load_state()
        railway.signalling.unlock_all_paths()
