from core.graphics.graphics_context import GraphicsContext
from core.models.railway.railway_system import RailwaySystem

from core.models.geometry.position import Position

class BaseView:
    def __init__(self, railway: RailwaySystem, state, graphics: GraphicsContext):
        self._railway = railway
        self._state = state
        self._surface = graphics.screen
        self._camera = graphics.camera
        
    def render(self, world_pos: Position):
        """Render this construction view"""
        pass