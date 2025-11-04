from models.railway_system import RailwaySystem
from models.construction_state import ConstructionState
from graphics.camera import Camera
from views.construction.base_construction_view import BaseConstructionView
from models.geometry import Position
from ui.models.ui_component import UIComponent

class BaseConstructionController(UIComponent):
    """Base class for controllers that manage construction modes."""
    def __init__(self, view: BaseConstructionView, railway: RailwaySystem, state: ConstructionState, camera: Camera):
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