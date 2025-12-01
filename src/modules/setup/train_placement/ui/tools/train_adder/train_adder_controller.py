from core.models.railway.railway_system import RailwaySystem
from core.graphics.graphics_context import GraphicsContext
from modules.setup.train_placement.models.train_placement_state import TrainPlacementState
from modules.setup.train_placement.models.train_placement_tool_controller import TrainPlacementToolController
from modules.setup.train_placement.ui.tools.train_adder.train_adder_view import TrainAdderView

class TrainAdderController(TrainPlacementToolController):
    def __init__(self, railway: RailwaySystem, state: TrainPlacementState, graphics: GraphicsContext):
        view = TrainAdderView(railway, state, graphics)
        super().__init__(view, railway, state, graphics)

    def _on_click(self, event)-> None:
        if event.is_right_click:
            self._state.switch_tool(None)
            return
        
        if self._state.preview.invalid_train_placement_edges:
            self._graphics.alert_component.show_alert('Cannot place train here! The path is already occupied or invalid.')
            return
        if self._state.preview.train_to_preview is None:
            self._graphics.alert_component.show_alert('Click on a section of track to place a train.')
            return
        self._railway.trains.add_to_repository(self._state.preview.train_to_preview)