from abc import ABC, abstractmethod
from ui.construction.construction_view import ConstructionView
from models.geometry import Position
import pygame

class UIController(ABC):
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Process a pygame event. Return True if consumed."""
        
    def render(self) -> None:
        self.view.render()
        
        
        
from domain.rail_map import RailMap
from models.construction import ConstructionState
from graphics.camera import Camera


class ConstructionModeController(UIController):
    """Base class for controllers that manage construction modes."""
    def __init__(self, view: ConstructionView, map: RailMap, state: ConstructionState, camera: Camera):
        self.view = view
        self._map = map
        self._construction_state = state
        self._camera = camera
        
    def render(self, world_pos: Position):
        self.view.render(world_pos)