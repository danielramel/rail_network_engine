from core.graphics.graphics_context import GraphicsContext
from modules.simulation.ui.panel.train_panel_manager import TrainPanelManager
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from shared.ui.models.ui_controller import UIController
from modules.simulation.ui.time_control_buttons import TimeControlButtons
from shared.ui.components.time_display import TimeDisplay
from shared.controllers.camera_controller import CameraController
from modules.simulation.ui.simulation_controller import SimulationController
from core.models.railway.railway_system import RailwaySystem
from modules.simulation.models.simulation_state import SimulationState

class SimulationMode(UIController, FullScreenUIComponent):
    elements: tuple[ClickableUIComponent]

    def __init__(self, railway: RailwaySystem, graphics: GraphicsContext):
        self._railway = railway
        self._graphics = graphics
        self.elements = ()

        graphics.input_component.request_input(
            "Enter simulation start time (HH:MM):",
            self._on_time_set
        )
        # self._on_time_set("00:00:00")

    def _initialize(self):
        self._state = SimulationState(self._railway.time)
        self.elements = (
            TimeControlButtons(self._state.time_control, self._graphics.screen),
            TimeDisplay(self._state.time, self._graphics),
            TrainPanelManager(self._railway, self._state, self._graphics.screen, self._railway.routes),
            CameraController(self._graphics.camera),
            SimulationController(self._railway, self._state, self._graphics),
        )

    def _on_time_set(self, time_str: str) -> None:
        try:
            self._railway.time.set_time_from_string(time_str)
        except ValueError:
            self._graphics.alert_component.show_alert("Invalid time format. Use HH:MM.")
            self._graphics.input_component.request_input(
                "Enter simulation start time (HH:MM):",
                self._on_time_set
            )
            return
        self._initialize()
