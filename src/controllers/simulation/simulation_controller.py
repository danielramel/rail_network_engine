import pygame
from models.geometry import Position
    
from graphics.camera import Camera
from models.railway_system import RailwaySystem
from models.time import TimeControlMode, TimeControlState
from ui.models.base import UIComponent
from views.simulation.simulation_view import SimulationView


class SimulationController(UIComponent):
    handled_events = [pygame.MOUSEBUTTONUP]
    def __init__(self, railway: RailwaySystem, camera: Camera, time_control_state: TimeControlState, screen: pygame.Surface):
        self.view = SimulationView(railway, camera, screen)
        self.time_control_state = time_control_state
        self._railway = railway
        self._camera = camera

    def handle_event(self, event):
        # handle click
        return True
            
            
    def render(self, screen_pos: Position | None):
        self.view.render(screen_pos)

    def contains(self, screen_pos: Position) -> bool:
        return True
    
    def tick(self):
        if self.time_control_state.paused:
            return
        for _ in range(self.time_control_state.mode.value):
            self._railway.tick()