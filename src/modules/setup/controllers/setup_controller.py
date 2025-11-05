import pygame
from core.models.geometry import Position
from core.models.railway.railway_system import RailwaySystem
from modules.setup.view.setup_view import SetupView
from shared.ui.models.ui_component import UIComponent
from core.graphics.graphics_context import GraphicsContext


class SetupController(UIComponent):
    handled_events = [pygame.MOUSEBUTTONUP]
    def __init__(self, railway: RailwaySystem, graphics: GraphicsContext):
        self.view = SetupView(railway, graphics)
        self._railway = railway
        self._camera = graphics.camera
        
        self._railway.signals.add_signals_to_dead_ends()

    def process_event(self, event) -> bool:            
        pass
            
            
    def render(self, screen_pos: Position | None):
        world_pos = None if screen_pos is None else self._camera.screen_to_world(screen_pos)
        self.view.render(world_pos)

    def contains(self, screen_pos: Position) -> bool:
        return True