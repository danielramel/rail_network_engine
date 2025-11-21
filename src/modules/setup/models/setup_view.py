from core.graphics.graphics_context import GraphicsContext
from core.models.railway.railway_system import RailwaySystem
from modules.setup.models.setup_state import SetupState
from core.models.geometry.position import Position


class SetupView:
    def __init__(self, railway: RailwaySystem, state: SetupState, graphics: GraphicsContext):
        self._railway = railway
        self._state = state
        self._screen = graphics.screen
        self._camera = graphics.camera
        
    def render(self, world_pos: Position | None) -> None:
        pass