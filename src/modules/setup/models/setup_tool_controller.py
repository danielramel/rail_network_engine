from core.models.railway.railway_system import RailwaySystem
from core.graphics.camera import Camera
from modules.setup.models.setup_state import SetupState
from modules.setup.models.setup_view import SetupView
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from core.models.geometry.position import Position
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent



class SetupToolController(ClickableUIComponent, FullScreenUIComponent):
    """Base class for controllers that manage setup modes."""
    def __init__(self, view: SetupView, railway: RailwaySystem, state: SetupState, camera: Camera):
        self._view = view
        self._railway = railway
        self._state = state
        self._camera = camera

    def render(self, screen_pos: Position):
        world_pos = self._camera.screen_to_world(screen_pos) if screen_pos is not None else None
        self._view.render(world_pos)