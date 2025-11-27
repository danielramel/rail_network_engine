from core.graphics.graphics_context import GraphicsContext
from core.models.railway.railway_system import RailwaySystem
from modules.setup.construction.models.construction_state import ConstructionState
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from modules.setup.construction.models.construction_view import ConstructionView
from core.models.geometry.position import Position
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent


class ConstructionToolController(ClickableUIComponent, FullScreenUIComponent):
    """Base class for controllers that manage construction modes."""
    def __init__(self, view: ConstructionView, railway: RailwaySystem, state: ConstructionState, graphics: GraphicsContext):
        self.view = view
        self._railway = railway
        self._state = state
        self._graphics = graphics
        
    def render(self, screen_pos: Position):
        world_pos = self._graphics.camera.screen_to_world(screen_pos) if screen_pos is not None else None
        self.view.render(world_pos)