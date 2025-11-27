from core.models.railway.railway_system import RailwaySystem
from core.graphics.graphics_context import GraphicsContext
from modules.setup.train_placement.models.train_placement_state import TrainPlacementState
from modules.setup.train_placement.models.train_placement_tool_controller import TrainPlacementToolController
from modules.setup.train_placement.ui.tools.train_removal.train_removal_view import TrainRemovalView

class TrainRemovalController(TrainPlacementToolController):
    def __init__(self, railway: RailwaySystem, state: TrainPlacementState, graphics: GraphicsContext):
        view = TrainRemovalView(railway, state, graphics)
        super().__init__(view, railway, state, graphics)

    def _on_click(self, event)-> None:            
        if event.is_right_click:
            self._state.switch_tool(None)
            return
        
        if self._state.preview.train_id_to_remove is not None:
            self._railway.trains.remove(self._state.preview.train_id_to_remove)
            return
        
        self._graphics.alert_component.show_alert("No train found here!")