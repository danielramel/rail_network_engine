from core.graphics.graphics_context import GraphicsContext
from core.models.railway.railway_system import RailwaySystem
from modules.construction.models.construction_state import ConstructionState
from shared.ui.enums.edge_action import EdgeAction
from shared.ui.utils import draw_grid, draw_track, draw_node, draw_signal, draw_station, draw_dotted_line
from core.models.geometry.position import Position
from core.config.colors import RED, PURPLE


class ConstructionView:
    def __init__(self, railway: RailwaySystem, state: ConstructionState, graphics: GraphicsContext):
        self._railway = railway
        self._state = state
        self._surface = graphics.screen
        self._camera = graphics.camera
        
    def render(self, world_pos: Position | None) -> None:
        pass