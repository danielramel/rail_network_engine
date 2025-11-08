from core.models.geometry import Position
from core.models.railway.railway_system import RailwaySystem
from modules.setup.models.setup_state import SetupState
from modules.setup.ui.setup_view import SetupView
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from core.graphics.graphics_context import GraphicsContext
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent
import pygame


class SetupController(ClickableUIComponent, FullScreenUIComponent):
    handled_events = [pygame.MOUSEBUTTONUP]
    def __init__(self, railway: RailwaySystem, setup_state: SetupState, graphics: GraphicsContext):
        self.view = SetupView(railway, setup_state, graphics)
        self._railway = railway
        self._camera = graphics.camera
        self._state = setup_state
        
        self._railway.signals.add_signals_to_dead_ends()

    def _on_click(self, event)-> None:            
        if not event.is_left_click:
            return
        
        closest_edge = event.world_pos.closest_edge(self._railway.graph.edges, self._camera.scale)
        if closest_edge and self._railway.stations.is_edge_platform(closest_edge):
            platform = sorted(self._railway.stations.get_platform_from_edge(closest_edge))
            train = self._railway.trains.get_train_on_edge(closest_edge)
            if train is not None:
                self._railway.trains.switch_direction(train)
                
            else:
                self._railway.trains.add_to_platform(platform)

    def render(self, screen_pos: Position | None):
        world_pos = None if screen_pos is None else self._camera.screen_to_world(screen_pos)
        self.view.render(world_pos)