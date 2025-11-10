from core.models.geometry import Position
from core.models.railway.railway_system import RailwaySystem
from modules.simulation.models.simulation_state import SimulationState
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from modules.simulation.ui.simulation_view import SimulationView
from core.graphics.graphics_context import GraphicsContext
from core.models.event import Event
import pygame


class SimulationController(ClickableUIComponent, FullScreenUIComponent):
    handled_events = [pygame.MOUSEBUTTONUP]
    def __init__(self, railway: RailwaySystem, simulation_state: SimulationState, graphics: GraphicsContext):
        self.view = SimulationView(railway, simulation_state, graphics)
        self._state = simulation_state
        self._railway = railway
        self._camera = graphics.camera
        
        self._railway.signals.add_signals_to_dead_ends()

    def _on_click(self, click: Event) -> None:
        snapped = self._camera.screen_to_world(click.screen_pos).snap_to_grid()
        if click.is_right_click:
            if self._state.selected_signal:
                self._state.selected_signal = None
            elif self._railway.signals.has_signal_at(snapped):
                self._railway.signalling.disconnect_signal_at(snapped)
            elif self._state.selected_train:
                self._state.selected_train = None
            return
                
        if self._railway.signals.has_signal_at(snapped):
            signal = self._railway.signals.get(snapped)
                        
            if self._state.selected_signal:
                self._railway.signalling.connect_signals(self._state.selected_signal, signal)
                self._state.selected_signal = None
                return
            self._state.selected_signal = signal
            
        closest_edge = click.world_pos.closest_edge(self._railway.graph.edges, self._camera.scale)
        train_id = closest_edge is not None and self._railway.trains.get_train_on_edge(closest_edge)
        if train_id:
            if self._state.selected_train is not None and self._state.selected_train.id == train_id:
                self._state.selected_train = None
                return
            self._state.selected_train = self._railway.trains.get(train_id)
            
            
    def render(self, screen_pos: Position | None):
        world_pos = None if screen_pos is None else self._camera.screen_to_world(screen_pos)
        self.view.render(world_pos)

    
    def tick(self):
        if self._state.time_control.paused:
            return
        self._state.tick()
        for _ in range(self._state.time_control.mode.value):
            self._railway.tick()