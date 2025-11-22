from core.graphics.graphics_context import GraphicsContext
from core.models.railway.railway_system import RailwaySystem
from modules.construction.models.construction_state import ConstructionState
from core.models.geometry.position import Position

class ConstructionView:
    def __init__(self, railway: RailwaySystem, state: ConstructionState, graphics: GraphicsContext):
        self._railway = railway
        self._state = state
        self._screen = graphics.screen
        self._camera = graphics.camera
        
    def render(self, world_pos: Position | None) -> None:
        pass