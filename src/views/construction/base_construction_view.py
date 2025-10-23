from models.simulation import Simulation
from models.construction import ConstructionState
from graphics.camera import Camera
import pygame

from models.geometry.position import Position
from abc import ABC, abstractmethod

class BaseConstructionView(ABC):
    def __init__(self, simulation: Simulation, state: ConstructionState, camera: Camera, surface: pygame.Surface):
        self._simulation = simulation
        self._construction_state = state
        self._camera = camera
        self._surface = surface
        
    @abstractmethod
    def render(self, world_pos: Position):
        """Render this construction view"""