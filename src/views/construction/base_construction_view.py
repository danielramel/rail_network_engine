from graphics.graphics_context import GraphicsContext
from models.railway_system import RailwaySystem
from models.construction_state import ConstructionState
from graphics.camera import Camera
import pygame

from models.geometry.position import Position
from abc import ABC, abstractmethod

class BaseConstructionView(ABC):
    def __init__(self, railway: RailwaySystem, state: ConstructionState, graphics: GraphicsContext):
        self._railway = railway
        self._state = state
        self._surface = graphics.screen
        self._camera = graphics.camera
        
    @abstractmethod
    def render(self, world_pos: Position):
        """Render this construction view"""