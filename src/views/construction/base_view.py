from graphics.graphics_context import GraphicsContext
from models.railway_system import RailwaySystem
from models.construction_state import ConstructionState

from models.geometry.position import Position
from models.simulation_state import SimulationState

class BaseView():
    def __init__(self, railway: RailwaySystem, state: ConstructionState | SimulationState, graphics: GraphicsContext):
        self._railway = railway
        self._state = state
        self._surface = graphics.screen
        self._camera = graphics.camera
        
    def render(self, world_pos: Position):
        """Render this construction view"""
        pass