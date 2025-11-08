from core.graphics.graphics_context import GraphicsContext
from core.models.geometry.position import Position
from core.models.railway.railway_system import RailwaySystem
from modules.setup.models.setup_state import SetupState
from modules.setup.models.setup_tool_controller import SetupToolController
from modules.setup.ui.setup_common_view import SetupCommonView
from modules.setup.ui.tools.train_placement.train_placement_controller import TrainPlacementController
from modules.setup.ui.tools.train_removal.train_removal_controller import TrainRemovalController
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent
from modules.setup.models.setup_state import SetupTool


class SetupToolStrategy(ClickableUIComponent, FullScreenUIComponent):
    def __init__(self, railway: RailwaySystem, state: SetupState, graphics: GraphicsContext):
        self.view = SetupCommonView(railway, state, graphics)
        self._railway = railway
        self._state = state
        self._graphics = graphics

        self._controllers: dict[SetupTool, SetupToolController] = {
            SetupTool.PLACE_TRAIN: TrainPlacementController(railway, state, graphics),
            SetupTool.REMOVE_TRAIN: TrainRemovalController(railway, state, graphics),
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