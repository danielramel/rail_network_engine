from core.config.settings import Config
from core.models.geometry.edge import Edge
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
        
        closest_edge = self._railway.graph_service.get_closest_edge_on_grid(event.world_pos, self._graphics.camera.scale)
        if closest_edge and self._railway.stations.is_edge_platform(closest_edge) and not self._railway.trains.get_train_on_edge(closest_edge):
            platform = self._railway.stations.get_platform_from_edge(closest_edge)
            if self._state.train_config.total_length > len(platform) *  Config.SHORT_SEGMENT_LENGTH:
                self._graphics.alert_component.show_alert('Train is too long for the selected platform!')
                return
            self._railway.trains.add_to_platform(platform, self._state.train_config)