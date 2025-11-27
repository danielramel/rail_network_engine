from core.graphics.graphics_context import GraphicsContext
from core.models.geometry.position import Position
from core.models.railway.railway_system import RailwaySystem
from modules.train_placement.models.train_placement_state import TrainPlacementState
from modules.train_placement.models.train_placement_tool_controller import TrainPlacementToolController
from modules.train_placement.ui.train_placement_common_view import TrainPlacementCommonView
from modules.train_placement.ui.tools.train_adder.train_adder_controller import TrainAdderController
from modules.train_placement.ui.tools.train_removal.train_removal_controller import TrainRemovalController
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent
from modules.train_placement.models.train_placement_state import TrainPlacementTool


class TrainPlacementToolStrategy(ClickableUIComponent, FullScreenUIComponent):
    def __init__(self, railway: RailwaySystem, state: TrainPlacementState, graphics: GraphicsContext):
        self.view = TrainPlacementCommonView(railway, state, graphics)
        self._railway = railway
        self._state = state
        self._graphics = graphics

        self._controllers: dict[TrainPlacementTool, TrainPlacementToolController] = {
            TrainPlacementTool.PLACE_TRAIN: TrainAdderController(railway, state, graphics),
            TrainPlacementTool.REMOVE_TRAIN: TrainRemovalController(railway, state, graphics),
        }
        
    def _on_click(self, event) -> None:
        if self._state.tool is None:
            return
        
        self._controllers[self._state.tool].dispatch_event(event)
            
            
    def render(self, screen_pos: Position | None):
        self.view.render(screen_pos)
        if self._state.tool is None:
            return

        if self._state.tool is not None:
            self._controllers[self._state.tool].render(screen_pos)