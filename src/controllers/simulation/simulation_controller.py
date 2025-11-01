import pygame
from models.geometry import Position
    
from graphics.camera import Camera
from models.railway_system import RailwaySystem
from models.simulation_state import SimulationState
from ui.models.base import UIComponent
from views.simulation.simulation_view import SimulationView


class SimulationController(UIComponent):
    handled_events = [pygame.MOUSEBUTTONUP]
    def __init__(self, railway: RailwaySystem, camera: Camera, simulation_state: SimulationState, screen: pygame.Surface):
        self.view = SimulationView(railway, camera, screen, simulation_state)
        self._simulation_state = simulation_state
        self._railway = railway
        self._camera = camera

    def handle_event(self, event) -> bool:
        if event.button == 3:
            self._simulation_state.selected_signal = None
            return True
            
        snapped: Position = self._camera.screen_to_world(event.screen_pos).snap_to_grid()
        if self._railway.graph.has_node_at(snapped) and self._railway.signals.has_signal_at(snapped):
            signal = self._railway.signals.get(snapped)
            if self._simulation_state.selected_signal:
                if self._simulation_state.selected_signal == signal:
                    self._simulation_state.selected_signal = None
                    return True

                path = self._railway.signals.find_path(self._simulation_state.selected_signal, signal)
                self._simulation_state.selected_signal.connect(path, signal)
                self._railway.signals.lock_path(path)
                self._simulation_state.selected_signal = None
                return True
            self._simulation_state.selected_signal = signal
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