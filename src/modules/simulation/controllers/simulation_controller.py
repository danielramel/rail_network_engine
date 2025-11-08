from core.models.geometry import Position
from core.models.railway.railway_system import RailwaySystem
from modules.simulation.models.simulation_state import SimulationState
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from modules.simulation.views.simulation_view import SimulationView
from core.graphics.graphics_context import GraphicsContext
import pygame


class SimulationController(ClickableUIComponent, FullScreenUIComponent):
    handled_events = [pygame.MOUSEBUTTONUP]
    def __init__(self, railway: RailwaySystem, simulation_state: SimulationState, graphics: GraphicsContext):
        self.view = SimulationView(railway, simulation_state, graphics)
        self._state = simulation_state
        self._railway = railway
        self._camera = graphics.camera
        
        self._railway.signals.add_signals_to_dead_ends()

    def _on_click(self, event) -> bool:            
        snapped: Position = self._camera.screen_to_world(event.screen_pos).snap_to_grid()
        if self._railway.graph.has_node_at(snapped) and self._railway.signals.has_signal_at(snapped):
            signal = self._railway.signals.get(snapped)
            
            if event.button == 3 and signal.next_signal is not None:
                self._railway.signalling.disconnect_signal(signal)
                return True
            
            if self._state.selected_signal:
                self._railway.signalling.connect_signals(self._state.selected_signal, signal)
                self._state.selected_signal = None
                return True
            self._state.selected_signal = signal
            
        if event.button == 3:
            self._state.selected_signal = None
        return True
            
            
    def render(self, screen_pos: Position | None):
        world_pos = None if screen_pos is None else self._camera.screen_to_world(screen_pos)
        self.view.render(world_pos)

    
    def tick(self):
        if self._state.time.paused:
            return
        for _ in range(self._state.time.mode.value):
            self._railway.tick()