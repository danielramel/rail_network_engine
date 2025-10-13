import pygame
from models.geometry import Position
    
from graphics.camera import Camera
from domain.rail_map import RailMap
from models.construction import ConstructionState, ConstructionMode
from models.event import Event, CLICK_TYPE
from ui.components.base import BaseUIComponent
from .rail_controller import RailController
from .platform_controller import PlatformController
from .signal_controller import SignalController
from .station_controller import StationController
from .bulldoze_controller import BulldozeController
from views.construction.construction_view import ConstructionCommonView
from .base_construction_controller import BaseConstructionController

class ConstructionManager(BaseUIComponent):
    def __init__(self, map: RailMap, state: ConstructionState, camera: Camera, screen: pygame.Surface):
        self.view = ConstructionCommonView(map, state, camera, screen)
        self._map = map
        self._construction_state = state
        self._camera = camera

        self._controllers: dict[ConstructionMode, BaseConstructionController] = {
            ConstructionMode.RAIL: RailController(map, state, camera, screen),
            ConstructionMode.SIGNAL: SignalController(map, state, camera, screen),
            ConstructionMode.STATION: StationController(map, state, camera, screen),
            ConstructionMode.PLATFORM: PlatformController(map, state, camera, screen),
            ConstructionMode.BULLDOZE: BulldozeController(map, state, camera, screen),
        }
        
    def handle_event(self, event):                
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._camera.start_drag(event.pos_)

        elif event.type == pygame.MOUSEMOTION:
            self._camera.update_drag(event.pos_)

        elif event.type == pygame.MOUSEWHEEL:
            self._camera.zoom(event.pos_, event.y)

        elif event.type == pygame.MOUSEBUTTONUP:
            was_dragging = self._camera.stop_drag(event.pos_)

            if was_dragging:
                return
            
            if self._construction_state.mode is None:
                return
            
            if event.button not in (1, 3):
                return
            
            click_type = CLICK_TYPE.LEFT_CLICK if event.button == 1 else CLICK_TYPE.RIGHT_CLICK
            event = Event(click_type, event.pos_)
            self._controllers[self._construction_state.mode].handle_event(event)
            
        return True
            
            
    def render(self, screen_pos: Position | None):
        self.view.render(screen_pos)
        
        if self._construction_state.mode is None:
            return
        

        self._controllers[self._construction_state.mode].render(screen_pos)

    def contains(self, screen_pos: Position) -> bool:
        return True