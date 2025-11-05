import pygame
from core.models.railway.railway_system import RailwaySystem
from modules.construction.models.construction_state import ConstructionState
from core.graphics.graphics_context import GraphicsContext
from shared.ui.models.ui_component import UIComponent
from modules.construction.views.construction_common_view import ConstructionCommonView
from modules.construction.models.construction_state import ConstructionTool
from core.models.geometry.position import Position
from .rail_controller import RailController
from .platform_controller import PlatformController
from .signal_controller import SignalController
from .station_controller import StationController
from .bulldoze_controller import BulldozeController
from .base_construction_tool_controller import BaseConstructionToolController

class ConstructionToolStrategy(UIComponent):
    handled_events = [pygame.MOUSEBUTTONUP]
    def __init__(self, railway: RailwaySystem, state: ConstructionState, graphics: GraphicsContext):
        self.view = ConstructionCommonView(railway, state, graphics)
        self._railway = railway
        self._state = state
        self._graphics = graphics

        self._controllers: dict[ConstructionTool, BaseConstructionToolController] = {
            ConstructionTool.RAIL: RailController(railway, state, graphics),
            ConstructionTool.SIGNAL: SignalController(railway, state, graphics),
            ConstructionTool.STATION: StationController(railway, state, graphics),
            ConstructionTool.PLATFORM: PlatformController(railway, state, graphics),
            ConstructionTool.BULLDOZE: BulldozeController(railway, state, graphics),
        }
        
    def process_event(self, event):                
        if self._state.tool is None:
            return
        
        if event.button not in (1, 3):
            return
        
        self._controllers[self._state.tool].process_event(event)
            
            
    def render(self, screen_pos: Position | None):
        self.view.render(screen_pos)
        
        if self._state.tool is None:
            return

        self._controllers[self._state.tool].render(screen_pos)

    def contains(self, screen_pos: Position) -> bool:
        return True