import pygame
from models.geometry import Position
    
from graphics.camera import Camera
from models.simulation import Simulation
from ui.models.base import UIComponent
from views.simulation.simulation_view import SimulationView


class SimulationController(UIComponent):
    handled_events = [pygame.MOUSEBUTTONUP]
    def __init__(self, simulation: Simulation, camera: Camera, screen: pygame.Surface):
        self.view = SimulationView(simulation, camera, screen)
        self._simulation = simulation
        self._camera = camera

    def handle_event(self, event):
        # handle click
        return True
            
            
    def render(self, screen_pos: Position | None):
        self.view.render(screen_pos)

    def contains(self, screen_pos: Position) -> bool:
        return True