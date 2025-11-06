from core.models.geometry import Position
from core.models.railway.railway_system import RailwaySystem
from modules.setup.view.setup_view import SetupView
from shared.ui.models.clickable_component import ClickableComponent
from core.graphics.graphics_context import GraphicsContext
import pygame


class SetupController(ClickableComponent):
    handled_events = [pygame.MOUSEBUTTONUP]
    def __init__(self, railway: RailwaySystem, graphics: GraphicsContext):
        self.view = SetupView(railway, graphics)
        self._railway = railway
        self._camera = graphics.camera
        
        self._railway.signals.add_signals_to_dead_ends()

    def process_event(self, event) -> bool:            
        if event.button != 1:
            return False
        
        closest_edge = event.world_pos.closest_edge(self._railway.graph.edges, self._camera.scale)
        if closest_edge and self._railway.stations.is_edge_platform(closest_edge):
            platform = self._railway.stations.get_platform_from_edge(closest_edge)
            sorted_platform = sorted(platform)
            pos = sorted_platform[0].a
            self._railway.trains.add_to_platform(platform, pos)

    def render(self, screen_pos: Position | None):
        world_pos = None if screen_pos is None else self._camera.screen_to_world(screen_pos)
        self.view.render(world_pos)