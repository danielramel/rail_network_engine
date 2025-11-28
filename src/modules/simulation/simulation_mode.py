from core.graphics.graphics_context import GraphicsContext
from core.models.app_state import AppState
from modules.simulation.end_simulation_button import EndSimulationButton
from modules.simulation.ui.panel.train_panel_manager import TrainPanelManager
from shared.ui.components.zoom_button import ZoomButton
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from shared.ui.models.ui_controller import UIController
from modules.simulation.ui.time_control_buttons import TimeControlButtons
from modules.simulation.ui.time_display import TimeDisplay
from shared.controllers.camera_controller import CameraController
from modules.simulation.ui.simulation_controller import SimulationController
from core.models.railway.railway_system import RailwaySystem
from modules.simulation.models.simulation_state import SimulationState
from typing import Callable

class SimulationMode(UIController, FullScreenUIComponent):
    elements: tuple[ClickableUIComponent]
    def __init__(self, app_state: AppState, railway: RailwaySystem, graphics: GraphicsContext) -> None:
        self._railway = railway
        self._graphics = graphics
        self.elements = ()
        self._app_state = app_state
        # graphics.input_component.request_input(
        #     "Enter simulation start time (HH:MM):",
        #     self._on_time_set
        # )
        self._on_time_set("04:49")
        
        

    def _on_time_set(self, time_str: str) -> None:
        if time_str is None:
            self._app_state.end_simulation()
            return
        
        time_set = self._railway.time.set_time_from_string(time_str)
        if not time_set:
            self._graphics.alert_component.show_alert("Invalid time format. Use HH:MM.")
            self._graphics.input_component.request_input(
                "Enter simulation start time (HH:MM):",
                self._on_time_set
            )
            return
        
        self._state = SimulationState(self._railway.time)
        self.elements = (
            EndSimulationButton(self._graphics.screen, self._app_state.end_simulation),
            TimeControlButtons(self._state.time_control, self._graphics.screen),
            TimeDisplay(self._state.time, self._graphics),
            TrainPanelManager(self._railway, self._state, self._graphics.screen, self._railway.routes),
            ZoomButton(self._graphics.screen, self._graphics.camera),
            CameraController(self._graphics.camera),
            SimulationController(self._railway, self._state, self._graphics),
        )
        self._railway.trains.save_state()
        self._railway.signalling.lock_paths_under_trains()
        self._railway.routes.calculate_start_times()
        self._railway.signalling.reset()
        self._railway.signals.reset_all()
        