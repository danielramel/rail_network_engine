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


    def _on_click(self, click: Event) -> None:
        snapped = self._camera.screen_to_world(click.screen_pos).snap_to_grid()
        if click.is_right_click:
            if self._state.selected_signal:
                self._state.selected_signal = None
            elif self._railway.signals.has_signal_at(snapped):
                self._railway.signalling.disconnect_signal_at(snapped)
            return
                
        if self._railway.signals.has_signal_at(snapped):
            signal = self._railway.signals.get(snapped)
                        
            if self._state.selected_signal:
                self._railway.signalling.connect_signals(self._state.selected_signal, signal)
                self._state.selected_signal = None
            else:
                self._state.selected_signal = signal
            return
            
        closest_edge = self._railway.graph_service.get_closest_edge_on_grid(click.world_pos, self._camera.scale)
        train_id = self._railway.trains.get_train_on_edge(closest_edge)
        if train_id:
            if train_id in self._state.selected_trains:
                self._state.deselect_train(train_id)
            else:
                self._state.select_train(train_id)
            
            
    def render(self, screen_pos: Position | None):
        world_pos = None if screen_pos is None else self._camera.screen_to_world(screen_pos)
        self.view.render(world_pos)

    
    def tick(self):
        if self._state.time_control.paused:
            return
        self._state.tick()
        for _ in range(self._state.time_control.mode.value):
            self._railway.tick()