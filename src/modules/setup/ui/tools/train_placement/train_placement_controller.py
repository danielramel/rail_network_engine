from core.config.settings import Config
from core.models.railway.railway_system import RailwaySystem
from core.graphics.graphics_context import GraphicsContext
from modules.setup.models.setup_state import SetupState
from modules.setup.models.setup_tool_controller import SetupToolController
from modules.setup.ui.tools.train_placement.train_placement_view import TrainPlacementView

class TrainPlacementController(SetupToolController):
    def __init__(self, railway: RailwaySystem, state: SetupState, graphics: GraphicsContext):
        view = TrainPlacementView(railway, state, graphics)
        super().__init__(view, railway, state, graphics)

    def _on_click(self, event)-> None:
        if event.is_right_click:
            self._state.switch_tool(None)
            return
        
        if self._state.preview.invalid_train_placement_edges:
            self._graphics.alert_component.show_alert('Cannot place train here! The path is blocked or invalid.')
            return
        if self._state.preview.train_to_preview is None:
            self._graphics.alert_component.show_alert('Click on a section of track to place a train.')
            return
        self._railway.trains.add_to_repository(self._state.preview.train_to_preview)