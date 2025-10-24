import pygame
from models.geometry import Position
    
from graphics.camera import Camera
from models.railway_system import RailwaySystem
from models.construction import ConstructionState, ConstructionMode
from ui.models.base import UIComponent
from .rail_controller import RailController
from .platform_controller import PlatformController
from .signal_controller import SignalController
from .station_controller import StationController
from .bulldoze_controller import BulldozeController
from views.construction.construction import ConstructionCommonView
from .base_construction_controller import BaseConstructionController

class ConstructionController(UIComponent):
    handled_events = [pygame.MOUSEBUTTONUP]
    def __init__(self, railway: RailwaySystem, state: ConstructionState, camera: Camera, screen: pygame.Surface):
        self.view = ConstructionCommonView(railway, state, camera, screen)
        self._railway = railway
        self._construction_state = state
        self._camera = camera

        self._controllers: dict[ConstructionMode, BaseConstructionController] = {
            ConstructionMode.RAIL: RailController(railway, state, camera, screen),
            ConstructionMode.SIGNAL: SignalController(railway, state, camera, screen),
            ConstructionMode.STATION: StationController(railway, state, camera, screen),
            ConstructionMode.PLATFORM: PlatformController(railway, state, camera, screen),
            ConstructionMode.BULLDOZE: BulldozeController(railway, state, camera, screen),
        }
        
    def handle_event(self, event):                
        if self._construction_state.mode is None:
            return
        self._controllers[self._construction_state.mode].handle_event(event)
            
            
    def render(self, screen_pos: Position | None):
        self.view.render(screen_pos)
        
        if self._construction_state.mode is None:
            return
    
        self._controllers[self._construction_state.mode].render(screen_pos)

    def contains(self, screen_pos: Position) -> bool:
        return True