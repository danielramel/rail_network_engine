from core.models.railway.railway_system import RailwaySystem
from core.graphics.graphics_context import GraphicsContext
from modules.setup.models.setup_state import SetupState
from modules.setup.models.setup_tool_controller import SetupToolController
from modules.setup.ui.tools.train_removal.train_removal_view import TrainRemovalView

class TrainRemovalController(SetupToolController):
    def __init__(self, railway: RailwaySystem, state: SetupState, graphics: GraphicsContext):
        view = TrainRemovalView(railway, state, graphics)
        super().__init__(view, railway, state, graphics.camera)

    def _on_click(self, event)-> None:            
        if event.is_right_click:
            self._state.switch_tool(None)
            return
        
        closest_edge = event.world_pos.closest_edge(self._railway.graph.edges, self._camera.scale)
        if closest_edge and self._railway.stations.is_edge_platform(closest_edge):
            train_id = self._railway.trains.get_train_on_edge(closest_edge)
            self._railway.trains.remove(train_id)