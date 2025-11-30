from core.graphics.graphics_context import GraphicsContext
from core.models.railway.railway_system import RailwaySystem
from modules.setup.train_placement.models.train_placement_state import TrainPlacementState
from core.models.geometry.position import Position


class TrainPlacementToolView:
    def __init__(self, railway: RailwaySystem, state: TrainPlacementState, graphics: GraphicsContext):
        self._railway = railway
        self._state = state
        self._screen = graphics.screen
        self._camera = graphics.camera
        
    def render(self, world_pos: Position | None) -> None:
        pass