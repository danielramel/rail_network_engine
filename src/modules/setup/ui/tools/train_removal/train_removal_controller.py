from core.models.railway.railway_system import RailwaySystem
from core.graphics.graphics_context import GraphicsContext
from modules.setup.models.setup_state import SetupState
from modules.setup.models.setup_tool_controller import SetupToolController
from modules.setup.ui.tools.train_removal.train_removal_view import TrainRemovalView

class TrainRemovalController(SetupToolController):
    def __init__(self, railway: RailwaySystem, state: SetupState, graphics: GraphicsContext):
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