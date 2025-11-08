import pygame
from core.models.railway.railway_system import RailwaySystem
from modules.construction.models.construction_state import ConstructionState
from core.graphics.camera import Camera
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from modules.construction.models.construction_view import ConstructionView
from core.models.geometry.position import Position


class ConstructionToolController(ClickableUIComponent):
    handled_events = [pygame.MOUSEBUTTONUP]
    """Base class for controllers that manage construction modes."""
    def __init__(self, view: ConstructionView, railway: RailwaySystem, state: ConstructionState, camera: Camera):
        self.view = view
        self._railway = railway
        self._construction_state = state
        self._camera = camera

    def render(self, screen_pos: Position):
        world_pos = self._camera.screen_to_world(screen_pos) if screen_pos is not None else None
        self.view.render(world_pos)