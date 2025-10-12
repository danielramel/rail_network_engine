from domain.rail_map import RailMap
from models.construction import ConstructionState
from graphics.camera import Camera
from views.construction.base_construction_view import BaseConstructionView
from models.geometry import Position
from ui.components.base import BaseUIComponent

class BaseConstructionController(BaseUIComponent):
    """Base class for controllers that manage construction modes."""
    def __init__(self, view: BaseConstructionView, map: RailMap, state: ConstructionState, camera: Camera):
        self.view = view
        self._map = map
        self._construction_state = state
        self._camera = camera

    def render(self, screen_pos: Position):
        world_pos = self._camera.screen_to_world(screen_pos)
        self.view.render(world_pos)