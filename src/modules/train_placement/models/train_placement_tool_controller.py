from core.models.railway.railway_system import RailwaySystem
from core.graphics.graphics_context import GraphicsContext
from modules.train_placement.models.train_placement_state import TrainPlacementState
from modules.train_placement.models.train_placement_view import TrainPlacementView
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from core.models.geometry.position import Position
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent



class TrainPlacementToolController(ClickableUIComponent, FullScreenUIComponent):
    """Base class for controllers that manage setup modes."""
    def __init__(self, view: TrainPlacementView, railway: RailwaySystem, state: TrainPlacementState, graphics: GraphicsContext):
        self._view = view
        self._railway = railway
        self._state = state
        self._graphics = graphics
        
    def render(self, screen_pos: Position | None) -> None:
        world_pos = self._graphics.camera.screen_to_world(screen_pos) if screen_pos is not None else None
        self._view.render(world_pos)