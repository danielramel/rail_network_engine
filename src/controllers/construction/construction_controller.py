import pygame
from graphics.graphics_context import GraphicsContext
from models.geometry import Position
    
from models.railway_system import RailwaySystem
from models.construction_state import ConstructionState, ConstructionMode
from ui.models.ui_component import UIComponent
from .rail_controller import RailController
from .platform_controller import PlatformController
from .signal_controller import SignalController
from .station_controller import StationController
from .bulldoze_controller import BulldozeController
from views.construction.construction_view import ConstructionCommonView
from .base_construction_controller import BaseConstructionController

class ConstructionController(UIComponent):
    handled_events = [pygame.MOUSEBUTTONUP]
    def __init__(self, railway: RailwaySystem, state: ConstructionState, graphics: GraphicsContext):
        self.view = ConstructionCommonView(railway, state, graphics)
        self._railway = railway
        self._state = state
        self._graphics = graphics

        self._controllers: dict[ConstructionMode, BaseConstructionController] = {
            ConstructionMode.RAIL: RailController(railway, state, graphics),
            ConstructionMode.SIGNAL: SignalController(railway, state, graphics),
            ConstructionMode.STATION: StationController(railway, state, graphics),
            ConstructionMode.PLATFORM: PlatformController(railway, state, graphics),
            ConstructionMode.BULLDOZE: BulldozeController(railway, state, graphics),
        }
        
    def _handle_filtered_event(self, event):                
        if self._state.mode is None:
            return
        
        if event.button not in (1, 3):
            return
        
        self._controllers[self._state.mode]._handle_filtered_event(event)
            
            
    def render(self, screen_pos: Position | None):
        self.view.render(screen_pos)
        
        if self._state.mode is None:
            return

        self._controllers[self._state.mode].render(screen_pos)

    def contains(self, screen_pos: Position) -> bool:
        return True