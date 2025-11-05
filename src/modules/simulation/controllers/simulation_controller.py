import pygame
from models.geometry import Position
    
from models.railway_system import RailwaySystem
from models.simulation_state import SimulationState
from ui.models.ui_component import UIComponent
from modules.simulation.views.simulation_view import SimulationView
from graphics.graphics_context import GraphicsContext


class SimulationController(UIComponent):
    handled_events = [pygame.MOUSEBUTTONUP]
    def __init__(self, railway: RailwaySystem, simulation_state: SimulationState, graphics: GraphicsContext):
        self.view = SimulationView(railway, simulation_state, graphics)
        self._simulation_state = simulation_state
        self._railway = railway
        self._camera = graphics.camera
        
        self._railway.signals.add_signals_to_dead_ends()

    def process_event(self, event) -> bool:            
        snapped: Position = self._camera.screen_to_world(event.screen_pos).snap_to_grid()
        if self._railway.graph.has_node_at(snapped) and self._railway.signals.has_signal_at(snapped):
            signal = self._railway.signals.get(snapped)
            
            if event.button == 3 and signal.next_signal is not None:
                self._railway.signalling.disconnect_signal(signal)
                return True
            
            if self._simulation_state.selected_signal:
                self._railway.signalling.connect_signals(self._simulation_state.selected_signal, signal)
                self._simulation_state.selected_signal = None
                return True
            self._simulation_state.selected_signal = signal
            
        if event.button == 3:
            self._simulation_state.selected_signal = None
        return True
            
            
    def render(self, screen_pos: Position | None):
        world_pos = None if screen_pos is None else self._camera.screen_to_world(screen_pos)
        self.view.render(world_pos)

    def contains(self, screen_pos: Position) -> bool:
        return True
    
    def tick(self):
        if self._simulation_state.time.paused:
            return
        for _ in range(self._simulation_state.time.mode.value):
            self._railway.tick()