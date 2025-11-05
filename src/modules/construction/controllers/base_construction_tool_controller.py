from core.models.railway.railway_system import RailwaySystem
from modules.construction.models.construction_state import ConstructionState
from core.graphics.camera import Camera
from shared.ui.models.ui_component import UIComponent
from shared.views.base_view import BaseView
from core.models.geometry.position import Position


class BaseConstructionToolController(UIComponent):
    """Base class for controllers that manage construction modes."""
    def __init__(self, view: BaseView, railway: RailwaySystem, state: ConstructionState, camera: Camera):
        self.view = view
        self._railway = railway
        self._construction_state = state
        self._camera = camera

    def render(self, screen_pos: Position):
        if screen_pos is None:
            self.view.render(None)
            return
        world_pos = self._camera.screen_to_world(screen_pos)
        self.view.render(world_pos)