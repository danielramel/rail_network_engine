import pygame
from models.geometry import Position
    
from graphics.camera import Camera
from models.simulation import Simulation
from models.construction import ConstructionState, ConstructionMode
from models.event import Event, CLICK_TYPE
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
    def __init__(self, simulation: Simulation, state: ConstructionState, camera: Camera, screen: pygame.Surface):
        self.view = ConstructionCommonView(simulation, state, camera, screen)
        self._simulation = simulation
        self._construction_state = state
        self._camera = camera

        self._controllers: dict[ConstructionMode, BaseConstructionController] = {
            ConstructionMode.RAIL: RailController(simulation, state, camera, screen),
            ConstructionMode.SIGNAL: SignalController(simulation, state, camera, screen),
            ConstructionMode.STATION: StationController(simulation, state, camera, screen),
            ConstructionMode.PLATFORM: PlatformController(simulation, state, camera, screen),
            ConstructionMode.BULLDOZE: BulldozeController(simulation, state, camera, screen),
        }
        
    def handle_event(self, event):                
        if self._construction_state.mode is None:
            return
        
        if event.button not in (1, 3):
            return
        
        click_type = CLICK_TYPE.LEFT_CLICK if event.button == 1 else CLICK_TYPE.RIGHT_CLICK
        event = Event(click_type, event.pos_)
        self._controllers[self._construction_state.mode].handle_event(event)
            
            
    def render(self, screen_pos: Position | None):
        self.view.render(screen_pos)
        
        if self._construction_state.mode is None:
            return
        

        self._controllers[self._construction_state.mode].render(screen_pos)

    def contains(self, screen_pos: Position) -> bool:
        return True